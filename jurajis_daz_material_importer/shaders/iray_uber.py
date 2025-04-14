from datetime import datetime

from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node

from .material_shader import MaterialShader


class IrayUberMaterialShader(MaterialShader):
    group_name = "DAZ Iray Uber"

    def create_node_group(self, node_trees: BlendDataNodeTrees):
        node_group = node_trees.new(type='ShaderNodeTree', name=self.group_name)
        node_group.color_tag = 'TEXTURE'
        node_group.description = f'Created at {datetime.now()}'
        node_group.default_group_node_width = 400

    def apply_material(self,
                       node_tree: ShaderNodeTree,
                       node_mapping: Node,
                       node_material_output: Node,
                       channels: dict):
        pass
