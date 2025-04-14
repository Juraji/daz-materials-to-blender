import bpy

from ..properties import MaterialImportProperties
from ..shaders import pbr_skin, iray_uber, translucent_shader
from ..shaders.common import dual_lobe_specular_group


class CreateShaderGroupsOperator(bpy.types.Operator):
    bl_idname = "daz_import.create_shader_groups"
    bl_label = "Create Shader Groups"
    bl_description = ("Create DAZ shader groups. Useful if you just want those shader node group goodies. "
                      "The import will create them if they don't exist.")
    bl_options = {"REGISTER", "UNDO"}

    shader_group_modules = [
        dual_lobe_specular_group,
        pbr_skin,
        iray_uber,
        translucent_shader
    ]

    @classmethod
    def poll(cls, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups
        group_names = map(lambda m: m.GROUP_NAME, cls.shader_group_modules)

        return props.replace_node_groups or any(name not in node_groups for name in group_names)

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        node_groups = bpy.data.node_groups

        for module in self.shader_group_modules:
            if module.GROUP_NAME in node_groups:
                if not props.replace_node_groups:
                    continue
                node_groups.remove(node_groups[module.GROUP_NAME])
            module.create_node_group(node_groups, props)

        return {'FINISHED'}
