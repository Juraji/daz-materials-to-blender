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

    def __init__(self):
        self.__content_dir_path_cache: dict[str, Path] = {}
        self.__geo_url_node_id_cache: dict[str, tuple[str, str, str | None]] = {}
        self.__material_shader_type_cache: dict[str, str] = {}

        # Initialize content libraries
        self.content_dirs = self._read_content_dirs_from_reg()

    def read_materials(self, daz_scene_file: Path) -> list[DsonSceneNode]:
        dson_data = self._read_dson_file(daz_scene_file)
        scene_nodes = dson_data['scene']['nodes']
        scene_materials = dson_data['scene']['materials']
        material_library = dson_data['material_library']

        mats_per_object: dict[str, DsonSceneNode] = {}

        for mat_data in scene_materials:
            mat_name = mat_data['groups'][0].replace(' ', '_')
            node_id, node_label, node_parent_name = self._find_node_by_geo_url(scene_nodes, mat_data['geometry'])
            mat_type = self._find_shader_type(material_library, mat_data['url'], mat_data['extra'][0]['type'])

            if node_id not in mats_per_object:
                mats_per_object[node_id] = DsonSceneNode(node_id, node_label, node_parent_name)
            elif mat_name in mats_per_object[node_id].materials:
                continue

            channels: dict[str, DsonMaterialChannel] = {}

            if 'diffuse' in mat_data:
                mapped_channel = self._map_channel(mat_data['diffuse']['channel'])
                channels[mapped_channel.id] = mapped_channel

            if len(mat_data['extra']) == 2:
                for channel in mat_data['extra'][1]['channels']:
                    mapped_channel = self._map_channel(channel['channel'])
                    channels[mapped_channel.id] = mapped_channel

            mats_per_object[node_id].materials.append(DsonMaterial(mat_name, mat_type, channels))

        return [*mats_per_object.values()]

    @staticmethod
    def create_dson_id_conversion_table(nodes: list[DsonSceneNode]) -> dict[str, str]:
        """
        :param nodes: The result from read_materials
        :return: A dict of DAZ node id to expected node name in Blender.
        """
        node_ids = map(lambda x: x.id, nodes)
        conversion_table = {}
        suffix_groups = defaultdict(list)

        for name in node_ids:
            if "-" in name:
                base_part, suffix_part = name.rsplit('-', 1)
                if suffix_part.isdigit():
                    suffix_groups[base_part].append(name)
                    continue

        for base, variants in suffix_groups.items():
            for i, variant in enumerate(sorted(variants)):
                new_suffix = f"{i + 1:03d}"
                conversion_table[variant] = f"{base}.{new_suffix}"

        return conversion_table

    @classmethod
    def _read_dson_file(cls, dson_file: PathLike) -> dict:
        # Check if the file starts with the GZIP magic number (0x1f, 0x8b)
        with open(dson_file, 'rb') as f:
            file_header = f.read(2)

        is_gzipped = file_header == b'\x1f\x8b'

        if is_gzipped:
            with gzip.open(dson_file, 'rt', encoding='utf-8') as f:
                data = json.load(f)
        else:
            with open(dson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        return data

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
        for scene_node in scene_nodes:
            if 'geometries' in scene_node:
                for geometry in scene_node['geometries']:
                    if geometry['id'] == geo_id:
                        scene_node_id = scene_node['id']
                        scene_node_label = scene_node['label']

                        if 'parent' in scene_node:
                            scene_node_parent = self._unquote_daz_ref(scene_node['parent'])
                        else:
                            scene_node_parent = None

                        self.__geo_url_node_id_cache[geo_url] = (scene_node_id, scene_node_label, scene_node_parent)
                        return scene_node_id, scene_node_label, scene_node_parent
        raise Exception('No geometries found in scene node for url {}'.format(geo_url))

    def _find_shader_type(self, material_library, material_url: str, type_ref: str) -> str:
        if type_ref == 'studio/material/uber_iray':
            return "iray_uber"

        if material_url in self.__material_shader_type_cache:
            return self.__material_shader_type_cache[material_url]

        if material_url.startswith("/"):  # Content Library url
            mat_id = slugify(self._unquote_daz_ref(material_url))
            self.__material_shader_type_cache[material_url] = mat_id
            return mat_id

        if material_url.startswith('#'):  # material library reference
            material_id = slugify(self._unquote_daz_ref(material_url))
            for mat in material_library:
                if mat['id'] == material_id:
                    if mat['extra'][0]['type'] == 'studio/material/daz_brick':
                        shader_type = slugify(mat['extra'][0]['brick_settings']['BrickSetup']['value']['BrickUserName'])
                        self.__material_shader_type_cache[material_url] = shader_type
                        return shader_type

        raise Exception(f'Unable to find shader type for url {material_url}.')

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
        raw_value = c['current_value'] if 'current_value' in c else c['value']
        value_type = c['type']

        image_file = str(self._determine_content_dir_path(c['image_file'])) if 'image_file' in c else None

        if value_type == "float_color" or value_type == "color":
            dson_channel = DsonColorMaterialChannel(mat_id, (raw_value[0], raw_value[1], raw_value[2]), image_file)
        elif value_type == "float":
            dson_channel = DsonFloatMaterialChannel(mat_id, raw_value, image_file)
        elif value_type == "bool":
            dson_channel = DsonBoolMaterialChannel(mat_id, raw_value, image_file)
        else:
            dson_channel = DsonStringMaterialChannel(mat_id, str(raw_value), image_file)

        return dson_channel

    @staticmethod
    def _read_content_dirs_from_reg() -> list[Path]:
        location = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\DAZ\Studio4', 0, winreg.KEY_READ)
        key_prefix = 'ContentDir'
        dirs = []

        with location as location_key:
            index = 0
            while True:
                try:
                    key, value, v_type = winreg.EnumValue(location_key, index)
                    if v_type == winreg.REG_SZ and key.startswith(key_prefix):
                        dirs.append(Path(value))
                    index += 1
                except OSError:
                    break

        return dirs
