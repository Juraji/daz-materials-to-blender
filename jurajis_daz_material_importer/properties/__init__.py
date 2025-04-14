from .material_import_properties import MaterialImportProperties

def register():
    import bpy

    bpy.utils.register_class(MaterialImportProperties)

    bpy.types.Scene.daz_import__material_import_properties = bpy.props.PointerProperty(type=MaterialImportProperties)

def unregister():
    import bpy

    bpy.utils.unregister_class(MaterialImportProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.daz_import__material_import_properties