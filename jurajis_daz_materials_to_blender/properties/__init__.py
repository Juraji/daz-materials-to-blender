from typing import cast

from bpy.types import Context as _Context

from .material_import_preferences import MaterialImportPreferences, ContentLibraryItem
from .material_import_properties import MaterialImportProperties


def register():
    import bpy

    bpy.utils.register_class(MaterialImportProperties)
    bpy.utils.register_class(ContentLibraryItem)
    bpy.utils.register_class(MaterialImportPreferences)

    bpy.types.Scene.daz_import__material_import_properties = bpy.props.PointerProperty(type=MaterialImportProperties)


def unregister():
    import bpy

    bpy.utils.unregister_class(MaterialImportProperties)
    bpy.utils.unregister_class(ContentLibraryItem)
    bpy.utils.unregister_class(MaterialImportPreferences)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.daz_import__material_import_properties


def props_from_ctx(context: _Context) -> MaterialImportProperties:
    # noinspection PyUnresolvedReferences
    return context.scene.daz_import__material_import_properties


def prefs_from_ctx(context: _Context) -> MaterialImportPreferences:
    prefs_name = MaterialImportPreferences.bl_idname
    return cast(MaterialImportPreferences, context.preferences.addons[prefs_name].preferences)
