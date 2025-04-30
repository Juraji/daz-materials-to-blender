from bpy.types import Context as _Context

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

def props_from_ctx(context: _Context) -> MaterialImportProperties:
    # noinspection PyUnresolvedReferences
    return context.scene.daz_import__material_import_properties