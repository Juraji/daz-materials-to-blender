from bpy.props import IntProperty
from bpy.types import Operator, Context

from ...properties import prefs_from_ctx


class PrefsRemoveLibraryOperator(Operator):
    bl_idname = "daz_import.prefs_remove_library_path"
    bl_label = "Remove Library Path"

    index: IntProperty()

    def execute(self, context: Context):
        prefs = prefs_from_ctx(context)
        if 0 <= self.index < len(prefs.content_libraries):
            prefs.content_libraries.remove(self.index)
        return {'FINISHED'}
