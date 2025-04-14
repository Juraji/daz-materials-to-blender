from bpy.types import Panel

from ..properties import MaterialImportProperties


class VIEW3D_PT_ImportMaterials(Panel):
    bl_category = "Juraji's DAZ Import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Import DAZ Materials"

    def draw(self, context):
        layout = self.layout

        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties

        options_header, options_panel = layout.panel("import_options", default_closed=True)
        options_header.label(text="Options")
        if options_panel:
            options_panel.label(text="Import Options")
            options_panel.prop(props, "replace_node_groups")
            options_panel.prop(props, "rename_materials")
            options_panel.prop(props, "rename_objects")
            options_panel.label(text="Corrections")
            options_panel.prop(props, "normal_factor")
            options_panel.prop(props, "dls_layer_factor")

        layout.prop(props, "daz_scene_file")
        layout.operator("object.import_daz_materials")
