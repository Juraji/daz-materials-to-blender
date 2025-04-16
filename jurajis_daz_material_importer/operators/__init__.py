def register():
    import bpy
    from .import_materials import ImportMaterialsOperator
    from .create_shader_group import CreateShaderGroupOperator

    bpy.utils.register_class(ImportMaterialsOperator)
    bpy.utils.register_class(CreateShaderGroupOperator)


def unregister():
    import bpy
    from .import_materials import ImportMaterialsOperator
    from .create_shader_group import CreateShaderGroupOperator

    bpy.utils.unregister_class(ImportMaterialsOperator)
    bpy.utils.unregister_class(CreateShaderGroupOperator)

    try:
        # noinspection PyUnresolvedReferences
        del bpy.types.Scene.daz_import__material_import_properties
    except:
        pass
