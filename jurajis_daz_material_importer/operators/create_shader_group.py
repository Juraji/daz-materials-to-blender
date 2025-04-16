import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

from .operator_report_mixin import OperatorReportMixin
from ..properties import MaterialImportProperties
from ..shaders import ShaderGroupBuilder, SHADER_GROUP_BUILDERS


class CreateShaderGroupOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.create_shader_group"
    bl_label = "Create Shader Group"
    bl_description = "Creates the Shader Group as identified by group_name."
    bl_options = {"REGISTER", "UNDO"}

    group_name: StringProperty(
        name="Group Name",
        description="The name of the shader group to create.",
    )

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups

        builder: ShaderGroupBuilder | None = None
        for b in SHADER_GROUP_BUILDERS:
            if b.group_name() == self.group_name:
                builder = b(props, node_groups)

        if builder is None:
            self.report_error(f"Builder not found for name \"{self.group_name}\"!")
            return {"CANCELLED"}

        if builder.group_name() in node_groups:
            if not props.replace_node_groups:
                self.report_warning(f"Shader Group \"{self.group_name}\" already exists!")
                return {"CANCELLED"}

            existing = node_groups[builder.group_name()]
            node_groups.remove(existing)

        # Also create dependencies
        for dep in builder.depends_on():
            # noinspection PyUnresolvedReferences
            bpy.ops.daz_import.create_shader_group(group_name=dep, silent=self.silent)

        builder.setup_group()
        self.report_info(f"Successfully created shader group \"{self.group_name}\".")
        return {'FINISHED'}
