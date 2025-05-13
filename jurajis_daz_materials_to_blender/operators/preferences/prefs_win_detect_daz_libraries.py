import sys

from bpy.props import IntProperty
from bpy.types import Operator, Context

from ...properties import prefs_from_ctx


class PrefsWinDetectDazLibraries(Operator):
    bl_idname = "daz_import.prefs_win_detect_daz_libraries"
    bl_label = "Auto-Detect"

    max_content_dirs: IntProperty(default=20)

    @classmethod
    def poll(cls, context):
        return sys.platform == "win32"

    def execute(self, context: Context):
        prefs = prefs_from_ctx(context)

        if sys.platform != "win32":
            self.report({'WARNING'}, "Auto-detect only works on Windows.")
            return {'CANCELLED'}

        content_dirs = self.read_content_dirs_from_registry(self.max_content_dirs)

        if content_dirs:
            prefs.content_libraries.clear()
            for content_dir in content_dirs:
                item = prefs.content_libraries.add()
                item.path = content_dir
        return {'FINISHED'}

    @staticmethod
    def read_content_dirs_from_registry(max_content_dirs: int) -> list[str]:
        import winreg

        def enum_values(k):
            for i in range(max_content_dirs):
                try:
                    yield winreg.EnumValue(k, i)
                except OSError:
                    break

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\DAZ\Studio4') as key:
            return [
                value
                for k, value, t in enum_values(key)
                if k.startswith('ContentDir') and t == winreg.REG_SZ
            ]
