from bpy.types import Panel

from ..properties import MaterialImportProperties


class ImportMaterialsPanelBase(Panel):
    bl_category = "Juraji's DAZ Import"
    bl_region_type = "UI"
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
            options_panel.label(text="Utilities")
            options_panel.operator("daz_import.create_shader_groups")

        layout.prop(props, "daz_scene_file")
        layout.operator("daz_import.import_all_materials")

class ImportMaterialsPanel3D(ImportMaterialsPanelBase):
    bl_space_type = "VIEW_3D"
    bl_context = "objectmode"
    bl_idname = "VIEW3D_PT_daz_import_materials"
    bl_label = ImportMaterialsPanelBase.bl_label

class ImportMaterialsPanelShaderEditor(ImportMaterialsPanelBase):
    bl_space_type = "NODE_EDITOR"
    bl_context = "shader"
    bl_idname = "NODE_PT_daz_import_materials"
    bl_label = ImportMaterialsPanelBase.bl_label
