from bpy.types import Panel

from ..shaders.library import SUPPORT_SHADER_GROUPS, SHADER_GROUPS
from ..properties import MaterialImportProperties


class ImportMaterialsPanelBase(Panel):
    bl_category = "Juraji's Tools"
    bl_region_type = "UI"
    bl_label = "Import DAZ Materials"

    def draw(self, context):
        layout = self.layout

        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties

        tools_header, tools_panel = layout.panel("tools", default_closed=True)
        tools_header.label(text="Tools & Debugging")
        if tools_panel:
            tools_panel.operator("daz_import.debug_export_materials_json")
            tools_panel.operator("daz_import.debug_delete_all_groups")

        shader_groups_header, shader_groups_panel = layout.panel("shader_groups", default_closed=True)
        shader_groups_header.label(text="Shader Groups")
        if shader_groups_panel:
            shader_groups_panel.label(text="Support")
            for group_name in SUPPORT_SHADER_GROUPS:
                op = shader_groups_panel.operator(
                    "daz_import.import_shader_group",
                    text=group_name)
                op.group_name = group_name

            shader_groups_panel.label(text="Shaders")
            for group_name in SHADER_GROUPS:
                op = shader_groups_panel.operator(
                    "daz_import.import_shader_group",
                    text=group_name)
                op.group_name = group_name

        options_header, options_panel = layout.panel("import_options", default_closed=True)
        options_header.label(text="Import Options")
        if options_panel:
            options_panel.label(text="Renaming")
            options_panel.prop(props, "rename_materials")
            options_panel.prop(props, "rename_objects")

            options_panel.label(text="General")
            options_panel.prop(props, "apply_color_corrections")
            options_panel.prop(props, "dls_weight_multiplier")
            options_panel.prop(props, "bump_strength_multiplier")

            options_panel.label(text="PBR Skin")
            options_panel.prop(props, "pbr_skin_normal_multiplier")

            options_panel.label(text="Iray Uber")
            options_panel.prop(props, "iray_uber_replace_glass")
            options_panel.prop(props, "iray_uber_remap_glossy_color_to_roughness")
            options_panel.prop(props, "iray_uber_clamp_emission")

        layout.prop(props, "daz_scene_file")
        layout.operator("daz_import.import_all_materials")
        layout.operator("daz_import.import_object_materials")


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
