import os
from datetime import datetime
from typing import Literal, Any, cast, Type

import bpy
from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node, NodeTree, NodeTreeInterfacePanel, NodeSocket, \
    NodeTreeInterfaceSocket, ShaderNodeTexImage

from ..properties import MaterialImportProperties
from ..utils.dson import DsonMaterialChannel, DsonFloatMaterialChannel, DsonColorMaterialChannel
from ..utils.slugify import slugify


class _GroupNameMixin:
    @staticmethod
    def group_name() -> str:
        raise NotImplementedError()


class _MaterialTypeIdMixin:
    @staticmethod
    def material_type_id() -> str:
        raise NotImplementedError()


class ShaderGroupBuilder(_GroupNameMixin, _MaterialTypeIdMixin):

    @staticmethod
    def depends_on() -> set[str]:
        return set()

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
    def _color_socket(self,
                      name: str,
                      default_value: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
                      in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                      parent: NodeTreeInterfacePanel = None,
                      props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self._add_socket("NodeSocketColor", name, default_value, in_out, parent, props)

    def _float_socket(self,
                      name: str,
                      default_value: float = 0,
                      in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                      parent: NodeTreeInterfacePanel = None,
                      props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self._add_socket("NodeSocketFloat", name, default_value, in_out, parent, props)

    def _vector_socket(self,
                       name: str,
                       default_value: tuple[float, float, float] = (0, 0, 0),
                       in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                       parent: NodeTreeInterfacePanel = None,
                       props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self._add_socket("NodeSocketVector", name, default_value, in_out, parent, props)

    def _shader_socket(self,
                       name: str,
                       in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                       parent: NodeTreeInterfacePanel = None,
                       props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self._add_socket("NodeSocketShader", name, None, in_out, parent, props)

    @staticmethod
    def _set_socket(node: Node, socket: NodeSocket | int, value: Any):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        socket_input = node.inputs[socket_key]
        setattr(socket_input, "default_value", value)

    def _link_socket(self,
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

    def _add_socket(self,
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
    def _add_panel(self, name: str, default_closed: bool = True) -> NodeTreeInterfacePanel:
        return self.node_group.interface.new_panel(name, default_closed=default_closed)

    def add_frame(self, label: str, location: tuple[float, float]) -> Node:
        return self._add_node("NodeFrame", label, location)

    def _add_node__group_input(self,
                               label: str,
                               location: tuple[float, float]):
        return self._add_node("NodeGroupInput", label, location)

    def _add_node__group_output(self,
                                label: str,
                                location: tuple[float, float]):
        out = self._add_node("NodeGroupOutput", label, location)
        out.is_active_output = True
        return out

    def _add_node__hsv(self,
                       label: str,
                       location: tuple[float, float],
                       parent: Node = None) -> Node:
        return self._add_node("ShaderNodeHueSaturation", label, location, parent)

    def _add_node__mix(self,
                       label: str,
                       location: tuple[float, float],
                       data_type: str = "RGBA",
                       blend_type: str = "MULTIPLY",
                       default_factor: float = 1,
                       parent: Node = None) -> Node:
        mix = self._add_node("ShaderNodeMix", label, location, parent, {
            "data_type": data_type,
            "blend_type": blend_type
        })
        # noinspection PyUnresolvedReferences
        mix.inputs[0].default_value = default_factor
        return mix

    def _add_node__mix_shader(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}) -> Node:
        return self._add_node("ShaderNodeMixShader", label, location, parent, props)

    def _add_node__math_vector(self,
                               label: str,
                               location: tuple[float, float],
                               parent: Node = None,
                               props: dict[str, Any] = {}) -> Node:
        return self._add_node("ShaderNodeVectorMath", label, location, parent, props=props)

    def _add_node__normal_map(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}):
        return self._add_node("ShaderNodeNormalMap", label, location, parent, props)

    def _add_node__bump(self,
                        label: str,
                        location: tuple[float, float],
                        parent: Node = None,
                        props: dict[str, Any] = {}):
        return self._add_node("ShaderNodeBump", label, location, parent, props)

    def _add_node__princ_bdsf(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}):
        return self._add_node("ShaderNodeBsdfPrincipled", label, location, parent, props)

    def _add_node_shader_group(self,
                               label: str,
                               location: tuple[float, float],
                               parent: Node = None,
                               props: dict[str, Any] = {}):
        return self._add_node("ShaderNodeGroup", label, location, parent, props)

    def _add_node(self,
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


class ShaderGroupApplier(_GroupNameMixin, _MaterialTypeIdMixin):
    __group_node_width: float = 400
    __texture_node_location_y_offset: float = 300

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

    def add_shader_group(self, location: tuple[float, float], channels: dict[str, DsonMaterialChannel]):
        shader_group = self.node_tree.nodes.new("ShaderNodeGroup")
        shader_group.label = self.group_name()
        shader_group.name = slugify(self.group_name())
        shader_group.location = location
        shader_group.width = self.__group_node_width
        shader_group.node_tree = bpy.data.node_groups[self.group_name()]
        self._link_socket(shader_group, self.material_ouput_node, 0, 0)
        self.shader_group_node = shader_group

    def align_image_nodes(self, start_x: float, start_y: float, offset: float = 50):
        tex_nodes = filter(lambda n: n.type == "TEX_IMAGE", self.node_tree.nodes)

        current_y = start_y
        for node in tex_nodes:
            node.location = (start_x, current_y)
            current_y -= offset

    @staticmethod
    def _channel_feat_enabled(channels: dict[str, DsonMaterialChannel], feat_switch: str) -> bool:
        return feat_switch in channels and channels[feat_switch].value

    def _channel_values(self,
                        channels: dict[str, DsonMaterialChannel],
                        channel_id: str,
                        value_socket_name: str | None,
                        map_socket_name: str | None,
                        non_color_map: bool = True):
        if not channel_id in channels:
            return

        channel = channels[channel_id]

        if not value_socket_name is None and value_socket_name in self.shader_group_node.inputs:
            value_socket = self.shader_group_node.inputs[value_socket_name]

            if isinstance(channel, DsonFloatMaterialChannel):
                value_socket.default_value = channel.value
            elif isinstance(channel, DsonColorMaterialChannel):
                if value_socket.type == "VECTOR":
                    value_socket.default_value = channel.value
                else:
                    value_socket.default_value = channel.as_rgba()
            else:
                raise Exception(f"Unsupported channel type: {type(channel)} for socket {value_socket_name}")

        if map_socket_name is not None and channel.has_image():
            image_texture = self._add_image_texture(channel.image_file, non_color_map)
            self._link_socket(image_texture, self.shader_group_node, 0, map_socket_name)

    def _add_image_texture(self, path: str, non_color: bool, tile: int = 1):
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

        self._link_socket(self.mapping_node, tex_image, 0, 0)
        return tex_image

    @staticmethod
    def _set_socket(node: Node, socket: NodeSocket | int | str, value: Any):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        socket_input = node.inputs[socket_key]
        setattr(socket_input, "default_value", value)

    def _link_socket(self,
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
