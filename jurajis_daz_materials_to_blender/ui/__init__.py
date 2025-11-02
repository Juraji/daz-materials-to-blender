def register():
    import bpy
    from .import_materials import ImportMaterialsPanel3D, ImportMaterialsPanelShaderEditor
    from .genesis_eye_tools import GenesisEyeToolsPanel3D

    bpy.utils.register_class(ImportMaterialsPanel3D)
    bpy.utils.register_class(ImportMaterialsPanelShaderEditor)
    bpy.utils.register_class(GenesisEyeToolsPanel3D)


def unregister():
    import bpy
    from .import_materials import ImportMaterialsPanel3D, ImportMaterialsPanelShaderEditor
    from .genesis_eye_tools import GenesisEyeToolsPanel3D

    bpy.utils.unregister_class(ImportMaterialsPanel3D)
    bpy.utils.unregister_class(ImportMaterialsPanelShaderEditor)
    bpy.utils.unregister_class(GenesisEyeToolsPanel3D)
