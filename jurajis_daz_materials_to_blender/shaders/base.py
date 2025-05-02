from __future__ import annotations

import os
from typing import Literal, Any, Type, TypeVar, Callable

import bpy
from bpy.types import Object as BObject, ShaderNodeTree, Node, NodeSocket, \
    ShaderNodeTexImage, NodeSocketVector, NodeSocketColor, NodeSocketFloat, ShaderNodeGroup, ShaderNodeMapping, \
    ShaderNodeUVMap, ShaderNodeOutputMaterial

from ..properties import MaterialImportProperties
from ..utils.dson import DsonMaterialChannel, DsonFloatMaterialChannel, DsonColorMaterialChannel, \
    DsonBoolMaterialChannel
from ..utils.math import tuple_zip_mult
from ..utils.slugify import slugify

_TNode = TypeVar('_TNode', bound=Node)


class ShaderGroupApplier:
    group_node_width = 400
    texture_node_location_x = -915
    texture_node_location_y_inital = 0
    texture_node_location_y_offset = 50
    mapping_node_location_offset = -50
    uv_map_location = (-1505, 0)
    mapping_location = (-1230, 0)
    node_group_location = (-515, 0)
    material_output_location = (0, 0)
    output_socket_map = {
        "Surface": 0,
        "Volume": 1,
        "Displacement": 2,
    }

    daz_color_correction_curve = (
        2.1975328999518102,
        2.2044513091402127,
        2.205027676463837,
    )

    @staticmethod
    def group_name() -> str:
        raise NotImplementedError()

    @staticmethod
    def material_type_id() -> str:
        raise NotImplementedError()

    def __init__(self,
                 properties: MaterialImportProperties,
                 b_object: BObject,
                 node_tree: ShaderNodeTree):
        super().__init__()
        self._properties = properties
        self._b_object = b_object
        self._node_tree = node_tree

        self._texture_node_location_y_current = self.texture_node_location_y_inital

        self._uv_map: ShaderNodeUVMap | None = None
        self._mapping: ShaderNodeMapping | None = None
        self._material_ouput: ShaderNodeOutputMaterial | None = None
        self._shader_group: ShaderNodeGroup | None = None
        self._channels: dict[str, DsonMaterialChannel] = {}

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        self._uv_map = self._add_node(ShaderNodeUVMap, "UV Map", self.uv_map_location,
                                      props={"from_instancer": False, "uv_map": "UVMap"})
        self._mapping = self._add_node(ShaderNodeMapping, "Mapping", self.mapping_location,
                                       props={"vector_type": "POINT", "hide": True})
        self._material_ouput = self._add_node(ShaderNodeOutputMaterial, "Material Output",
                                              self.material_output_location,
                                              props={"is_active_output": True, "target": "ALL"})
        self._link_socket(self._uv_map, self._mapping, 0, 0)

        self._shader_group = self._add_node(ShaderNodeGroup, self.group_name(), self.node_group_location, props={
            "width": self.group_node_width,
            "node_tree": bpy.data.node_groups[self.group_name()]
        })

        for out_sock in self._shader_group.outputs:
            target_sock = self.output_socket_map.get(out_sock.name)
            if target_sock is None:
                raise Exception(
                    f"Output socket {out_sock.name} in group {self.group_name()} has no target socket in Material Output.")

            self._link_socket(self._shader_group, self._material_ouput, out_sock, target_sock)

        self._channels = channels

    def _channel_value(
            self,
            channel_id: str,
            check_set: bool = True,
            transform: Callable[[DsonMaterialChannel], Any] | None = None) -> Any | None:
        ch = self._channels.get(channel_id)
        if ch is None:
            return None
        elif not check_set or ch.is_set():
            if transform is not None:
                return transform(ch)
            else:
                return ch.value
        else:
            return ch.default_value

    def _channel_enabled(self, *feat_names: str) -> bool:
        for feat_name in feat_names:
            channel = self._channels.get(feat_name)
            if not channel:
                continue
            if isinstance(channel, DsonBoolMaterialChannel) and channel.value:
                return True
            elif channel.is_set():
                return True
        return False

    def _channel_to_sockets(self,
                            channel_id: str,
                            value_socket_name: str | None,
                            map_socket_name: str | None,
                            non_color_map: bool = True,
                            force_new_image_node: bool = False) -> ShaderNodeTexImage | None:
        channel = self._channels.get(channel_id, None)
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
                            value_socket.default_value = self._correct_color(c.as_rgba())
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
        node.name = slugify(node_type_id, label)
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

    def _set_socket(
            self,
            node: Node,
            socket: NodeSocket | int | str,
            value: Any,
            op: Literal["SET", "MULTIPLY"] = "SET"):
        socket_key = socket.name if isinstance(socket, NodeSocket) else socket
        socket_input = node.inputs[socket_key]

        match op:
            case "SET":
                match socket_input:
                    case NodeSocketColor():
                        value = self._correct_color(value)
                        setattr(socket_input, "default_value", value)
                    case _:
                        setattr(socket_input, "default_value", value)
            case "MULTIPLY":
                match socket_input:
                    case NodeSocketFloat():
                        sock_value = getattr(socket_input, "default_value", 1.0)
                        setattr(socket_input, "default_value", sock_value * value)
                    case NodeSocketColor():
                        base = (1.0, 1.0, 1.0, 1.0)
                        sock_value = getattr(socket_input, "default_value", base)
                        value = self._correct_color(value)
                        setattr(socket_input, "default_value", tuple_zip_mult(base, sock_value, value))
                    case NodeSocketVector():
                        base = (1.0, 1.0, 1.0)
                        sock_value = getattr(socket_input, "default_value", base)
                        setattr(socket_input, "default_value", tuple_zip_mult(base, sock_value, value))
                    case _:
                        raise Exception(f"Can not use MULITPLY of socket of type: {type(socket_input)}")

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

    def _correct_color(self, rgba: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        if self._properties.apply_color_corrections:
            r, g, b, a = rgba
            cr, cg, cb = self.daz_color_correction_curve
            return r ** cr, g ** cg, b ** cb, a
        else:
            return rgba
