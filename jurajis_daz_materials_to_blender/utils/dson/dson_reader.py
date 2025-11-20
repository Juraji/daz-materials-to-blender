import gzip
import json
import os
from collections import defaultdict
from os import PathLike, path
from pathlib import Path
from urllib import parse as urlparse

from .dson_data import DsonCoordinate, DsonChannel, DsonColorChannel, DsonFloatChannel, DsonBoolChannel, \
    DsonStringChannel, DsonImageChannel, DsonChannels, DsonObjectInstance, DsonObject, DsonData
from ..math import tuple_zip_sum, tuple_zip_prod, tuple_mod, tuple_prod
from ..slugify import slugify


class DsonReader:
    def __init__(self, content_dirs: list[Path]):
        self.__content_dir_path_cache: dict[str, Path] = {}
        self.__material_shader_type_cache: dict[str, str] = {}
        self.__content_dirs = content_dirs

    def read_dson(self, daz_scene_file: PathLike | str) -> DsonData:
        dson = self._read_dson_file(daz_scene_file)
        scene_nodes = [n for n in dson["scene"]["nodes"] if "geometries" in n]

        dson_objects = []

        for scene_node in scene_nodes:
            n_base_rot, n_base_trans, n_base_scale = self._find_transforms_recursive(scene_node, None, dson)

            # noinspection PyTypeChecker
            dson_objects.append(DsonObject(
                id=scene_node["id"].strip(),
                label=scene_node["label"],
                origin=tuple(scene_node["preview"]["center_point"]) if "preview" in scene_node else (0, 0, 0),
                rotation=n_base_rot,
                translation=n_base_trans,
                scale=n_base_scale,
                parent_id=self._unquote_daz_ref(scene_node["parent"]) if "parent" in scene_node else None,
                materials=self._read_material_channels(scene_node, dson),
                instances=self._read_instances(scene_node, dson)
            ))

        dson_to_blender, blender_to_dson = self._create_conversion_tables(dson_objects)

        return DsonData(
            objects=dson_objects,
            dson_to_blender=dson_to_blender,
            blender_to_dson=blender_to_dson,
        )

    def _read_material_channels(self, scene_node: dict, dson: dict) -> list[DsonChannels]:
        scene_node_geo_ids = [g["id"] for g in scene_node["geometries"]]
        scene_mats = [
            m for m in dson['scene']['materials']
            if self._unquote_daz_ref(m["geometry"]) in scene_node_geo_ids
        ]
        materials: list[DsonChannels] = []
        # TODO: If node is a geo shell, check which material groups should not be exported

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

    def _read_instances(self, node: dict, dson: dict) -> list[DsonObjectInstance]:
        if not "node_library" in dson:
            # Scene does not contain a node library. Might be a scene subset.
            return []

        scene_nodes = dson["scene"]["nodes"]
        node_library = dson["node_library"]
        instance_scene_nodes = [
            n for n in scene_nodes
            if "extra" in n
               and n["extra"][0]["type"] == "studio/node/instance"
               and self._unquote_daz_ref(n["extra"][1]["channels"][0]["channel"]["node"]) == node["id"]
        ]

        if len(instance_scene_nodes) == 0:
            return []

        instances: list[DsonObjectInstance] = []
        for instance in instance_scene_nodes:
            lib_node = self._find_entry_by_url(node_library, instance["url"])

            if not lib_node:
                continue

            instance_rotation, instance_translation, instance_scale = \
                self._find_transforms_recursive(instance, lib_node, dson)
            instance_rotation = tuple_mod(instance_rotation, 360.0)
            instance_origin = self._read_point_axis(lib_node, "center_point", 0.0)

            # noinspection PyTypeChecker
            instances.append(DsonObjectInstance(
                id=slugify(instance["id"]),
                label=instance["label"],
                origin=instance_origin,
                rotation=instance_rotation,
                translation=instance_translation,
                scale=instance_scale
            ))

        return instances

    @classmethod
    def _find_entry_by_url(cls, library: list[dict], url: str):
        ref = cls._unquote_daz_ref(url)
        return next((entry for entry in library if entry["id"] == ref), None)

    @classmethod
    def _find_transforms_recursive(cls,
                                   node: dict,
                                   lib_node: dict | None,
                                   dson: dict) -> tuple[DsonCoordinate, DsonCoordinate, DsonCoordinate]:
        if "geometries" in node:
            n_rot = cls._read_point_axis(node, "rotation", 0.0)
            n_trans = cls._read_point_axis(node, "translation", 0.0)

            sn_gscale = node["general_scale"]["current_value"] if "general_scale" in node else 1.0
            n_scale = tuple_prod(cls._read_point_axis(node, "scale", 1.0), sn_gscale)
        elif lib_node:
            n_rot = tuple(v["current_value"] for v in lib_node["rotation"])
            n_trans = tuple(v["current_value"] for v in lib_node["translation"])
            ln_gscale = lib_node["general_scale"]["current_value"]
            n_scale = tuple(v["current_value"] * ln_gscale for v in lib_node["scale"])
        else:
            n_rot = (0, 0, 0)
            n_trans = (0, 0, 0)
            n_scale = (1.0, 1.0, 1.0)

        if "parent" in node and "node_library" in dson:
            p_scene_node = cls._find_entry_by_url(dson["scene"]["nodes"], node["parent"])
            if p_scene_node:
                p_lib_node = cls._find_entry_by_url(dson["node_library"], p_scene_node["url"])
                p_rot, p_trans, p_scale = cls._find_transforms_recursive(p_scene_node, p_lib_node, dson)

                n_rot = tuple_zip_sum(n_rot, p_rot)
                n_trans = tuple_zip_sum(n_trans, p_trans)
                n_scale = tuple_zip_prod(n_scale, p_scale)

        return n_rot, n_trans, n_scale

    @staticmethod
    def _read_point_axis(node: dict, prop_name: str, default: float) -> DsonCoordinate:
        prop = node.get(prop_name, [])
        return next((v["current_value"] for v in prop if v["id"] == "x"), default), \
            next((v["current_value"] for v in prop if v["id"] == "y"), default), \
            next((v["current_value"] for v in prop if v["id"] == "z"), default)

    @classmethod
    def _read_dson_file(cls, dson_file: PathLike | str) -> dict:
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
            if mat_extra:
                mat_type = mat_extra[0]['type']
                if mat_type != 'studio/material/daz_brick':
                    # For daz_brick we need to check the lib mat!
                    return mat_extra[0]['type'][16:]

            if lib_mat:
                if "type" in lib_mat:
                    return slugify(lib_mat["type"].replace("studio/material/", ""))

                lib_mat_extra = lib_mat.get('extra')
                if not lib_mat_extra:
                    return None

                mat_type = lib_mat_extra[0]['type']
                if mat_type == 'studio/material/daz_brick':
                    return slugify(lib_mat_extra[0]['brick_settings']['BrickSetup']['value']['BrickUserName'])
                else:
                    return slugify(lib_mat_extra[0].replace("studio/material/", ""))

            return None

        mat_id = _find_type()
        if mat_id:
            self.__material_shader_type_cache[url] = mat_id
            return mat_id
        else:
            raise Exception(f'Unable to find shader type for url "{url}".')

    @staticmethod
    def _find_modifier_type(scene_mod: dict) -> str:
        has_hairs_channel = next(
            (True
             for extra in scene_mod["extra"] if extra["type"] == "studio_modifier_channels"
             for ch in extra["channels"] if "PreRender Hairs" in ch["channel"]["id"]),
            False
        )

        return "dforce_hair" if has_hairs_channel else "dforce_sim"

    @staticmethod
    def _resolve_real_path(base: Path, raw_path: str) -> Path | None:
        decoded = urlparse.unquote(raw_path.lstrip(path.sep))
        candidate = base / decoded

        if candidate.exists():
            return candidate

        # slow path: resolve with case-insensitive lookup
        parts = decoded.split(path.sep)
        current = base

        for part in parts:
            found = None
            try:
                with os.scandir(current) as it:
                    for entry in it:
                        if entry.name.lower() == part.lower():
                            found = Path(entry.path)
                            break
            except (PermissionError, FileNotFoundError):
                return None

            if not found:
                return None
            current = found

        return current

    def _resolve_content_dir_path(self, raw_path: str) -> Path | None:
        if raw_path is None:
            return None

        if raw_path in self.__content_dir_path_cache:
            return self.__content_dir_path_cache[raw_path]

        for content_dir in self.__content_dirs:
            cd_path = self._resolve_real_path(content_dir, raw_path)
            if not cd_path is None:
                self.__content_dir_path_cache[raw_path] = cd_path
                return cd_path

        return None

    def _map_channel(self, c_data: dict) -> DsonChannel:
        raw_value = c_data.get("current_value")
        value_type = c_data['type']

        image_file = None
        raw_path = c_data.get("image_file")
        if raw_path is not None:
            resolved = self._resolve_content_dir_path(raw_path)
            if resolved:
                image_file = str(resolved)

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

    @staticmethod
    def _create_conversion_tables(dson_objects: list[DsonObject]) -> tuple[dict[str, str], dict[str, str]]:
        dson_to_blender = {}
        blender_to_dson = {}
        suffix_groups = defaultdict(list)
        node_ids = [n.id for n in dson_objects]

        for node_id in node_ids:
            base, *suffix = node_id.rsplit('-', 1)
            if suffix and suffix[0].isdigit():
                suffix_groups[base].append(node_id)
            else:
                suffix_groups[base].append(node_id)

        for base, variants in suffix_groups.items():
            base = base.replace(' ', '_')
            offset = 1 if base in node_ids else 0
            for i, variant in enumerate(sorted(variants)):
                n = i + offset
                name = f"{base}.{n:03d}" if n > 0 else base
                dson_to_blender[variant] = name
                blender_to_dson[name] = variant

        return dson_to_blender, blender_to_dson
