from typing import Type

import bpy
from bpy.types import Material, ShaderNodeGroup, ShaderNodeOutputMaterial

from ..shaders import ShaderGroupApplier
from ..utils.node_trees import link_socket, add_node
from ..utils.slugify import slugify


class ShaderGroupConverter:

    @staticmethod
    def from_type() -> Type[ShaderGroupApplier]:
        raise NotImplementedError()

    @staticmethod
    def to_type() -> Type[ShaderGroupApplier]:
        raise NotImplementedError()

    @staticmethod
    def display_name() -> str:
        raise NotImplementedError()

    @staticmethod
    def property_mapping() -> list[tuple[str, str]]:
        raise NotImplementedError()

    def convert_materials(self, materials: list[Material]):
        mapping = self.property_mapping()
        to_cls = self.to_type()

        for material in materials:
            node_tree = material.node_tree
            org_group = next(n for n in node_tree.nodes if isinstance(n, ShaderNodeGroup))

            new_group = add_node(
                node_tree,
                ShaderNodeGroup,
                to_cls.group_name(),
                to_cls.node_group_location,
                props={
                    "width": to_cls.group_node_width,
                    "node_tree": bpy.data.node_groups[to_cls.group_name()],
                }
            )

            # Link new group to material output
            material_ouput = next(n for n in node_tree.nodes if isinstance(n, ShaderNodeOutputMaterial))
            for out_sock in new_group.outputs:
                target_sock = to_cls.output_socket_map.get(out_sock.name)
                if target_sock is None:
                    raise Exception(
                        f"Output socket {out_sock.name} in group {to_cls.group_name()} has no target socket in Material Output.")

                link_socket(node_tree, new_group, material_ouput, out_sock, target_sock)

            # Reroute links and copy values
            for org_sock_name, new_sock_name in mapping:
                org_socket = next(s for s in org_group.inputs if s.name == org_sock_name)
                new_socket = new_group.inputs[new_sock_name]

                if org_socket.type != new_socket.type:
                    raise Exception("Source and target socket types do not match")

                if len(org_socket.links) > 0:
                    from_socket = org_socket.links[0].from_socket
                    from_node = from_socket.node
                    link_socket(node_tree, from_node, new_group, from_socket, new_socket)
                else:
                    value = getattr(org_socket, "default_value")
                    setattr(new_socket, "default_value", value)

            node_tree.nodes.remove(org_group)
