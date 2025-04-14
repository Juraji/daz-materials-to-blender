from typing import Callable, Literal, Optional

from bpy.types import NodeTree, NodeTreeInterfaceSocket, Node, NodeTreeInterfacePanel


def color_socket_input_generator(
        node_tree: NodeTree,
        in_out: Literal["INPUT", "OUTPUT"] | None = "INPUT"
):
    def curried_generator(name: str,
                          default_value: tuple[float, float, float, float],
                          parent: NodeTreeInterfacePanel | None = None) -> NodeTreeInterfaceSocket:
        sock = node_tree.interface.new_socket(name=name, in_out=in_out, socket_type='NodeSocketColor', parent=parent)
        sock.default_value = default_value
        return sock

    return curried_generator


def float_socket_input_generator(
        node_tree: NodeTree,
        in_out: Literal["INPUT", "OUTPUT"] | None = "INPUT"
):
    def curried_generator(name: str,
                          default_value: float,
                          parent: NodeTreeInterfacePanel | None = None) -> NodeTreeInterfaceSocket:
        sock = node_tree.interface.new_socket(name=name, in_out=in_out, socket_type='NodeSocketFloat', parent=parent)
        sock.default_value = default_value
        return sock

    return curried_generator


def vector_socket_input_generator(
        node_tree: NodeTree,
        in_out: Literal["INPUT", "OUTPUT"] | None = "INPUT"
):
    def curried_generator(name: str,
                          default_value: tuple[float, float, float],
                          parent: NodeTreeInterfacePanel | None = None) -> NodeTreeInterfaceSocket:
        sock = node_tree.interface.new_socket(name=name, in_out=in_out, socket_type='NodeSocketVector', parent=parent)
        sock.default_value = default_value
        return sock

    return curried_generator


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
