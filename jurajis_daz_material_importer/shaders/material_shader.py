import os
from datetime import datetime
from typing import Literal, Any, cast

import bpy
from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node, NodeTree, NodeTreeInterfacePanel, NodeSocket, \
    NodeTreeInterfaceSocket, TextureNodeImage, ShaderNodeTexImage

from ..properties import MaterialImportProperties
from ..utils.slugify import slugify


class ShaderGroupBuilder:
    @staticmethod
    def group_name() -> str:
        raise NotImplementedError()

    def __init__(self, properties: MaterialImportProperties, node_trees: BlendDataNodeTrees):
        super().__init__()
        self.properties = properties
        self.node_trees = node_trees
        self.node_group: NodeTree | None = None

    def setup_group(self):
        # noinspection PyTypeChecker
        self.node_group = self.node_trees.new(type="ShaderNodeTree", name=self.group_name())
        self.node_group.color_tag = "SHADER"
        self.node_group.description = f'Created by DAZ Material Importer at {datetime.now()}'
        self.node_group.default_group_node_width = 400

    # Sockets
    def color_socket(self,
                     name: str,
                     default_value: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
                     in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                     parent: NodeTreeInterfacePanel = None,
                     props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self.__add_socket("NodeSocketColor", name, default_value, in_out, parent, props)

    def float_socket(self,
                     name: str,
                     default_value: float = 0,
                     in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                     parent: NodeTreeInterfacePanel = None,
                     props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self.__add_socket("NodeSocketFloat", name, default_value, in_out, parent, props)

    def vector_socket(self,
                      name: str,
                      default_value: tuple[float, float, float] = (0, 0, 0),
                      in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                      parent: NodeTreeInterfacePanel = None,
                      props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self.__add_socket("NodeSocketVector", name, default_value, in_out, parent, props)

    def shader_socket(self,
                      name: str,
                      in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                      parent: NodeTreeInterfacePanel = None,
                      props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self.__add_socket("NodeSocketShader", name, None, in_out, parent, props)

    @staticmethod
    def set_socket(node: Node, socket: NodeSocket | int, value: Any):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        socket_input = node.inputs[socket_key]
        setattr(socket_input, "default_value", value)

    def link_socket(self,
                    source: Node,
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

        self.node_group.links.new(source_socket, target_socket)

    def __add_socket(self,
                     socket_type: str,
                     name: str,
                     default_value: Any,
                     in_out: Literal["INPUT", "OUTPUT"],
                     parent: NodeTreeInterfacePanel,
                     props: dict[str, Any]) -> NodeTreeInterfaceSocket:
        sock = self.node_group.interface \
            .new_socket(name=name, in_out=in_out, socket_type=socket_type, parent=parent)

        if default_value is not None:
            sock.default_value = default_value

        for prop, value in props.items():
            sock[prop] = value

        return sock

    # Nodes
    def add_panel(self, name: str, default_closed: bool = True) -> NodeTreeInterfacePanel:
        return self.node_group.interface.new_panel(name, default_closed=default_closed)

    def add_frame(self, label: str, location: tuple[float, float]) -> Node:
        return self.add_node("NodeFrame", label, location)

    def add_node__group_input(self,
                              label: str,
                              location: tuple[float, float]):
        return self.add_node("NodeGroupInput", label, location)

    def add_node__group_output(self,
                               label: str,
                               location: tuple[float, float]):
        out = self.add_node("NodeGroupOutput", label, location)
        out.is_active_output = True
        return out

    def add_node__hsv(self,
                      label: str,
                      location: tuple[float, float],
                      parent: Node = None) -> Node:
        return self.add_node("ShaderNodeHueSaturation", label, location, parent)

    def add_node__mix(self,
                      label: str,
                      location: tuple[float, float],
                      data_type: str = "RGBA",
                      blend_type: str = "MULTIPLY",
                      default_factor: float = 1,
                      parent: Node = None) -> Node:
        mix = self.add_node("ShaderNodeMix", label, location, parent, {
            "data_type": data_type,
            "blend_type": blend_type
        })
        # noinspection PyUnresolvedReferences
        mix.inputs[0].default_value = default_factor
        return mix

    def add_node__mix_shader(self,
                             label: str,
                             location: tuple[float, float],
                             parent: Node = None,
                             props: dict[str, Any] = {}) -> Node:
        return self.add_node("ShaderNodeMixShader", label, location, parent, props)

    def add_node__math_vector(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}) -> Node:
        return self.add_node("ShaderNodeVectorMath", label, location, parent, props=props)

    def add_node__normal_map(self,
                             label: str,
                             location: tuple[float, float],
                             parent: Node = None,
                             props: dict[str, Any] = {}):
        return self.add_node("ShaderNodeNormalMap", label, location, parent, props)

    def add_node__bump(self,
                       label: str,
                       location: tuple[float, float],
                       parent: Node = None,
                       props: dict[str, Any] = {}):
        return self.add_node("ShaderNodeBump", label, location, parent, props)

    def add_node__princ_bdsf(self,
                             label: str,
                             location: tuple[float, float],
                             parent: Node = None,
                             props: dict[str, Any] = {}):
        return self.add_node("ShaderNodeBsdfPrincipled", label, location, parent, props)

    def add_node_shader_group(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}):
        return self.add_node("ShaderNodeGroup", label, location, parent, props)

    def add_node(self,
                 node_type: str,
                 label: str,
                 location: tuple[float, float],
                 parent: Node = None,
                 props: dict[str, Any] = {}) -> Node:
        node = self.node_group.nodes.new(node_type)
        node.label = label
        node.name = slugify(self.group_name(), node_type, label)
        node.parent = parent
        node.location = location

        for prop, value in props.items():
            if hasattr(node, prop):
                setattr(node, prop, value)

        return node


class ShaderGroupApplier:
    __group_node_width: float = 400
    __texture_node_location_y_offset: float = 300

    @staticmethod
    def group_name() -> str:
        raise NotImplementedError()

    def __init__(self,
                 properties: MaterialImportProperties,
                 node_tree: ShaderNodeTree,
                 mapping_node: Node,
                 material_ouput_node: Node):
        super().__init__()
        self.shader_group_node: Node | None = None
        self.properties = properties
        self.node_tree = node_tree
        self.mapping_node = mapping_node
        self.material_ouput_node = material_ouput_node

    def add_shader_group(self, location: tuple[float, float], channels: dict):
        shader_group = self.node_tree.nodes.new("ShaderNodeGroup")
        shader_group.label = self.group_name()
        shader_group.name = slugify(self.group_name())
        shader_group.location = location
        shader_group.width = self.__group_node_width
        shader_group.node_tree = bpy.data.node_groups[self.group_name()]
        self.link_socket(shader_group, self.material_ouput_node, 0, 0)
        self.shader_group_node = shader_group

    def align_image_nodes(self, start_x: float, start_y: float, offset: float = 50):
        tex_nodes = filter(lambda n: n.type == "TEX_IMAGE", self.node_tree.nodes)

        current_y = start_y
        for node in tex_nodes:
            node.location = (start_x, current_y)
            current_y -= offset

    def add_image_texture(self, path: str, non_color: bool, tile: int = 1):
        tex_image: ShaderNodeTexImage = cast(ShaderNodeTexImage, self.node_tree.nodes.new(type="ShaderNodeTexImage"))
        tex_image.hide = True
        tex_image.image = bpy.data.images.load(path)
        # noinspection PyTypeChecker
        tex_image.image.colorspace_settings.name = "Non-Color" if non_color else "sRGB"
        tex_image.image_user.tile = tile

        img_name = os.path.basename(path)
        if img_name in bpy.data.images:
            tex_image.image = bpy.data.images[img_name]
        else:
            tex_image.image = bpy.data.images.load(img_name)

        self.link_socket(self.mapping_node, tex_image, 0, 0)
        return tex_image

    @staticmethod
    def set_socket(node: Node, socket: NodeSocket | int | str, value: Any):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        socket_input = node.inputs[socket_key]
        setattr(socket_input, "default_value", value)

    def link_socket(self,
                    source: Node,
                    target: Node,
                    source_socket: NodeSocket | int | str,
                    target_socket: NodeSocket | int | str):
        if isinstance(source_socket, NodeSocket):
            source_socket = source.outputs[source_socket.name]
        else:
            source_socket = source.outputs[source_socket]
        if isinstance(target_socket, NodeSocket):
            target_socket = target.inputs[target_socket.name]
        else:
            target_socket = target.inputs[target_socket]

        self.node_tree.links.new(source_socket, target_socket)
