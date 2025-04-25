from __future__ import annotations

import os
from collections.abc import Callable
from datetime import datetime
from typing import Literal, Any, Type, TypeVar

import bpy
from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node, NodeTree, NodeTreeInterfacePanel, NodeSocket, \
    NodeTreeInterfaceSocket, ShaderNodeTexImage, NodeSocketVector, NodeSocketColor, NodeSocketFloat, NodeReroute, \
    NodeFrame, NodeGroupInput, NodeGroupOutput, ShaderNodeHueSaturation, ShaderNodeMix, ShaderNodeMixShader, \
    ShaderNodeMath, ShaderNodeVectorMath, ShaderNodeNormalMap, ShaderNodeBump, ShaderNodeBsdfPrincipled, ShaderNodeGroup

from ...properties import MaterialImportProperties
from ...utils.dson import DsonMaterialChannel, DsonFloatMaterialChannel, DsonColorMaterialChannel, \
    DsonBoolMaterialChannel
from ...utils.slugify import slugify

_TNode = TypeVar('_TNode', bound=Node)
_RerouteNodeGenerator = Callable[[tuple[float, float], NodeFrame | None], NodeReroute]

GROUP_DESCRIPTION_PREFIX = "Created by DAZ Material Importer"


class _GroupNameMixin:
    @staticmethod
    def group_name() -> str:
        raise NotImplementedError()


class _MaterialTypeIdMixin:
    @staticmethod
    def material_type_id() -> str:
        raise NotImplementedError()


class RerouteGroup:

    def __init__(self,
                 location_x: float,
                 location_y: float,
                 parent: NodeFrame | None = None,
                 offset: float = 20.0):
        self.location_x = location_x
        self.location_y = location_y
        self.parent = parent
        self.offset = offset
        self._counter = 0
        self.node_register: dict[NodeSocket, NodeReroute] = {}

    def reroute_node_by_source_socket(self,
                                      source_socket: NodeSocket,
                                      generator: _RerouteNodeGenerator) -> NodeReroute | None:
        """
        Get the existing node or use the generator to create and register a new node for the source socket.
        :param source_socket: The source/origin socket for this reroute.
        :param generator: A callable that accepts the next node position and an optional parent and returns a new reroute node.
        :return: The reroute node from the register or the newly generated node.
        """
        if source_socket in self.node_register:
            return self.node_register[source_socket]
        else:
            node = generator(self._next_position(), self.parent)
            self.node_register[source_socket] = node
            return node

    def _next_position(self) -> tuple[float, float]:
        y = self.location_y
        y -= self.offset * self._counter

        self._counter += 1
        return self.location_x, y


class ShaderGroupBuilder(_GroupNameMixin, _MaterialTypeIdMixin):
    group_node_width = 400

    @staticmethod
    def depends_on() -> set[Type[ShaderGroupBuilder]]:
        return set()

    @staticmethod
    def is_support() -> bool:
        return False

    def __init__(self, properties: MaterialImportProperties, node_trees: BlendDataNodeTrees):
        super().__init__()
        self.properties: MaterialImportProperties = properties
        self.node_trees: BlendDataNodeTrees = node_trees
        self.node_group: NodeTree | None = None

    def setup_group(self):
        # noinspection PyTypeChecker
        self.node_group = self.node_trees.new(type="ShaderNodeTree", name=self.group_name())
        self.node_group.color_tag = "SHADER"
        self.node_group.description = f"{GROUP_DESCRIPTION_PREFIX} at {datetime.now()}"
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

    def _bool_socket(self,
                     name: str,
                     default_value: bool = False,
                     in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                     parent: NodeTreeInterfacePanel = None,
                     props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self._add_socket("NodeSocketBool", name, default_value, in_out, parent, props)

    @staticmethod
    def _set_socket(node: Node,
                    socket: NodeSocket | int,
                    value: Any,
                    in_out: Literal["INPUT", "OUTPUT"] = "INPUT", ):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        if in_out == "INPUT":
            socket_input = node.inputs[socket_key]
        else:
            socket_input = node.outputs[socket_key]
        setattr(socket_input, "default_value", value)

    def _link_socket(self,
                     source: Node,
                     target: Node,
                     source_socket: NodeTreeInterfaceSocket | NodeSocket | int | str,
                     target_socket: NodeTreeInterfaceSocket | NodeSocket | int | str,
                     group: RerouteGroup | tuple[RerouteGroup, ...] | None = None):

        match source_socket:
            case int() | str():
                r_source_socket = source.outputs[source_socket]
            case NodeTreeInterfaceSocket() | NodeSocket():
                r_source_socket = source.outputs[source_socket.name]
            case _:
                raise Exception(f"Unknown source socket type {type(source_socket)} ({source.name}[{source_socket}])")
        match target_socket:
            case int() | str():
                r_target_socket = target.inputs[target_socket]
            case NodeTreeInterfaceSocket() | NodeSocket():
                r_target_socket = target.inputs[target_socket.name]
            case _:
                raise Exception(f"Unknown target socket type {type(target_socket)} ({target.name}[{target_socket}])")

        match group:
            case None:  # No Reroute Group
                self.node_group.links.new(r_source_socket, r_target_socket)
            case RerouteGroup():  # Single Reroute Group
                node_reroute = group.reroute_node_by_source_socket(
                    r_source_socket, lambda pos, parent: self._add_node__reroute(pos, parent))
                self._link_socket(source, node_reroute, source_socket, 0)
                self._link_socket(node_reroute, target, 0, target_socket)
                return
            case tuple():  # Reroute Group chain
                prev_node = source
                prev_socket = source_socket

                for reroute_group in group:
                    node_reroute = reroute_group.reroute_node_by_source_socket(
                        r_source_socket, lambda pos, parent: self._add_node__reroute(pos, parent))
                    self._link_socket(prev_node, node_reroute, prev_socket, 0)
                    prev_node = node_reroute
                    prev_socket = node_reroute.outputs[0]

                self._link_socket(prev_node, target, prev_socket, target_socket)
                return

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
            if hasattr(sock, prop):
                setattr(sock, prop, value)

        return sock

    # Nodes
    def _add_panel(self, name: str,
                   default_closed: bool = True) -> NodeTreeInterfacePanel:
        return self.node_group.interface.new_panel(name, default_closed=default_closed)

    def _add_frame(self, label: str):
        return self._add_node(NodeFrame, label, (0, 0))

    def _add_node__group_input(self,
                               label: str,
                               location: tuple[float, float]):
        return self._add_node(NodeGroupInput, label, location)

    def _add_node__group_output(self,
                                label: str,
                                location: tuple[float, float]):
        out = self._add_node(NodeGroupOutput, label, location)
        out.is_active_output = True
        return out

    def _add_node__hsv(self,
                       label: str,
                       location: tuple[float, float],
                       parent: Node = None) -> Node:
        return self._add_node(ShaderNodeHueSaturation, label, location, parent)

    def _add_node__mix(self,
                       label: str,
                       location: tuple[float, float],
                       data_type: str = "RGBA",
                       blend_type: str = "MULTIPLY",
                       default_factor: float = 1,
                       parent: Node = None,
                       props: dict[str, Any] = {}) -> Node:
        props = {
            **props,
            "data_type": data_type,
            "blend_type": blend_type,
            "clamp_factor": True,
            "clamp_result": False,
        }
        mix = self._add_node(ShaderNodeMix, label, location, parent, props)
        self._set_socket(mix, 0, default_factor)
        return mix

    def _add_node__mix_shader(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}) -> Node:
        return self._add_node(ShaderNodeMixShader, label, location, parent, props)

    def _add_node__math(self,
                        label: str,
                        location: tuple[float, float],
                        operation: str = "ADD",
                        parent: Node = None,
                        props: dict[str, Any] = {}) -> Node:
        props = {**props, "operation": operation}
        return self._add_node(ShaderNodeMath, label, location, parent, props)

    def _add_node__math_vector(self,
                               label: str,
                               location: tuple[float, float],
                               operation: str = "ADD",
                               parent: Node = None,
                               props: dict[str, Any] = {}) -> Node:
        props = {**props, "operation": operation}
        return self._add_node(ShaderNodeVectorMath, label, location, parent, props=props)

    def _add_node__normal_map(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}):
        return self._add_node(ShaderNodeNormalMap, label, location, parent, props)

    def _add_node__bump(self,
                        label: str,
                        location: tuple[float, float],
                        parent: Node = None,
                        props: dict[str, Any] = {}):
        return self._add_node(ShaderNodeBump, label, location, parent, props)

    def _add_node__princ_bdsf(self,
                              label: str,
                              location: tuple[float, float],
                              parent: Node = None,
                              props: dict[str, Any] = {}):
        return self._add_node(ShaderNodeBsdfPrincipled, label, location, parent, props)

    def _add_node__shader_group(self,
                                label: str,
                                builder: Type[ShaderGroupBuilder],
                                location: tuple[float, float],
                                parent: Node = None,
                                props: dict[str, Any] = {}):
        props = {**props, "node_tree": self.node_trees[builder.group_name()], "width": self.group_node_width}
        return self._add_node(ShaderNodeGroup, label, location, parent, props)

    def _add_node__reroute(self,
                           location: tuple[float, float],
                           parent: Node = None):
        return self._add_node(NodeReroute, "", location, parent)

    def _add_node(self,
                  node_type: Type[_TNode],
                  label: str,
                  location: tuple[float, float],
                  parent: Node = None,
                  props: dict[str, Any] = {}) -> _TNode:
        node_type_id = getattr(getattr(node_type, "bl_rna", None), "identifier", None)
        if node_type_id is None:
            raise TypeError(f"Cannot resolve bl_idname for type: {node_type.__name__}")

        node = self.node_group.nodes.new(node_type_id)
        node.label = label
        node.name = slugify(node_type_id, label)
        node.parent = parent
        node.location = location

        # Set props
        for prop, value in props.items():
            if hasattr(node, prop):
                setattr(node, prop, value)

        return node

    def hide_all_nodes(self, *exempt_nodes: Node):
        nodes_to_hide = [n for n in self.node_group.nodes if not n in exempt_nodes]

        for n in nodes_to_hide:
            n.hide = True


class SupportShaderGroupBuilder(ShaderGroupBuilder):
    @staticmethod
    def is_support() -> bool:
        return True


class ShaderGroupApplier(_GroupNameMixin, _MaterialTypeIdMixin):
    group_node_width = 400
    texture_node_location_x = -915
    texture_node_location_y_inital = 0
    texture_node_location_y_offset = 50
    uv_map_location = (-1505, 0)
    mapping_location = (-1230, 0)
    node_group_location = (-515, 0)
    material_output_location = (0, 0)
    output_socket_map = {
        "Surface": 0,
        "Volume": 1,
        "Displacement": 2,
    }

    def __init__(self,
                 properties: MaterialImportProperties,
                 node_tree: ShaderNodeTree):
        super().__init__()
        self._properties = properties
        self._node_tree = node_tree

        self._texture_node_location_y_current = self.texture_node_location_y_inital

        self._uv_map: Node | None = None
        self._mapping: Node | None = None
        self._material_ouput: Node | None = None
        self._shader_group: Node | None = None
        self._channels: dict[str, DsonMaterialChannel] = {}

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        mapping = self._node_tree.nodes.new("ShaderNodeMapping")
        mapping.name = "Mapping"
        mapping.vector_type = 'POINT'
        mapping.hide = True
        mapping.location = self.mapping_location
        self._mapping = mapping

        # node UV Map
        uv_map = self._node_tree.nodes.new("ShaderNodeUVMap")
        uv_map.name = "UV Map"
        uv_map.from_instancer = False
        uv_map.uv_map = "UVMap"
        uv_map.location = self.uv_map_location
        self._link_socket(uv_map, mapping, 0, 0)
        self._uv_map = uv_map

        material_output = self._node_tree.nodes.new("ShaderNodeOutputMaterial")
        material_output.name = "Material Output"
        material_output.is_active_output = True
        material_output.target = 'ALL'
        material_output.location = self.material_output_location
        self._material_ouput = material_output

        shader_group = self._node_tree.nodes.new("ShaderNodeGroup")
        shader_group.label = self.group_name()
        shader_group.name = slugify(self.group_name())
        shader_group.location = self.node_group_location
        shader_group.width = self.group_node_width
        shader_group.node_tree = bpy.data.node_groups[self.group_name()]

        for out_sock in shader_group.outputs:
            target_sock = self.output_socket_map.get(out_sock.name)
            if target_sock is None:
                raise Exception(
                    f"Output socket {out_sock.name} in group {self.group_name()} has no target socket in Material Output.")

            self._link_socket(shader_group, self._material_ouput, out_sock, target_sock)

        self._shader_group = shader_group
        self._channels = channels

    def _channel_enabled(self, *feat_names: str) -> bool:
        for feat_name in feat_names:
            channel = self._channels.get(feat_name)
            if not channel:
                continue
            if isinstance(channel, DsonBoolMaterialChannel):
                return channel.value
            else:
                return channel.is_set()
        return False

    def _channel_to_sockets(self,
                            channel_id: str,
                            value_socket_name: str | None,
                            map_socket_name: str | None,
                            non_color_map: bool = True,
                            force_new_image_node: bool = False) -> ShaderNodeTexImage | None:
        channel = self._channels.get(channel_id)
        if channel is None:
            return None

        if value_socket_name and value_socket_name in self._shader_group.inputs:
            value_socket = self._shader_group.inputs[value_socket_name]

            match channel:
                case DsonFloatMaterialChannel() | DsonBoolMaterialChannel():
                    value_socket.default_value = channel.value or 0
                case DsonColorMaterialChannel() as c:
                    match value_socket:
                        case NodeSocketColor():
                            value_socket.default_value = c.as_rgba()
                        case NodeSocketVector():
                            value_socket.default_value = c.value
                        case _:
                            value_socket.default_value = c.as_float()
                case _:
                    raise Exception(f"Unsupported channel type: {type(channel)} for socket '{value_socket_name}'")

        image_texture: ShaderNodeTexImage | None = None
        if map_socket_name and channel.has_image():
            image_texture = self._add_image_texture(channel.image_file, non_color_map, force_new_image_node)
            self._link_socket(self._mapping, image_texture, 0, 0)
            self._link_socket(image_texture, self._shader_group, 0, map_socket_name)

        return image_texture

    def _add_image_texture(self, path: str, non_color: bool, force_new_node: bool = False) -> ShaderNodeTexImage:
        img_name = os.path.basename(path)

        if not force_new_node:
            for node in self._node_tree.nodes:
                if isinstance(node, ShaderNodeTexImage) and node.image and node.image.name == img_name:
                    return node

        image = bpy.data.images.load(path, check_existing=True)
        # noinspection PyTypeChecker
        image.colorspace_settings.name = "Non-Color" if non_color else "sRGB"

        return self._add_node(
            ShaderNodeTexImage,
            img_name,
            self._next_image_node_location(),
            props={
                "image": image,
                "hide": True
            }
        )

    def _next_image_node_location(self):
        loc = (self.texture_node_location_x, self._texture_node_location_y_current)
        self._texture_node_location_y_current -= self.texture_node_location_y_offset
        return loc

    def _add_node(self,
                  node_type: Type[_TNode],
                  label: str,
                  location: tuple[float, float],
                  parent: Node = None,
                  props: dict[str, Any] = {}) -> _TNode:
        node_type_id = getattr(getattr(node_type, "bl_rna", None), "identifier", None)
        if node_type_id is None:
            raise TypeError(f"Cannot resolve bl_idname for type: {node_type.__name__}")

        node = self._node_tree.nodes.new(node_type_id)
        node.label = label
        node.name = slugify(self.group_name(), node_type_id, label)
        node.parent = parent
        node.location = location

        # Set props
        for prop, value in props.items():
            if hasattr(node, prop):
                setattr(node, prop, value)

        return node

    def _set_material_mapping(self,
                              horizontal_tiling_channel_id: str,
                              horizontal_offset_channel_id: str,
                              vertical_tiling_channel_id: str,
                              vertical_offset_channel_id: str,
                              mapping_node: Node | None = None):

        mapping_node = mapping_node or self._mapping

        if horizontal_offset_channel_id in self._channels:
            scale = self._channels[horizontal_offset_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[1].default_value[0] = scale

        if vertical_offset_channel_id in self._channels:
            scale = self._channels[vertical_offset_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[1].default_value[1] = scale

        if horizontal_tiling_channel_id in self._channels:
            scale = self._channels[horizontal_tiling_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[3].default_value[0] = scale

        if vertical_tiling_channel_id in self._channels:
            scale = self._channels[vertical_tiling_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[3].default_value[1] = scale

    @staticmethod
    def _set_socket(
            node: Node,
            socket: NodeSocket | int | str,
            value: Any,
            op: Literal["SET", "MULTIPLY"] = "SET"):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        socket_input = node.inputs[socket_key]

        match op:
            case "SET":
                setattr(socket_input, "default_value", value)
            case "MULTIPLY":
                sock_value = getattr(socket_input, "default_value", 0)
                if not isinstance(socket_input, NodeSocketFloat):
                    raise Exception(
                        f"Invalid operation {op} using value {value} for socket {socket_key} with value {sock_value}!")
                setattr(socket_input, "default_value", sock_value * value)

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

        self._node_tree.links.new(source_socket, target_socket)
