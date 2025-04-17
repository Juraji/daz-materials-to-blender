import os
from datetime import datetime
from typing import Literal, Any, cast, Self, Type

import bpy
from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node, NodeTree, NodeTreeInterfacePanel, NodeSocket, \
    NodeTreeInterfaceSocket, ShaderNodeTexImage

from ..properties import MaterialImportProperties
from ..utils.dson import DsonMaterialChannel, DsonFloatMaterialChannel, DsonColorMaterialChannel, \
    DsonBoolMaterialChannel
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

    def _bool_socket(self,
                     name: str,
                     default_value: bool = False,
                     in_out: Literal["INPUT", "OUTPUT"] = "INPUT",
                     parent: NodeTreeInterfacePanel = None,
                     props: dict[str, Any] = {}) -> NodeTreeInterfaceSocket:
        return self._add_socket("NodeSocketBool", name, default_value, in_out, parent, props)

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
    def _add_panel(self, name: str,
                   default_closed: bool = True) -> NodeTreeInterfacePanel:
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
                               builder: Type[Self],
                               location: tuple[float, float],
                               parent: Node = None,
                               props: dict[str, Any] = {}):
        props = {**props, "node_tree": bpy.data.node_groups[builder.group_name()]}
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
    __texture_node_location_y_offset: float = 50

    def __init__(self,
                 properties: MaterialImportProperties,
                 node_tree: ShaderNodeTree):
        super().__init__()
        self._properties = properties
        self._node_tree = node_tree

        self._uv_map: Node | None = None
        self._mapping: Node | None = None
        self._material_ouput: Node | None = None
        self._shader_group: Node | None = None
        self._channels: dict[str, DsonMaterialChannel] = {}

    def add_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        mapping = self._node_tree.nodes.new("ShaderNodeMapping")
        mapping.name = "Mapping"
        mapping.vector_type = 'POINT'
        mapping.location = (-1230, 0)
        self._mapping = mapping

        # node UV Map
        uv_map = self._node_tree.nodes.new("ShaderNodeUVMap")
        uv_map.name = "UV Map"
        uv_map.from_instancer = False
        uv_map.uv_map = "UVMap"
        uv_map.location = (-1505, 0)
        self._link_socket(uv_map, mapping, 0, 0)
        self._uv_map = uv_map

        material_output = self._node_tree.nodes.new("ShaderNodeOutputMaterial")
        material_output.name = "Material Output"
        material_output.is_active_output = True
        material_output.target = 'ALL'
        material_output.location = (125, 0)
        self._material_ouput = material_output

        shader_group = self._node_tree.nodes.new("ShaderNodeGroup")
        shader_group.label = self.group_name()
        shader_group.name = slugify(self.group_name())
        shader_group.location = (-415, 0)
        shader_group.width = self.__group_node_width
        shader_group.node_tree = bpy.data.node_groups[self.group_name()]
        self._link_socket(shader_group, self._material_ouput, 0, 0)
        self._shader_group = shader_group

        self._channels = channels

    def align_image_nodes(self):
        tex_nodes = filter(lambda n: n.type == "TEX_IMAGE", self._node_tree.nodes)

        current_y = 0
        for node in tex_nodes:
            node.location = (-915, current_y)
            current_y -= self.__texture_node_location_y_offset

    def _channel_enabled(self, *feat_names: str) -> bool:
        for feat_name in feat_names:
            channel = self._channels.get(feat_name)
            if not channel:
                continue
            val = channel.value
            if isinstance(val, tuple):
                # Enabled if any of the first 3 components are not zero
                if val[:3] != (0.0, 0.0, 0.0):
                    return True
            elif val:
                return True
        return False

    def _channel_to_inputs(self,
                           channel_id: str,
                           value_socket_name: str | None,
                           map_socket_name: str | None,
                           non_color_map: bool = True) -> ShaderNodeTexImage | None:
        if not channel_id in self._channels:
            return None

        channel = self._channels[channel_id]

        if not value_socket_name is None and value_socket_name in self._shader_group.inputs:
            value_socket = self._shader_group.inputs[value_socket_name]

            if isinstance(channel, DsonFloatMaterialChannel):
                value_socket.default_value = channel.value
            elif isinstance(channel, DsonBoolMaterialChannel):
                value_socket.default_value = channel.value
            elif isinstance(channel, DsonColorMaterialChannel):
                if value_socket.type == "VECTOR":
                    value_socket.default_value = channel.value
                else:
                    value_socket.default_value = channel.as_rgba()
            else:
                raise Exception(f"Unsupported channel type: {type(channel)} for socket {value_socket_name}")

        image_texture: ShaderNodeTexImage | None = None
        if map_socket_name is not None and channel.has_image():
            image_texture = self._add_image_texture(channel.image_file, non_color_map)
            self._link_socket(image_texture, self._shader_group, 0, map_socket_name)

        return image_texture

    def _add_image_texture(self, path: str, non_color: bool, tile: int = 1) -> ShaderNodeTexImage:
        tex_image: ShaderNodeTexImage = cast(ShaderNodeTexImage, self._node_tree.nodes.new(type="ShaderNodeTexImage"))
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

        self._link_socket(self._mapping, tex_image, 0, 0)
        return tex_image

    def _add_node(self,
                  node_type: str,
                  label: str,
                  location: tuple[float, float],
                  parent: Node = None,
                  props: dict[str, Any] = {}) -> Node:
        node = self._node_tree.nodes.new(node_type)
        node.label = label
        node.name = slugify(self.group_name(), node_type, label)
        node.parent = parent
        node.location = location

        for prop, value in props.items():
            if hasattr(node, prop):
                setattr(node, prop, value)

        return node

    def _set_material_mapping(self,
                              channels: dict[str, DsonMaterialChannel],
                              horizontal_tiling_channel_id: str,
                              horizontal_offset_channel_id: str,
                              vertical_tiling_channel_id: str,
                              vertical_offset_channel_id: str,
                              mapping_node: Node | None = None):

        mapping_node = mapping_node or self._mapping

        if horizontal_offset_channel_id in channels:
            scale = channels[horizontal_offset_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[1].default_value[0] = scale

        if vertical_offset_channel_id in channels:
            scale = channels[vertical_offset_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[1].default_value[1] = scale

        if horizontal_tiling_channel_id in channels:
            scale = 1 / channels[horizontal_tiling_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[3].default_value[0] = scale

        if vertical_tiling_channel_id in channels:
            scale = 1 / channels[vertical_tiling_channel_id].value
            # noinspection PyUnresolvedReferences
            mapping_node.inputs[3].default_value[1] = scale

        pass

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

        self._node_tree.links.new(source_socket, target_socket)
