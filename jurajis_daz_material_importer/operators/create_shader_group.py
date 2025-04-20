from typing import Type

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Context

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

    def execute(self, context: Context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups

        builder_cls: Type[ShaderGroupBuilder] | None = next(
            (c for c in SHADER_GROUP_BUILDERS if c.group_name() == self.group_name), None)

        if builder_cls is None:
            self.report_error(f"Builder not found for name \"{self.group_name}\"!")
            return {"CANCELLED"}

        if builder_cls.group_name() in node_groups:
            self.report_warning(f"Shader Group \"{self.group_name}\" already exists!")
            return {"FINISHED"}

        # Also create dependencies
        for dep in builder_cls.depends_on():
            # noinspection PyUnresolvedReferences
            res = bpy.ops.daz_import.create_shader_group(group_name=dep.group_name(), silent=self.silent)
            if not res == {"FINISHED"}:
                return {"FINISHED"}

        builder = builder_cls(props, node_groups)
        builder.setup_group()

        self.report_info(f"Successfully created shader group \"{self.group_name}\".")
        return {'FINISHED'}
