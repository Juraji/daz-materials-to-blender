def register():
    import bpy
    from .import_materials import ImportMaterialsOperator
    from .create_shader_group import CreateShaderGroupOperator
    from .debug.export_materials import DebugExportMaterialsOperator
    from .debug.delete_all_groups import DebugDeleteAllGroupsOperator

    bpy.utils.register_class(ImportMaterialsOperator)
    bpy.utils.register_class(CreateShaderGroupOperator)
    bpy.utils.register_class(DebugExportMaterialsOperator)
    bpy.utils.register_class(DebugDeleteAllGroupsOperator)


def unregister():
    import bpy
    from .import_materials import ImportMaterialsOperator
    from .create_shader_group import CreateShaderGroupOperator
    from .debug.export_materials import DebugExportMaterialsOperator
    from .debug.delete_all_groups import DebugDeleteAllGroupsOperator

    bpy.utils.unregister_class(ImportMaterialsOperator)
    bpy.utils.unregister_class(CreateShaderGroupOperator)
    bpy.utils.unregister_class(DebugDeleteAllGroupsOperator)

    try:
        # noinspection PyUnresolvedReferences
        del bpy.types.Scene.daz_import__material_import_properties
    except:
        pass
