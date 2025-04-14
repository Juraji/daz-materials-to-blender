from datetime import datetime

from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node

from ..properties import MaterialImportProperties

GROUP_NAME = "DAZ Translucent Shader"


def create_node_group(
        node_trees: BlendDataNodeTrees,
        props: MaterialImportProperties):
    node_group = node_trees.new(type='ShaderNodeTree', name=GROUP_NAME)
    node_group.color_tag = 'TEXTURE'
    node_group.description = f'Created at {datetime.now()}'
    node_group.default_group_node_width = 400


def apply_material(
        node_tree: ShaderNodeTree,
        node_mapping: Node,
        node_material_output: Node,
        channels: dict,
        props: MaterialImportProperties):
    pass
