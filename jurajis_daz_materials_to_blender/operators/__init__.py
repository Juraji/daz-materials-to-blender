def register():
    import bpy
    from .import_all_materials import ImportAllMaterialsOperator
    from .import_object_materials import ImportObjectMaterialsOperator
    from .import_shader_group import ImportShaderGroupOperator
    from .debug.export_materials import DebugExportMaterialsOperator
    from .debug.delete_all_groups import DebugDeleteAllGroupsOperator

    bpy.utils.register_class(ImportAllMaterialsOperator)
    bpy.utils.register_class(ImportObjectMaterialsOperator)
    bpy.utils.register_class(ImportShaderGroupOperator)
    bpy.utils.register_class(DebugExportMaterialsOperator)
    bpy.utils.register_class(DebugDeleteAllGroupsOperator)


def unregister():
    import bpy
    from .import_all_materials import ImportAllMaterialsOperator
    from .import_object_materials import ImportObjectMaterialsOperator
    from .import_shader_group import ImportShaderGroupOperator
    from .debug.export_materials import DebugExportMaterialsOperator
    from .debug.delete_all_groups import DebugDeleteAllGroupsOperator

    bpy.utils.unregister_class(ImportAllMaterialsOperator)
    bpy.utils.unregister_class(ImportObjectMaterialsOperator)
    bpy.utils.unregister_class(ImportShaderGroupOperator)
    bpy.utils.unregister_class(DebugExportMaterialsOperator)
    bpy.utils.unregister_class(DebugDeleteAllGroupsOperator)
