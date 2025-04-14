import bpy


def register():
    from bpy.props import PointerProperty
    from .operators import OBJECT_OT_ImportMaterials
    from .properties import MaterialImportProperties
    from .ui import VIEW3D_PT_ImportMaterials

    bpy.utils.register_class(OBJECT_OT_ImportMaterials)
    bpy.utils.register_class(VIEW3D_PT_ImportMaterials)
    bpy.utils.register_class(MaterialImportProperties)

    bpy.types.Scene.daz_import__material_import_properties = PointerProperty(type=MaterialImportProperties)


def unregister():
    from .operators import OBJECT_OT_ImportMaterials
    from .properties import MaterialImportProperties
    from .ui import VIEW3D_PT_ImportMaterials

    bpy.utils.unregister_class(OBJECT_OT_ImportMaterials)
    bpy.utils.unregister_class(VIEW3D_PT_ImportMaterials)
    bpy.utils.unregister_class(MaterialImportProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.daz_import__material_import_properties
