import bpy
from bpy.types import Operator, Context

from ..base import OperatorReportMixin
from ...properties import props_from_ctx


class ImportAllMaterialsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.import_all_materials"
    bl_label = "Import All Materials"
    bl_description = "Import Materials from DAZ for all objects."
    bl_options = {"REGISTER", "BLOCKING"}

    @classmethod
    def poll(cls, context: Context):
        props = props_from_ctx(context)
        return props.has_scene_file_set()

    def execute(self, context: Context):
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
