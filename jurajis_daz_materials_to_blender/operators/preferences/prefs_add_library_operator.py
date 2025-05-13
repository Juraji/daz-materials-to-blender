from bpy.types import Operator

from ...properties import prefs_from_ctx


class PrefsAddLibraryOperator(Operator):
    bl_idname = "daz_import.prefs_add_library_path"
    bl_label = "Add Library Path"

    def execute(self, context):
        prefs = prefs_from_ctx(context)
        prefs.content_libraries.add()
        return {'FINISHED'}
