from bpy.types import Operator

from ..base import OperatorReportMixin
from ...utils.dson import DsonCacheManager


class DebugClearSceneCacheOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.debug_clear_scene_cache"
    bl_label = "Clear Scene Cache"
    bl_description = "Delete scene cache files."

    def execute(self, context):
        DsonCacheManager.clear_cache()
        return {'FINISHED'}
