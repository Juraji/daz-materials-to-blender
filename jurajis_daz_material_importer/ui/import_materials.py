from bpy.types import Panel

from ..properties import MaterialImportProperties
from ..shaders import SHADER_GROUP_BUILDERS


class ImportMaterialsPanelBase(Panel):
    bl_category = "Juraji's Tools"
    bl_region_type = "UI"
    bl_label = "Import DAZ Materials"

    _support_builders = [b for b in SHADER_GROUP_BUILDERS if b.is_support()]
    _shader_builders = [b for b in SHADER_GROUP_BUILDERS if not b.is_support()]

    def draw(self, context):
        layout = self.layout

        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties

        shader_groups_header, shader_groups_panel = layout.panel("shader_groups", default_closed=True)
        shader_groups_header.label(text="Shader Groups")
        if shader_groups_panel:
            shader_groups_panel.label(text="Support")
            for builder in self._support_builders:
                op = shader_groups_panel.operator(
                    "daz_import.create_shader_group",
                    text=builder.group_name())
                op.group_name = builder.group_name()

            shader_groups_panel.label(text="Shaders")
            for builder in self._shader_builders:
                op = shader_groups_panel.operator(
                    "daz_import.create_shader_group",
                    text=builder.group_name())
                op.group_name = builder.group_name()

        options_header, options_panel = layout.panel("import_options", default_closed=True)
        options_header.label(text="Import Options")
        if options_panel:
            options_panel.prop(props, "rename_materials")
            options_panel.prop(props, "rename_objects")

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
