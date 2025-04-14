import gzip
import json
import winreg
from os import PathLike
from pathlib import Path
from typing import Dict, List
from urllib import parse as urlparse

def _get_daz_content_dirs() -> List[Path]:
    location = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\DAZ\Studio4', 0, winreg.KEY_READ)
    key_prefix = 'ContentDir'

    with location as location_key:
        content_dirs = []
        index = 0
        while True:
            try:
                key, value, v_type = winreg.EnumValue(location_key, index)
                if v_type == winreg.REG_SZ and key.startswith(key_prefix):
                    content_dirs.append(Path(value))
                index += 1
            except OSError:
                break

        return content_dirs


def _read_dson_file(dson_file: PathLike) -> Dict:
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


def read_daz_save_into_mats_per_object(daz_scene_file: Path) -> Dict:
    daz_content_dirs = _get_daz_content_dirs()
    cd_path_cache: dict[str, Path] = {}
    geo_url_node_id_cache: dict[str, tuple[str, str, str | None]] = {}
    material_shader_type_cache: dict[str, str] = {}

    dson_data = _read_dson_file(daz_scene_file)
    scene_nodes = dson_data['scene']['nodes']
    scene_materials = dson_data['scene']['materials']
    material_library = dson_data['material_library']

    def find_node_by_geo_url(geo_url: str) -> tuple[str, str, str | None]:
        if geo_url in geo_url_node_id_cache:
            return geo_url_node_id_cache[geo_url]

        geo_id = urlparse.unquote(geo_url[1:])  # Remove leading '#'
        for scene_node in scene_nodes:
            if 'geometries' in scene_node:
                for geometry in scene_node['geometries']:
                    if geometry['id'] == geo_id:
                        scene_node_id = scene_node['id']
                        scene_node_label = scene_node['label']
                        scene_node_parent = urlparse.unquote(scene_node['parent'][1:]) \
                            if 'parent' in scene_node else None

                        geo_url_node_id_cache[geo_url] = (scene_node_id, scene_node_label, scene_node_parent)
                        return scene_node_id, scene_node_label, scene_node_parent
        raise Exception('No geometries found in scene node for url {}'.format(geo_url))

    def find_shader_type(material_url: str, type_ref: str) -> str:
        if type_ref == 'studio/material/uber_iray':
            return "iray_uber"

        if material_url in material_shader_type_cache:
            return material_shader_type_cache[material_url]

        if material_url.startswith("/"):  # Content Library url
            fragment_idx = material_url.find('#')
            mat_id = material_url[fragment_idx + 1:].lower()
            material_shader_type_cache[material_url] = mat_id
            return mat_id

        if material_url.startswith('#'):  # material library reference
            material_id = urlparse.unquote(material_url[1:])  # Remove leading '#'
            for mat in material_library:
                if mat['id'] == material_id:
                    if mat['extra'][0]['type'] == 'studio/material/daz_brick':
                        shader_type = mat['extra'][0]['brick_settings']['BrickSetup']['value'][
                            'BrickUserName'].lower().replace(' ', '_')
                        material_shader_type_cache[material_url] = shader_type
                        return shader_type

        raise Exception(f'Unable to find shader type for url {material_url}.')

    def determine_content_dir_path(path: str) -> Path | None:
        if path is None:
            return None
        if path in cd_path_cache:
            return cd_path_cache[path]
        for content_dir in daz_content_dirs:
            decoded_path = urlparse.unquote(path[1:])
            cd_path = content_dir.joinpath(decoded_path)
            if cd_path.exists():
                cd_path_cache[path] = cd_path
                return cd_path

    def map_channel(c: dict) -> tuple[str, dict]:
        mat_id = c['id']
        raw_value = c['current_value'] if 'current_value' in c else c['value']
        value_type = c['type']

        if value_type == 'float_color' or value_type == 'color':
            converted_value = (*raw_value, 1.0)  # Blender uses RGBA colors (DAZ uses RGB)
        else:
            converted_value = raw_value

        image_file = str(determine_content_dir_path(c['image_file'])) if 'image_file' in c else None

        try:
            return mat_id, {
                'id': mat_id,
                'type': value_type,
                'value': converted_value,
                'image_file': image_file,
            }
        except Exception as e:
            print(f'Failed to map channel {mat_id} {c}')
            raise e

    mats_per_object = {}

    for mat_data in scene_materials:
        mat_name = mat_data['groups'][0].replace(' ', '_')
        node_id, node_label, node_parent_name = find_node_by_geo_url(mat_data['geometry'])

        if node_id not in mats_per_object:
            mats_per_object[node_id] = {
                'label': node_label,
                'parent_id': node_parent_name,
                'materials': {}
            }
        elif mat_name in mats_per_object[node_id]['materials']:
            continue

        channels = {}

        if 'diffuse' in mat_data:
            _, mapped_channel = map_channel(mat_data['diffuse']['channel'])
            channels['Diffuse'] = mapped_channel

        if len(mat_data['extra']) == 2:
            for channel in mat_data['extra'][1]['channels']:
                channel_id, mapped_channel = map_channel(channel['channel'])
                channels[channel_id.replace(' ', '_')] = mapped_channel

        mats_per_object[node_id]['materials'][mat_name] = {
            'type': find_shader_type(mat_data['url'], mat_data['extra'][0]['type']),
            'channels': channels
        }

    return mats_per_object
