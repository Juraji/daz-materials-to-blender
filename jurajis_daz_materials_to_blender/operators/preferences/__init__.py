from .prefs_add_library_operator import PrefsAddLibraryOperator
from .prefs_remove_library_operator import PrefsRemoveLibraryOperator
from .prefs_win_detect_daz_libraries import PrefsWinDetectDazLibraries


def register():
    from bpy.utils import register_class

    register_class(PrefsAddLibraryOperator)
    register_class(PrefsRemoveLibraryOperator)
    register_class(PrefsWinDetectDazLibraries)


def unregister():
    from bpy.utils import unregister_class

    unregister_class(PrefsAddLibraryOperator)
    unregister_class(PrefsRemoveLibraryOperator)
    unregister_class(PrefsWinDetectDazLibraries)
