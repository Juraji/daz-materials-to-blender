from .clear_scene_cache import DebugClearSceneCacheOperator
from .delete_all_groups import DebugDeleteAllGroupsOperator


def register():
    from bpy.utils import register_class

    register_class(DebugClearSceneCacheOperator)
    register_class(DebugDeleteAllGroupsOperator)


def unregister():
    from bpy.utils import unregister_class

    unregister_class(DebugClearSceneCacheOperator)
    unregister_class(DebugDeleteAllGroupsOperator)
