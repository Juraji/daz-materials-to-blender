from collections import defaultdict
from os import path, PathLike

import bpy

from .dson import DsonObject, DsonReader


class DsonIdConversionTable:
    def __init__(self, for_nodes: list[DsonObject]):
        self._table_dson_to_blender = {}
        self._table_blender_to_dson = {}
        suffix_groups = defaultdict(list)
        node_ids = [n.id for n in for_nodes]

        for node_id in node_ids:
            base, *suffix = node_id.rsplit('-', 1)
            if suffix and suffix[0].isdigit():
                suffix_groups[base].append(node_id)

        for base, variants in suffix_groups.items():
            offset = 1 if base in node_ids else 0
            for i, variant in enumerate(sorted(variants)):
                n = i + offset
                name = f"{base}.{n:03d}" if n > 0 else base
                self._table_dson_to_blender[variant] = name
                self._table_blender_to_dson[name] = variant

    def to_blender(self, dson_id: str) -> str:
        if dson_id in self._table_dson_to_blender:
            return self._table_dson_to_blender[dson_id]
        else:
            return dson_id

    def to_dson(self, dson_id: str) -> str:
        if dson_id in self._table_blender_to_dson:
            return self._table_blender_to_dson[dson_id]
        else:
            return dson_id


class DsonSceneData:
    @staticmethod
    def load_scene_data(dson_scene_path: PathLike) -> tuple[list[DsonObject], DsonIdConversionTable]:
        if not path.exists(dson_scene_path):
            raise DsonFileNotFoundException(f"File {dson_scene_path} does not exist")

        dson_reader = DsonReader()
        dson_scene_nodes = dson_reader.read_dson(dson_scene_path)
        dson_id_conversion_table = DsonIdConversionTable(dson_scene_nodes)

        dns = bpy.app.driver_namespace
        dns["dson_scene_nodes"] = dson_scene_nodes
        dns["dson_id_conversion_table"] = dson_id_conversion_table

        return dson_scene_nodes, dson_id_conversion_table

    @staticmethod
    def has_scene_data():
        dns = bpy.app.driver_namespace
        return "dson_scene_nodes" in dns

    @classmethod
    def get_scene_data(cls) -> tuple[list[DsonObject], DsonIdConversionTable]:
        if not cls.has_scene_data():
            raise Exception("No scene data cached!")

        dns = bpy.app.driver_namespace
        return dns["dson_scene_nodes"], dns["dson_id_conversion_table"]


class DsonFileNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
