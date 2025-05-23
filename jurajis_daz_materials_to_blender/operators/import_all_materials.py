from pathlib import Path

import bpy
from bpy.types import Operator, Context

from .base import OperatorReportMixin
from ..properties import MaterialImportProperties, props_from_ctx, prefs_from_ctx
from ..utils.dson_scene_data import DsonSceneData, DsonFileNotFoundException


class ImportAllMaterialsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.import_all_materials"
    bl_label = "Import All Materials"
    bl_description = "Import Materials from DAZ for all objects."
    bl_options = {"REGISTER", "BLOCKING"}

    @classmethod
    def poll(cls, context: Context):
        props: MaterialImportProperties = props_from_ctx(context)
        return props.has_scene_file_set()

    def execute(self, context: Context):
        props: MaterialImportProperties = props_from_ctx(context)

        try:
            prefs = prefs_from_ctx(context)
            daz_save_file = Path(bpy.path.abspath(props.daz_scene_file))
            dson_scene_nodes, dson_id_conversion_table = DsonSceneData.load_scene_data(daz_save_file, prefs)
            self.report_info(f"Found {len(dson_scene_nodes)} objects in {daz_save_file}!")
        except DsonFileNotFoundException as e:
            self.report_error(e.message)
            return {"CANCELLED"}

        # Copy current selection and deselect everything
        prev_selection = context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        mesh_objects = [obj for obj in context.scene.objects if obj.type == 'MESH']

        for obj in mesh_objects:
            obj.select_set(True)

        # noinspection PyUnresolvedReferences
        bpy.ops.daz_import.import_object_materials(use_cached_scene_data=True)

        for obj in mesh_objects:
            if obj not in prev_selection:
                obj.select_set(False)

        return {"FINISHED"}
