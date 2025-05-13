import json
from os import path
from pathlib import Path

import bpy
from bpy.types import Operator
from bpy import path as bpath

from ..base import OperatorReportMixin
from ...properties import prefs_from_ctx, props_from_ctx
from ...utils.dson import DsonReader
from ...utils.json import DataclassJSONEncoder


class DebugExportMaterialsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.debug_export_materials_json"
    bl_label = "Export DAZ Materials as JSON"
    bl_description = """Convert Materials from DAZ Scene to "Intermediate Representation" and saves it as a JSON file.
The file will be saved in the same directory as this file, suffixed by ".materials-ir.json"."""

    @classmethod
    def poll(cls, context):
        # noinspection PyUnresolvedReferences
        props = props_from_ctx(context)
        return bpy.data.is_saved and props.has_scene_file_set()

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props = props_from_ctx(context)
        prefs = prefs_from_ctx(context)

        # Read and convert DAZ scene
        daz_save_file = Path(bpy.path.abspath(props.daz_scene_file))
        if not daz_save_file.exists():
            self.report_error(f"File {daz_save_file} does not exist")
            return {"CANCELLED"}

        dson_reader = DsonReader(prefs.content_libraries_as_paths())
        dson_scene_nodes = dson_reader.read_dson(daz_save_file)

        directory = path.dirname(bpy.data.filepath)
        output_name = f"{bpath.basename(str(daz_save_file))}.materials-ir.json"
        output_path = path.join(directory, output_name)

        with open(output_path, "w") as f:
            f.write(json.dumps(dson_scene_nodes, indent=2, cls=DataclassJSONEncoder))

        self.report_info(f"Exported materials to {output_path}!")
        return {"FINISHED"}
