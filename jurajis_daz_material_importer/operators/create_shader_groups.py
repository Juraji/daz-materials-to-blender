from typing import Type

import bpy

from ..properties import MaterialImportProperties
from ..shaders import pbr_skin, iray_uber, iwave_translucent_fabric, dls
from ..shaders.material_shader import ShaderGroupBuilder


class CreateShaderGroupsOperator(bpy.types.Operator):
    bl_idname = "daz_import.create_shader_groups"
    bl_label = "Create Shader Groups"
    bl_description = ("Create DAZ shader groups. Useful if you just want those shader node group goodies. "
                      "The import will create them if they don't exist.")
    bl_options = {"REGISTER", "UNDO"}

    builders: list[Type[ShaderGroupBuilder]] = [
        dls.DualLobeSpecularShaderGroupBuilder,
        pbr_skin.PBRSkinShaderGroupBuilder,
        iray_uber.IrayUberShaderGroupBuilder,
        iwave_translucent_fabric.IWaveTranslucentFabricShaderGroupBuilder
    ]

    @classmethod
    def poll(cls, context):
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups
        group_names = map(lambda b: b.group_name(), cls.builders)

        return props.replace_node_groups or any(name not in node_groups for name in group_names)

    def execute(self, context):
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups

        for material_shader in self.builders:
            if material_shader.group_name() in node_groups:
                if not props.replace_node_groups:
                    continue
                node_groups.remove(node_groups[material_shader.group_name()])
            material_shader(props, node_groups).setup_group()

        return {'FINISHED'}
