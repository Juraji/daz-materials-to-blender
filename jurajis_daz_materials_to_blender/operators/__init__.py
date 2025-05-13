def register():
    import bpy
    from .import_all_materials import ImportAllMaterialsOperator
    from .import_object_materials import ImportObjectMaterialsOperator
    from .import_shader_group import ImportShaderGroupOperator
    from .create_instances import CreateInstancesOperator
    from .convert_materials import ConvertMaterialsOperator, MaterialItem
    from .debug.export_materials import DebugExportMaterialsOperator
    from .debug.delete_all_groups import DebugDeleteAllGroupsOperator
    from .preferences.prefs_add_library_operator import PrefsAddLibraryOperator
    from .preferences.prefs_remove_library_operator import PrefsRemoveLibraryOperator
    from .preferences.prefs_win_detect_daz_libraries import PrefsWinDetectDazLibraries

    bpy.utils.register_class(ImportAllMaterialsOperator)
    bpy.utils.register_class(ImportObjectMaterialsOperator)
    bpy.utils.register_class(ImportShaderGroupOperator)
    bpy.utils.register_class(CreateInstancesOperator)
    bpy.utils.register_class(MaterialItem)
    bpy.utils.register_class(ConvertMaterialsOperator)
    bpy.utils.register_class(DebugExportMaterialsOperator)
    bpy.utils.register_class(DebugDeleteAllGroupsOperator)
    bpy.utils.register_class(PrefsAddLibraryOperator)
    bpy.utils.register_class(PrefsRemoveLibraryOperator)
    bpy.utils.register_class(PrefsWinDetectDazLibraries)


def unregister():
    import bpy
    from .import_all_materials import ImportAllMaterialsOperator
    from .import_object_materials import ImportObjectMaterialsOperator
    from .import_shader_group import ImportShaderGroupOperator
    from .create_instances import CreateInstancesOperator
    from .convert_materials import ConvertMaterialsOperator, MaterialItem
    from .debug.export_materials import DebugExportMaterialsOperator
    from .debug.delete_all_groups import DebugDeleteAllGroupsOperator
    from .preferences.prefs_add_library_operator import PrefsAddLibraryOperator
    from .preferences.prefs_remove_library_operator import PrefsRemoveLibraryOperator
    from .preferences.prefs_win_detect_daz_libraries import PrefsWinDetectDazLibraries

    bpy.utils.unregister_class(ImportAllMaterialsOperator)
    bpy.utils.unregister_class(ImportObjectMaterialsOperator)
    bpy.utils.unregister_class(ImportShaderGroupOperator)
    bpy.utils.unregister_class(CreateInstancesOperator)
    bpy.utils.unregister_class(MaterialItem)
    bpy.utils.unregister_class(ConvertMaterialsOperator)
    bpy.utils.unregister_class(DebugExportMaterialsOperator)
    bpy.utils.unregister_class(DebugDeleteAllGroupsOperator)
    bpy.utils.unregister_class(PrefsAddLibraryOperator)
    bpy.utils.unregister_class(PrefsRemoveLibraryOperator)
    bpy.utils.unregister_class(PrefsWinDetectDazLibraries)
