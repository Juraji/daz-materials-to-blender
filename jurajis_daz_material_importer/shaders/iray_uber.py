from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node
from ..properties import MaterialImportProperties


def create_node_group(
        node_trees: BlendDataNodeTrees,
        props: MaterialImportProperties):
    pass


def apply_material(
        node_tree: ShaderNodeTree,
        node_mapping: Node,
        node_material_output: Node,
        channels: dict,
        props: MaterialImportProperties):
    pass
