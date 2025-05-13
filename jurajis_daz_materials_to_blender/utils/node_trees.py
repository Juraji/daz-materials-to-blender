from os import path
from typing import Any, TypeVar, Type

import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTexImage

from .slugify import slugify


def link_socket(node_tree: NodeTree,
                source: Node,
                target: Node,
                source_socket: NodeSocket | int | str,
                target_socket: NodeSocket | int | str,
                optional: bool = False, ):
    if not isinstance(source_socket, NodeSocket):
        source_socket = source.outputs[source_socket]

    if not isinstance(target_socket, NodeSocket):
        target_socket = target.inputs[target_socket]

    if not optional and not source_socket:
        raise Exception(f"Source socket not found!")
    if not optional and not target_socket:
        raise Exception(f"Target socket not found!")

    node_tree.links.new(source_socket, target_socket)


_TNode = TypeVar('_TNode', bound=Node)


def add_node(node_tree: NodeTree,
             node_type: Type[_TNode],
             label: str,
             location: tuple[float, float],
             parent: Node = None,
             props: dict[str, Any] = {}) -> _TNode:
    node_type_id = getattr(getattr(node_type, "bl_rna", None), "identifier", None)
    if node_type_id is None:
        raise TypeError(f"Cannot resolve bl_idname for type: {node_type.__name__}")

    node = node_tree.nodes.new(node_type_id)
    node.label = label
    node.name = slugify(node_type_id, label)
    node.parent = parent
    node.location = location

    # Set props
    for prop, value in props.items():
        if hasattr(node, prop):
            setattr(node, prop, value)

    return node


def add_image_texture(node_tree: NodeTree,
                      location: tuple[float, float],
                      image_path: str,
                      non_color: bool,
                      force_new_node: bool = False) -> ShaderNodeTexImage:
    img_name = path.basename(image_path)

    if not force_new_node:
        for node in node_tree.nodes:
            if isinstance(node, ShaderNodeTexImage) and node.image and node.image.name == img_name:
                return node

    try:
        image = bpy.data.images.load(image_path, check_existing=True)
        # noinspection PyTypeChecker
        image.colorspace_settings.name = "Non-Color" if non_color else "sRGB"
    except Exception as e:
        raise Exception(f"Failed to load image {image_path}: {e}")


    props = {"image": image, "hide": True}

    return add_node(node_tree, ShaderNodeTexImage, img_name, location, props=props)
