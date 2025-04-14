from typing import Callable

from bpy.types import NodeTree, NodeTreeInterfaceSocket, Node


def node_tree_color_socket_input_generator(node_tree: NodeTree) -> Callable[
    [str, tuple[float, float, float, float]], NodeTreeInterfaceSocket]:
    def curried_generator(name: str, default_value: tuple[float, float, float, float]) -> NodeTreeInterfaceSocket:
        sock = node_tree.interface.new_socket(name=name, in_out='INPUT', socket_type='NodeSocketColor')
        sock.default_value = default_value
        return sock

    return curried_generator


def node_tree_float_socket_input_generator(node_tree: NodeTree) -> Callable[
    [str, float], NodeTreeInterfaceSocket]:
    def curried_generator(name: str, default_value: float) -> NodeTreeInterfaceSocket:
        sock = node_tree.interface.new_socket(name=name, in_out='INPUT', socket_type='NodeSocketFloat')
        sock.default_value = default_value
        return sock

    return curried_generator


def node_tree_vector_socket_input_generator(node_tree: NodeTree) -> Callable[
    [str, tuple[float, float, float]], NodeTreeInterfaceSocket]:
    def curried_generator(name: str, default_value: tuple[float, float, float]) -> NodeTreeInterfaceSocket:
        sock = node_tree.interface.new_socket(name=name, in_out='INPUT', socket_type='NodeSocketVector')
        sock.default_value = default_value
        return sock

    return curried_generator


def node_tree_link_socket_generator(node_tree: NodeTree) -> Callable[
    [Node, Node, NodeTreeInterfaceSocket | int, int], None]:
    def curried_link(source: Node, target: Node, source_socket: NodeTreeInterfaceSocket | int, target_socket: int):
        if isinstance(source_socket, NodeTreeInterfaceSocket):
            node_tree.links.new(source.outputs[source_socket.index - 1], target.inputs[target_socket])
        else:
            node_tree.links.new(source.outputs[source_socket], target.inputs[target_socket])

    return curried_link
