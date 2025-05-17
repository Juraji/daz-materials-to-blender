import bpy
from bpy.types import Material, ShaderNodeGroup, ShaderNodeOutputMaterial, ShaderNodeTree

from ..shaders import ShaderGroupApplier
from ..utils.node_trees import link_socket, add_node


class ShaderGroupConverter:
    from_type: type[ShaderGroupApplier] = None
    to_type: type[ShaderGroupApplier] = None
    display_name: str = None

    @classmethod
    def property_mapping(cls) -> list[tuple[str, str]]:
        raise NotImplementedError("Missing property mapping")

    @classmethod
    def convert_materials(cls, materials: list[Material], keep_original_group: bool):
        mapping = cls.property_mapping()
        target = cls.to_type

        for material in materials:
            node_tree = material.node_tree
            org_group = next(n for n in node_tree.nodes if isinstance(n, ShaderNodeGroup))

            new_group = add_node(
                node_tree,
                ShaderNodeGroup,
                target.group_name(),
                target.node_group_location,
                props={
                    "width": target.group_node_width,
                    "node_tree": bpy.data.node_groups[target.group_name()],
                }
            )

            cls.convert_material(mapping, node_tree, org_group, new_group)

            if not keep_original_group:
                node_tree.nodes.remove(org_group)

    @classmethod
    def convert_material(cls,
                         mapping: list[tuple[str, str]],
                         node_tree: ShaderNodeTree,
                         org_group: ShaderNodeGroup,
                         new_group: ShaderNodeGroup):
        # Link new group to material output
        material_output = next(n for n in node_tree.nodes if isinstance(n, ShaderNodeOutputMaterial))
        for out_sock in new_group.outputs:
            target_sock = cls.to_type.output_socket_map.get(out_sock.name)
            if target_sock is None:
                raise Exception(f"Output socket {out_sock.name} in group {cls.to_type.group_name()} has no "
                                f"target socket in Material Output.")

            link_socket(node_tree, new_group, material_output, out_sock, target_sock)

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
