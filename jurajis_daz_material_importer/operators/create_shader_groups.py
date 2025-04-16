from typing import Type

import bpy
from bpy.types import Operator

from .operator_report_mixin import OperatorReportMixin
from ..properties import MaterialImportProperties
from ..shaders.base import ShaderGroupBuilder
from ..shaders.dls import DualLobeSpecularShaderGroupBuilder
from ..shaders.iray_uber import IrayUberShaderGroupBuilder
from ..shaders.iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupBuilder
from ..shaders.pbr_skin import PBRSkinShaderGroupBuilder


class CreateShaderGroupsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.create_shader_groups"
    bl_label = "Create Shader Groups"
    bl_description = ("Create DAZ shader groups. Useful if you just want those shader node group goodies. "
                      "The import will create them if they don't exist.")
    bl_options = {"REGISTER", "UNDO"}

    builders: list[Type[ShaderGroupBuilder]] = [
        DualLobeSpecularShaderGroupBuilder,
        PBRSkinShaderGroupBuilder,
        IrayUberShaderGroupBuilder,
        IWaveTranslucentFabricShaderGroupBuilder
    ]

    @classmethod
    def poll(cls, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups
        group_names = map(lambda b: b.group_name(), cls.builders)

        return props.replace_node_groups or any(name not in node_groups for name in group_names)

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups

        for material_shader in self.builders:
            if material_shader.group_name() in node_groups:
                if not props.replace_node_groups:
                    continue
                node_groups.remove(node_groups[material_shader.group_name()])
            material_shader(props, node_groups).setup_group()
            self.report_info(f"Created shader group \"{material_shader.group_name()}\".")

        self.report_info(f"Shader groups updated/created!")
        return {'FINISHED'}
