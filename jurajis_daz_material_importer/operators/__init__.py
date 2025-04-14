def register():
    import bpy
    from .import_materials import ImportMaterialsOperator
    from .create_shader_groups import CreateShaderGroupsOperator

    bpy.utils.register_class(ImportMaterialsOperator)
    bpy.utils.register_class(CreateShaderGroupsOperator)


def unregister():
    import bpy
    from .import_materials import ImportMaterialsOperator
    from .create_shader_groups import CreateShaderGroupsOperator

    bpy.utils.unregister_class(ImportMaterialsOperator)
    bpy.utils.unregister_class(CreateShaderGroupsOperator)

    try:
        # noinspection PyUnresolvedReferences
        del bpy.types.Scene.daz_import__material_import_properties
    except:
        pass
