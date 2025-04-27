def register():
    import bpy
    from .import_materials import ImportMaterialsPanel3D, ImportMaterialsPanelShaderEditor

    bpy.utils.register_class(ImportMaterialsPanel3D)
    bpy.utils.register_class(ImportMaterialsPanelShaderEditor)


def unregister():
    import bpy
    from .import_materials import ImportMaterialsPanel3D, ImportMaterialsPanelShaderEditor

    bpy.utils.unregister_class(ImportMaterialsPanel3D)
    bpy.utils.unregister_class(ImportMaterialsPanelShaderEditor)
