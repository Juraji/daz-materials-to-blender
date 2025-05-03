from bpy.types import ShaderNodeAttribute

from .shader_group_applier import (ShaderGroupApplier)
from .library import BLENDED_DUAL_LOBE_HAIR
from ..utils.dson import DsonChannel


class BlendedDualLobeHairShaderApplier(ShaderGroupApplier):
    ATTRIB__ROOT_TO_TIP_GRADIENT = "blended_dual_lobe_hair_root_to_tip_gradient"

    # Diffuse Reflection
    IN_HAIR_ROOT_COLOR = "Hair Root Color"
    IN_HAIR_ROOT_COLOR_MAP = "Hair Root Color Map"
    IN_HAIR_TIP_COLOR = "Hair Tip Color"
    IN_HAIR_TIP_COLOR_MAP = "Hair Tip Color Map"
    IN_GLOSSY_LAYER_WEIGHT = "Glossy Layer Weight"
    IN_GLOSSY_LAYER_WEIGHT_MAP = "Glossy Layer Weight Map"
    IN_ROUGHNESS = "Roughness"
    IN_ROUGHNESS_MAP = "Roughness Map"

    # Heighlight Reflection
    IN_HIGHLIGHT_WEIGHT = "Highlight Weight"
    IN_HIGHLIGHT_WEIGHT_MAP = "Highlight Weight Map"
    IN_HIGHLIGHT_ROOT_COLOR = "Highlight Root Color"
    IN_HIGHLIGHT_ROOT_COLOR_MAP = "Highlight Root Color Map"
    IN_TIP_HIGHLIGHT_COLOR = "Tip Highlight Color"
    IN_TIP_HIGHLIGHT_COLOR_MAP = "Tip Highlight Color Map"
    IN_HIGHLIGHT_ROUGHNESS = "Highlight Roughness"
    IN_HIGHLIGHT_ROUGHNESS_MAP = "Highlight Roughness Map"

    # Blend
    IN_REDNESS_BIAS = "Redness Bias"
    IN_ROOT_TO_TIP_BIAS = "Root To Tip Bias"
    IN_ROOT_TO_TIP_GAIN = "Root to Tip Gain"
    IN_HIGHLIGHT_SEPARATION = "Highlight Separation"
    IN_HIGHLIGHT_SEPARATION_MAP = "Highlight Separation Map"

    # Bump
    IN_NORMAL = "Normal"
    IN_NORMAL_MAP = "Normal Map"
    IN_BUMP_STRENGTH = "Bump Strength"
    IN_BUMP_STRENGTH_MAP = "Bump Strength Map"

    # Geometry
    IN_ROOT_TO_TIP_GEOMETRY_DATA = "Root to Tip Geometry Data"
    IN_CUTOUT_OPACITY = "Cutout Opacity"
    IN_CUTOUT_OPACITY_MAP = "Cutout Opacity Map"
    IN_DISPLACEMENT_STRENGTH = "Displacement Strength"
    IN_DISPLACEMENT_STRENGTH_MAP = "Displacement Strength Map"
    IN_MINIMUM_DISPLACEMENT = "Minimum Displacement"
    IN_MAXIMUM_DISPLACEMENT = "Maximum Displacement"

    @staticmethod
    def group_name() -> str:
        return BLENDED_DUAL_LOBE_HAIR

    @staticmethod
    def material_type_id() -> str:
        return "blended_dual_lobe_hair"

    def apply_shader_group(self, channels: dict[str, DsonChannel]):
        super().apply_shader_group(channels)

        self._calculate_and_set_root_to_tip_gradient_attribute()

        # @formatter:off
        attribute_props = {"attribute_type": "GEOMETRY",
                           "attribute_name": "blended_dual_lobe_hair_root_to_tip_gradient"}
        node_root_to_tip_attribute = self._add_node(ShaderNodeAttribute, self.IN_ROOT_TO_TIP_GEOMETRY_DATA,
                                                    (self.uv_map_location[0], -120), props=attribute_props)
        self._link_socket(node_root_to_tip_attribute, self._shader_group, 0, self.IN_ROOT_TO_TIP_GEOMETRY_DATA)

        if self._channel_enabled("root_transmission_color") or self._channel_enabled("tip_transmission_color"):
            self._channel_to_sockets("root_transmission_color", self.IN_HAIR_ROOT_COLOR, self.IN_HAIR_ROOT_COLOR_MAP)
            self._channel_to_sockets("tip_transmission_color", self.IN_HAIR_TIP_COLOR, self.IN_HAIR_TIP_COLOR_MAP)

            value = self._channel_value("hair_root_color", False, lambda c: c.as_rgba())
            self._set_socket(self._shader_group, self.IN_HAIR_ROOT_COLOR, value, "MULTIPLY")
            value = self._channel_value("hair_tip_color", False, lambda c: c.as_rgba())
            self._set_socket(self._shader_group, self.IN_HAIR_TIP_COLOR, value, "MULTIPLY")
        else:
            self._channel_to_sockets("hair_root_color", self.IN_HAIR_ROOT_COLOR, self.IN_HAIR_ROOT_COLOR_MAP)
            self._channel_to_sockets("hair_tip_color", self.IN_HAIR_TIP_COLOR, self.IN_HAIR_TIP_COLOR_MAP)

        current_root_color = self._socket_value(self.IN_HAIR_ROOT_COLOR)
        current_tip_color = self._socket_value(self.IN_HAIR_TIP_COLOR)
        redness_bias = self._calculate_redness_bias(current_root_color, current_tip_color)
        self._set_socket(self._shader_group, self.IN_REDNESS_BIAS, redness_bias)

        self._channel_to_sockets("glossy_layer_weight", self.IN_GLOSSY_LAYER_WEIGHT, self.IN_GLOSSY_LAYER_WEIGHT_MAP)
        self._channel_to_sockets("base_roughness", self.IN_ROUGHNESS, self.IN_ROUGHNESS_MAP)

        self._channel_to_sockets("highlight_weight", self.IN_HIGHLIGHT_WEIGHT, self.IN_HIGHLIGHT_WEIGHT_MAP)
        self._channel_to_sockets("highlight_root_color", self.IN_HIGHLIGHT_ROOT_COLOR, self.IN_HIGHLIGHT_ROOT_COLOR_MAP)
        self._channel_to_sockets("tip_highlight_color", self.IN_TIP_HIGHLIGHT_COLOR, self.IN_TIP_HIGHLIGHT_COLOR_MAP)
        self._channel_to_sockets("highlight_roughness", self.IN_HIGHLIGHT_ROUGHNESS, self.IN_HIGHLIGHT_ROUGHNESS_MAP)

        self._channel_to_sockets("root_to_tip_bias", self.IN_ROOT_TO_TIP_BIAS, None)
        self._channel_to_sockets("root_to_tip_gain", self.IN_ROOT_TO_TIP_GAIN, None)
        self._channel_to_sockets("separation", self.IN_HIGHLIGHT_SEPARATION, self.IN_HIGHLIGHT_SEPARATION_MAP)

        self._channel_to_sockets("bump_strength", self.IN_BUMP_STRENGTH, self.IN_BUMP_STRENGTH_MAP)
        self._channel_to_sockets("cutout_opacity", self.IN_CUTOUT_OPACITY, self.IN_CUTOUT_OPACITY_MAP)
        # @formatter:on

    def _calculate_and_set_root_to_tip_gradient_attribute(self):
        import bpy
        import bmesh
        obj = self._b_object

        if self.ATTRIB__ROOT_TO_TIP_GRADIENT in obj.data.attributes:
            # Attribute already exists, skip
            return

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        try:
            bm = bmesh.from_edit_mesh(obj.data)

            # Ensure we have UVs
            uv_layer = bm.loops.layers.uv.get(self._uv_map.uv_map)
            if not uv_layer:
                raise ValueError(f"UV layer not found.")

            # Prepare the attribute to store the normalized value
            attr_layer = bm.verts.layers.float.new(self.ATTRIB__ROOT_TO_TIP_GRADIENT)

            # Tag all faces as unvisited
            for f in bm.faces:
                f.tag = False

            # Process all islands
            for face in bm.faces:
                if not face.tag:
                    island_faces = self.collect_island(uv_layer, face)

                    # Collect all UV Y coords in this island
                    uvs_y = []
                    for f in island_faces:
                        for loop in f.loops:
                            uvs_y.append(loop[uv_layer].uv.y)

                    if not uvs_y:
                        continue

                    min_y = min(uvs_y)
                    max_y = max(uvs_y)
                    range_y = max_y - min_y if (max_y - min_y) != 0 else 1e-6  # Prevent divide by zero

                    # Set normalized Y into vertex attribute
                    for f in island_faces:
                        for loop in f.loops:
                            vert = loop.vert
                            uv_y = loop[uv_layer].uv.y
                            normalized = (uv_y - min_y) / range_y
                            vert[attr_layer] = normalized

            # Update mesh
            bmesh.update_edit_mesh(obj.data)
        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def collect_island(uv_layer, seed_face):
        stack = [seed_face]
        seed_face.tag = True
        island_faces = [seed_face]

        while stack:
            face = stack.pop()
            for edge in face.edges:
                linked_faces = [f for f in edge.link_faces if not f.tag]
                for linked_face in linked_faces:
                    # Check if UVs match across the edge (continuous UV seam check)
                    matching = True
                    for l1, l2 in zip(face.loops, linked_face.loops):
                        uv1 = l1[uv_layer].uv
                        uv2 = l2[uv_layer].uv
                        if (l1.vert == l2.vert) and (uv1 - uv2).length > 1e-5:
                            matching = False
                            break
                    if matching:
                        linked_face.tag = True
                        island_faces.append(linked_face)
                        stack.append(linked_face)
        return island_faces

    @staticmethod
    def _calculate_redness_bias(current_root_color, current_tip_color):
        rr, rg, rb, _ = current_root_color
        tr, tg, tb, _ = current_tip_color

        avg_r = ((rr + tr) / 2)
        avg_g = ((rg + tb) / 2)
        avg_b = ((rb + tb) / 2)
        gamma = 0.8


        return max(0.0, avg_r - (avg_g + avg_b) / 2) ** gamma / (avg_r ** gamma + 1e-5)
