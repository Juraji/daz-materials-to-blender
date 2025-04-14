from typing import Literal

from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node, NodeTree, NodeTreeInterfaceSocket, \
    NodeTreeInterfacePanel

from ...properties import MaterialImportProperties


class MaterialShader:
    group_name: str

    def __init__(self, properties: MaterialImportProperties):
        self.properties = properties

    def create_node_group(self, node_trees: BlendDataNodeTrees):
        raise NotImplementedError()

    def apply_material(self,
                       node_tree: ShaderNodeTree,
                       node_mapping: Node,
                       node_material_output: Node,
                       channels: dict):
        raise NotImplementedError()

    @staticmethod
    def color_socket_input_generator(
            node_tree: NodeTree,
            in_out: Literal["INPUT", "OUTPUT"] | None = "INPUT"
    ):
        def curried_generator(name: str,
                              default_value: tuple[float, float, float, float],
                              parent: NodeTreeInterfacePanel | None = None) -> NodeTreeInterfaceSocket:
            sock = node_tree.interface.new_socket(name=name, in_out=in_out, socket_type='NodeSocketColor',
                                                  parent=parent)
            sock.default_value = default_value
            return sock

        return curried_generator

    @staticmethod
    def float_socket_input_generator(
            node_tree: NodeTree,
            in_out: Literal["INPUT", "OUTPUT"] | None = "INPUT"
    ):
        def curried_generator(name: str,
                              default_value: float,
                              parent: NodeTreeInterfacePanel | None = None) -> NodeTreeInterfaceSocket:
            sock = node_tree.interface.new_socket(name=name, in_out=in_out, socket_type='NodeSocketFloat',
                                                  parent=parent)
            sock.default_value = default_value
            return sock

        return curried_generator

    @staticmethod
    def vector_socket_input_generator(
            node_tree: NodeTree,
            in_out: Literal["INPUT", "OUTPUT"] | None = "INPUT"
    ):
        def curried_generator(name: str,
                              default_value: tuple[float, float, float],
                              parent: NodeTreeInterfacePanel | None = None) -> NodeTreeInterfaceSocket:
            sock = node_tree.interface.new_socket(name=name, in_out=in_out, socket_type='NodeSocketVector',
                                                  parent=parent)
            sock.default_value = default_value
            return sock

        return curried_generator

    @staticmethod
    def link_socket_generator(node_tree: NodeTree):
        def curried_link(source: Node,
                         target: Node,
                         source_socket: NodeTreeInterfaceSocket | int,
                         target_socket: NodeTreeInterfaceSocket | int):
            if isinstance(source_socket, NodeTreeInterfaceSocket):
                source_socket = source.outputs[source_socket.name]
            else:
                source_socket = source.outputs[source_socket]
            if isinstance(target_socket, NodeTreeInterfaceSocket):
                target_socket = target.inputs[target_socket.name]
            else:
                target_socket = target.inputs[target_socket]

            node_tree.links.new(source_socket, target_socket)

        return curried_link
