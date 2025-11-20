import bpy
from bpy.types import Operator, Context


class ClearCustomSplitNormalsOperator(Operator):
    bl_idname = "daz_import.clear_custom_split_normals"
    bl_label = "Clear Custom Split Normals"
    bl_description = "Clears custom split normals for all selected objects."

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context: Context):
        current_active_object = context.view_layer.objects.active

        for o in context.selected_objects:
            if o.type != "MESH":
                continue
            try:
                context.view_layer.objects.active = o
                bpy.ops.mesh.customdata_custom_splitnormals_clear()
                self.report({'INFO'}, f"Cleared custom split normals for {o.name}.")
            except:
                self.report({'INFO'}, f"{o.name} does not have custom split normals, skipped.")

        context.view_layer.objects.active = current_active_object
        return {'FINISHED'}
