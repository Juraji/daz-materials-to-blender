import gzip
import json
import winreg
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import TypeVar, Generic
from urllib import parse as urlparse

from .json import serializable
from .slugify import slugify

DMC_V = TypeVar('DMC_V')


@serializable("has_image", "is_set")
@dataclass
class DsonChannel(Generic[DMC_V]):
    value: DMC_V
    default_value: DMC_V
    image_file: str | None

    def has_image(self) -> bool: return self.image_file is not None

    def is_set(self):
        return self.value != self.default_value or self.has_image()


@dataclass
class DsonColorChannel(DsonChannel[tuple[float, float, float]]):
    alpha: float = 1.0

    def as_rgba(self) -> tuple[float, float, float, float]:
        return self.value[0], self.value[1], self.value[2], self.alpha

    def as_float(self):
        return (sum(self.value) / 3) * self.alpha


@dataclass
class DsonFloatChannel(DsonChannel[float]):
    pass


@dataclass
class DsonBoolChannel(DsonChannel[bool]):
    pass


@dataclass
class DsonStringChannel(DsonChannel[str]):
    pass


@dataclass
class DsonImageChannel(DsonChannel[None]):
    def is_set(self):
        return self.has_image()


@dataclass
class DsonChannels:
    name: str
    type_id: str
    channels: dict[str, DsonChannel] = field(default_factory=dict)


@dataclass
class DsonObject:
    id: str
    label: str
    parent_id: str | None
    materials: list[DsonChannels] = field(default_factory=list)
    simulation: list[DsonChannels] = field(default_factory=list)


class DsonReader:
    max_content_dirs = 100

    def __init__(self):
        self.__content_dir_path_cache: dict[str, Path] = {}
        self.__geo_url_node_id_cache: dict[str, tuple[str, str, str | None]] = {}
        self.__material_shader_type_cache: dict[str, str] = {}

        # Initialize content libraries
        self.content_dirs = self._read_content_dirs_from_registry()

    def read_dson(self, daz_scene_file: PathLike) -> list[DsonObject]:
        dson = self._read_dson_file(daz_scene_file)
        scene_nodes = [n for n in dson["scene"]["nodes"] if "geometries" in n]

        return [
            DsonObject(
                id=n["id"],
                label=n["label"],
                parent_id=self._unquote_daz_ref(n["parent"]) if "parent" in n else None,
                materials=self._read_material_channels(n, dson),
                simulation=self._read_sim_modifiers(n, dson),
            ) for n in scene_nodes
        ]

    def _read_material_channels(self, scene_node: dict, dson: dict) -> list[DsonChannels]:
        scene_node_geo_ids = [g["id"] for g in scene_node["geometries"]]
        scene_mats = [
            m for m in dson['scene']['materials']
            if self._unquote_daz_ref(m["geometry"]) in scene_node_geo_ids
        ]
        materials: list[DsonChannels] = []

        for scene_mat in scene_mats:
            mat_library_id = self._unquote_daz_ref(scene_mat["url"])
            lib_mat = next((m for m in dson["material_library"] if m["id"] == mat_library_id), None)

            material = DsonChannels(
                name=scene_mat["groups"][0],
                type_id=self._find_shader_type(scene_mat, lib_mat),
            )

            materials.append(material)

            # 1st level channels
            for key, value in scene_mat.items():
                if isinstance(value, dict) and "channel" in value:
                    mat_id = slugify(key)
                    material.channels[mat_id] = self._map_channel(value["channel"])

            # Extra channels
            for mat_extra in scene_mat.get("extra", []):
                if mat_extra["type"] == "studio_material_channels":
                    for channel in mat_extra["channels"]:
                        mat_id = slugify(channel["channel"]["id"])
                        material.channels[mat_id] = self._map_channel(channel["channel"])

            # Material library channels
            if lib_mat:
                for mat_extra in lib_mat.get("extra", []):
                    if mat_extra["type"] == "studio_material_channels":
                        for channel in mat_extra["channels"]:
                            mat_id = slugify(channel["channel"]["id"])
                            if not mat_id in material.channels:
                                material.channels[mat_id] = self._map_channel(channel["channel"])

        return materials

    def _read_sim_modifiers(self, scene_node: dict, dson: dict) -> list[DsonChannels]:
        scene_node_geo_ids = [g["id"] for g in scene_node["geometries"]]
        scene_mods = [
            m for m in dson["scene"]["modifiers"]
            if "extra" in m and m["url"][0] == "#"  # Is local
               and m["extra"][0]["type"] == "studio/simulation_settings/dynamic_simulation"  # is sim
               and self._unquote_daz_ref(m["parent"]) in scene_node_geo_ids
        ]
        modifiers: list[DsonChannels] = []

        for scene_mod in scene_mods:
            mod_library_id = self._unquote_daz_ref(scene_mod["url"])
            lib_mod = next((m for m in dson["modifier_library"] if m["id"] == mod_library_id), None)

            modifier = DsonChannels(
                name=scene_mod["name"],
                type_id=self._find_modifier_type(scene_mod),
            )

            modifiers.append(modifier)

            # 1st level channels
            for key, value in scene_mod.items():
                if isinstance(value, dict) and "channel" in value:
                    mat_id = slugify(key)
                    modifier.channels[mat_id] = self._map_channel(value["channel"])

            # Extra channels
            for mod_extra in scene_mod.get("extra", []):
                if mod_extra["type"] == "studio_modifier_channels":
                    for channel in mod_extra["channels"]:
                        mat_id = slugify(channel["channel"]["id"])
                        modifier.channels[mat_id] = self._map_channel(channel["channel"])

            # Modifier library channels
            if lib_mod:
                for mat_extra in lib_mod.get("extra", []):
                    if mat_extra["type"] == "studio_modifier_channels":
                        for channel in mat_extra["channels"]:
                            mat_id = slugify(channel["channel"]["id"])
                            if not mat_id in modifier.channels:
                                modifier.channels[mat_id] = self._map_channel(channel["channel"])

        return modifiers

    @classmethod
    def _read_dson_file(cls, dson_file: PathLike) -> dict:
        with open(dson_file, 'rb') as f:
            file_header = f.read(2)

        # Check if the file is gzipped based on the magic number
        is_gzipped = file_header == b'\x1f\x8b'

        open_func = gzip.open if is_gzipped else open
        mode = 'rt' if is_gzipped else 'r'

        # Open once, load data
        with open_func(dson_file, mode, encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def _unquote_daz_ref(ref: str) -> str:
        if ref.startswith("#"):
            return urlparse.unquote(ref[1:])
        else:
            fragment_idx = ref.find('#') + 1
            return urlparse.unquote(ref[fragment_idx:])

    def _find_shader_type(self, scene_mat: dict, lib_mat: dict) -> str:
        url = scene_mat['url']

        # Try get from cache
        if url in self.__material_shader_type_cache:
            return self.__material_shader_type_cache[url]

        def _find_type():
            # Uses external DSF
            if url.startswith("/"):
                return slugify(self._unquote_daz_ref(url))

            # Try get from extra
            mat_extra = scene_mat.get('extra')
            if mat_extra and mat_extra[0]['type'] == 'studio/material/uber_iray':
                return "iray_uber"

            if lib_mat:
                if "type" in lib_mat:
                    return slugify(lib_mat["type"])

                lib_mat_extra = lib_mat.get('extra')
                if not lib_mat_extra:
                    return None

                if lib_mat_extra[0]['type'] == 'studio/material/uber_iray':
                    return "iray_uber"

                if lib_mat_extra[0]['type'] == 'studio/material/daz_brick':
                    return slugify(lib_mat['extra'][0]['brick_settings']['BrickSetup']['value']['BrickUserName'])

            return None

        mat_id = _find_type()
        if mat_id:
            self.__material_shader_type_cache[url] = mat_id
            return mat_id
        else:
            raise Exception(f'Unable to find shader type for url {url}.')

    @staticmethod
    def _find_modifier_type(scene_mod: dict) -> str:
        has_hairs_channel = next(
            (True
             for extra in scene_mod["extra"] if extra["type"] == "studio_modifier_channels"
             for ch in extra["channels"] if "PreRender Hairs" in ch["channel"]["id"]),
            False
        )

        return "dforce_hair" if has_hairs_channel else "dforce_sim"

    def _find_content_dir_path(self, path: str) -> Path | None:
        if path is None:
            return None
        if path in self.__content_dir_path_cache:
            return self.__content_dir_path_cache[path]
        for content_dir in self.content_dirs:
            decoded_path = urlparse.unquote(path[1:])
            cd_path = content_dir.joinpath(decoded_path)
            if cd_path.exists():
                self.__content_dir_path_cache[path] = cd_path
                return cd_path
        return None

    def _map_channel(self, c_data: dict) -> DsonChannel:
        raw_value = c_data.get("current_value")
        value_type = c_data['type']

        image_file = str(self._find_content_dir_path(c_data['image_file'])) if 'image_file' in c_data else None

        match value_type:
            case "float_color" | "color":
                raw_default_value = c_data.get("value", (0, 0, 0))
                return DsonColorChannel(
                    tuple(raw_value[:3]),
                    tuple(raw_default_value[:3]),
                    image_file)
            case "float":
                raw_default_value = c_data.get("value", 0.0)
                return DsonFloatChannel(float(raw_value), float(raw_default_value), image_file)
            case "bool":
                raw_default_value = c_data.get("value", False)
                return DsonBoolChannel(bool(raw_value), bool(raw_default_value), image_file)
            case "image":
                return DsonImageChannel(None, None, image_file or raw_value)
            case _:
                raw_default_value = c_data.get("value", "")
                return DsonStringChannel(str(raw_value), str(raw_default_value), image_file)

    @classmethod
    def _read_content_dirs_from_registry(cls) -> list[Path]:
        def enum_values(k):
            for i in range(cls.max_content_dirs):
                try:
                    yield winreg.EnumValue(k, i)
                except OSError:
                    break

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\DAZ\Studio4') as key:
            return [
                Path(value)
                for k, value, t in enum_values(key)
                if k.startswith('ContentDir') and t == winreg.REG_SZ
            ]
