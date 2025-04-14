from typing import Type

import bpy

from ..properties import MaterialImportProperties
from ..shaders import pbr_skin, iray_uber, iwave_translucent_fabric, dls
from ..shaders.common.shader_group import MaterialShader


class CreateShaderGroupsOperator(bpy.types.Operator):
    bl_idname = "daz_import.create_shader_groups"
    bl_label = "Create Shader Groups"
    bl_description = ("Create DAZ shader groups. Useful if you just want those shader node group goodies. "
                      "The import will create them if they don't exist.")
    bl_options = {"REGISTER", "UNDO"}

    material_shaders: list[Type[MaterialShader]] = [
        dls.DualLobeSpecularMaterialShader,
        pbr_skin.PBRSkinMaterialShader,
        iray_uber.IrayUberMaterialShader,
        iwave_translucent_fabric.IWaveTranslucentFabricMaterialShader
    ]

    @classmethod
    def poll(cls, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups
        group_names = map(lambda m: m.group_name, cls.material_shaders)

        return props.replace_node_groups or any(name not in node_groups for name in group_names)

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups

        for material_shader in self.material_shaders:
            if material_shader.group_name in node_groups:
                if not props.replace_node_groups:
                    continue
                node_groups.remove(node_groups[material_shader.group_name])
            material_shader(props).create_node_group(node_groups)

        return {'FINISHED'}
