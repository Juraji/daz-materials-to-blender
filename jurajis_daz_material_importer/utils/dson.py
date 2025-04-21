import gzip
import json
import winreg
from collections import defaultdict
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import Any
from urllib import parse as urlparse

from .slugify import slugify


@dataclass
class DsonMaterialChannel:
    id: str
    value: Any
    image_file: str | None

    def has_image(self) -> bool: return self.image_file is not None


@dataclass
class DsonColorMaterialChannel(DsonMaterialChannel):
    value: tuple[float, float, float]
    alpha: float = 1.0

    def as_rgba(self) -> tuple[float, float, float, float]:
        return self.value[0], self.value[1], self.value[2], self.alpha

    def as_float(self):
        return (sum(self.value) / 3) * self.alpha


@dataclass
class DsonFloatMaterialChannel(DsonMaterialChannel):
    value: float


@dataclass
class DsonBoolMaterialChannel(DsonMaterialChannel):
    value: bool


@dataclass
class DsonStringMaterialChannel(DsonMaterialChannel):
    value: str


@dataclass
class DsonImageMaterialChannel(DsonMaterialChannel):
    value: None


@dataclass
class DsonMaterial:
    material_name: str
    type_id: str
    channels: dict[str, DsonMaterialChannel]


@dataclass
class DsonSceneNode:
    id: str
    label: str
    parent_id: str | None
    materials: list[DsonMaterial] = field(default_factory=list)


class DazDsonMaterialReader:
    max_content_dirs = 100

    def __init__(self):
        self.__content_dir_path_cache: dict[str, Path] = {}
        self.__geo_url_node_id_cache: dict[str, tuple[str, str, str | None]] = {}
        self.__material_shader_type_cache: dict[str, str] = {}

        # Initialize content libraries
        self.content_dirs = self._read_content_dirs_from_reg()

    def read_materials(self, daz_scene_file: Path) -> list[DsonSceneNode]:
        dson = self._read_dson_file(daz_scene_file)
        scene_nodes = dson['scene']['nodes']
        scene_materials = dson['scene']['materials']
        material_library = dson['material_library']

        mats_per_object: dict[str, DsonSceneNode] = {}

        for scene_mat in scene_materials:
            mat_name = scene_mat['groups'][0].replace(' ', '_')
            node_id, node_label, node_parent = self._find_node_by_geo_url(scene_nodes, scene_mat['geometry'])

            lib_mat: dict | None = None
            if scene_mat['url'].startswith('#'):
                material_id = self._unquote_daz_ref(scene_mat['url'])
                lib_mat = next((m for m in material_library if m['id'] == material_id), None)

            mat_type = self._find_shader_type(scene_mat, lib_mat)
            node = mats_per_object.setdefault(node_id, DsonSceneNode(node_id, node_label, node_parent))

            if mat_name in node.materials:
                continue

            channels = {}

            if 'diffuse' in scene_mat:
                ch = self._map_channel(scene_mat['diffuse']['channel'])
                channels[ch.id] = ch

            # Map scene materials
            extra_channels = scene_mat.get('extra', [])
            if len(extra_channels) == 2:
                for ch_data in extra_channels[1]['channels']:
                    ch = self._map_channel(ch_data['channel'])
                    channels[ch.id] = ch

            # Map library materials if missing from scene material
            if lib_mat:
                lib_extra_channels = lib_mat.get('extra', [])
                if len(lib_extra_channels) == 2:
                    for ch_data in lib_extra_channels[1]['channels']:
                        ch = self._map_channel(ch_data['channel'])
                        if not ch.id in channels:
                            channels[ch.id] = ch

            node.materials.append(DsonMaterial(mat_name, mat_type, channels))

        return list(mats_per_object.values())

    @staticmethod
    def create_dson_id_conversion_table(nodes: list[DsonSceneNode]) -> dict[str, str]:
        """
        :param nodes: The result from read_materials
        :return: A dict of DAZ node id to expected node name in Blender.
        """
        conversion_table = {}
        suffix_groups = defaultdict(list)

        # Collect node IDs with suffixes
        for node in nodes:
            base, *suffix = node.id.rsplit('-', 1)
            if suffix and suffix[0].isdigit():
                suffix_groups[base].append(node.id)

        # Assign new names based on suffix groups
        for base, variants in suffix_groups.items():
            for i, variant in enumerate(sorted(variants)):
                conversion_table[variant] = f"{base}.{i + 1:03d}"

        return conversion_table

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

    def _find_node_by_geo_url(self, scene_nodes, geo_url: str) -> tuple[str, str, str | None]:
        if geo_url in self.__geo_url_node_id_cache:
            return self.__geo_url_node_id_cache[geo_url]

        geo_id = self._unquote_daz_ref(geo_url)

        for node in scene_nodes:
            geometries = node.get('geometries', [])
            if any(g['id'] == geo_id for g in geometries):
                scene_node_id = node['id']
                scene_node_label = node['label']
                scene_node_parent = None if not 'parent' in node else self._unquote_daz_ref(node['parent'])

                result = (scene_node_id, scene_node_label, scene_node_parent)
                self.__geo_url_node_id_cache[geo_url] = result
                return result

        raise Exception(f'No geometries found in scene node for url {geo_url}')

    def _find_shader_type(self, scene_mat: dict, lib_mat: dict) -> str:
        url = scene_mat['url']

        if url in self.__material_shader_type_cache:
            return self.__material_shader_type_cache[url]

        extra = scene_mat['extra']
        if extra[0]['type'] == 'studio/material/uber_iray':
            if len(extra) == 2:
                base_mixing = next((ch['channel']['current_value'] for ch in extra[1]['channels'] if
                                    ch['channel']['id'] == 'Base Mixing'), 0)
                match base_mixing:
                    case 1:
                        mat_id = "iray_uber__pbr_sg"
                    case 2:
                        mat_id = "iray_uber__weighted"
                    case _:
                        mat_id = "iray_uber__pbr_mr"
            else:
                mat_id = "iray_uber__pbr_mr"

            self.__material_shader_type_cache[url] = mat_id
            return mat_id

        if url.startswith("/"):
            mat_id = slugify(self._unquote_daz_ref(url))
            self.__material_shader_type_cache[url] = mat_id
            return mat_id

        if lib_mat and scene_mat['extra'][0]['type'] == 'studio/material/daz_brick':
            shader_type = slugify(lib_mat['extra'][0]['brick_settings']['BrickSetup']['value']['BrickUserName'])
            self.__material_shader_type_cache[url] = shader_type
            return shader_type

        raise Exception(f'Unable to find shader type for url {url}.')

    def _determine_content_dir_path(self, path: str) -> Path | None:
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

    def _map_channel(self, c: dict) -> DsonMaterialChannel:
        mat_id = slugify(c['id'])
        raw_value = c.get("current_value") or c.get("value")
        value_type = c['type']

        image_file = str(self._determine_content_dir_path(c['image_file'])) if 'image_file' in c else None

        if value_type == "float_color" or value_type == "color":
            dson_channel = DsonColorMaterialChannel(mat_id, (raw_value[0], raw_value[1], raw_value[2]), image_file)
        elif value_type == "float":
            dson_channel = DsonFloatMaterialChannel(mat_id, raw_value, image_file)
        elif value_type == "bool":
            dson_channel = DsonBoolMaterialChannel(mat_id, raw_value, image_file)
        elif value_type == "image":
            dson_channel = DsonImageMaterialChannel(mat_id, None, image_file or raw_value)
        else:
            dson_channel = DsonStringMaterialChannel(mat_id, str(raw_value), image_file)

        return dson_channel

    @classmethod
    def _read_content_dirs_from_reg(cls) -> list[Path]:
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
