from bpy.types import ShaderNodeMapping

from .base import ShaderGroupApplier
from .library import PBR_SKIN
from ..utils.dson import DsonMaterialChannel

from ..utils.math import tuple_zip_sum


class PBRSkinShaderGroupApplier(ShaderGroupApplier):
    IN_DIFFUSE_COLOR = "Diffuse Color"
    IN_DIFFUSE_COLOR_MAP = "Diffuse Color Map"
    IN_ROUGHNESS = "Roughness"
    IN_ROUGHNESS_MAP = "Roughness Map"
    IN_METALLIC = "Metallic"
    IN_METALLIC_MAP = "Metallic Map"
    IN_OPACITY = "Opacity"
    IN_OPACITY_MAP = "Opacity Map"

    IN_DLS_WEIGHT = "DLS Weight"
    IN_DLS_WEIGHT_MAP = "DLS Weight Map"
    IN_DLS_REFLECTIVITY = "DLS Reflectivity"
    IN_DLS_REFLECTIVITY_MAP = "DLS Reflectivity Map"
    IN_DLS_ROUGHNESS_MULT = "DLS Roughness Mult"
    IN_DLS_L1_ROUGHNESS = "DLS Lobe 1 Roughness"
    IN_DLS_L1_ROUGHNESS_MAP = "DLS Lobe 1 Roughness Map"
    IN_DLS_L2_ROUGHNESS_MULT = "DLS Lobe 2 Roughness Mult"
    IN_DLS_L2_ROUGHNESS_MULT_MAP = "DLS Lobe 2 Roughness Mult Map"
    IN_DLS_RATIO = "DLS Ratio"
    IN_DLS_RATIO_MAP = "DLS Ratio Map"

    IN_SSS_WEIGHT = "SSS Weight"
    IN_SSS_RADIUS = "SSS Radius"
    IN_SSS_SCALE = "SSS Scale"
    IN_SSS_DIRECTION = "SSS Direction"

    IN_NORMAL_WEIGHT = "Normal Weight"
    IN_NORMAL_MAP = "Normal Map"
    IN_DETAIL_WEIGHT = "Detail Weight"
    IN_DETAIL_WEIGHT_MAP = "Detail Weight Map"
    IN_DETAIL_NORMAL_MAP = "Detail Normal Map"
    IN_BUMP_STRENGTH = "Bump Strength"
    IN_BUMP_STRENGTH_MAP = "Bump Strength Map"

    IN_TOP_COAT_WEIGHT = "Top Coat Weight"
    IN_TOP_COAT_WEIGHT_MAP = "Top Coat Weight Map"
    IN_TOP_COAT_ROUGHNESS = "Top Coat Roughness"
    IN_TOP_COAT_ROUGHNESS_MAP = "Top Coat Roughness Map"
    IN_TOP_COAT_COLOR = "Top Coat Color"
    IN_TOP_COAT_COLOR_MAP = "Top Coat Color Map"

    IN_MAKEUP_WEIGHT = "Makeup Weight"
    IN_MAKEUP_WEIGHT_MAP = "Makeup Weight Map"
    IN_MAKEUP_BASE_COLOR = "Makeup Base Color"
    IN_MAKEUP_BASE_COLOR_MAP = "Makeup Base Color Map"
    IN_MAKEUP_ROUGHNESS_MULT = "Makeup Roughness Mult"
    IN_MAKEUP_ROUGHNESS_MULT_MAP = "Makeup Roughness Mult Map"
    IN_MAKEUP_METALLIC_WEIGHT = "Makeup Metallic Weight"
    IN_MAKEUP_METALLIC_WEIGHT_MAP = "Makeup Metallic Weight Map"
    IN_MAKEUP_REDUCE_NORMALS = "Makeup Reduce Normals"

    @staticmethod
    def group_name() -> str:
        return PBR_SKIN

    @staticmethod
    def material_type_id() -> str:
        return "pbrskin"

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        # @formatter:off
        self._set_material_mapping("horizontal_tiles2", "horizontal_offset2", "vertical_tiles2", "vertical_offset2")

        self._channel_to_sockets('diffuse', self.IN_DIFFUSE_COLOR, self.IN_DIFFUSE_COLOR_MAP, False)

        if self._channel_enabled('diffuse_roughness'):
            # For some reason the diffuse roughness is set to 0 by default.
            # This makes the shader very glossy in Blender, hence we only set it if it's non-zero.
            self._channel_to_sockets('diffuse_roughness', self.IN_ROUGHNESS, self.IN_ROUGHNESS_MAP)

        self._channel_to_sockets('metallic_weight', self.IN_METALLIC, self.IN_METALLIC_MAP)
        self._channel_to_sockets('cutout_opacity', self.IN_OPACITY, self.IN_OPACITY_MAP)

        if self._channel_enabled('dual_lobe_specular_enable'):
            self._channel_to_sockets('dual_lobe_specular_weight', self.IN_DLS_WEIGHT, self.IN_DLS_WEIGHT_MAP)
            if self._properties.dls_weight_multiplier != 1.0:
                self._set_socket(self._shader_group, self.IN_DLS_WEIGHT, self._properties.dls_weight_multiplier, "MULTIPLY")

            self._channel_to_sockets('dual_lobe_specular_reflectivity', self.IN_DLS_REFLECTIVITY, self.IN_DLS_REFLECTIVITY_MAP)
            self._channel_to_sockets('dual_lobe_specular_roughness_mult', self.IN_DLS_ROUGHNESS_MULT, None)
            self._channel_to_sockets('specular_lobe_1_roughness', self.IN_DLS_L1_ROUGHNESS, self.IN_DLS_L1_ROUGHNESS_MAP)
            self._channel_to_sockets('specular_lobe_2_roughness_mult', self.IN_DLS_L2_ROUGHNESS_MULT, self.IN_DLS_L2_ROUGHNESS_MULT_MAP)
            self._channel_to_sockets('dual_lobe_specular_ratio', self.IN_DLS_RATIO, self.IN_DLS_RATIO_MAP)

        if self._channel_enabled('sub_surface_enable'):
            self._channel_to_sockets('translucency_weight', self.IN_SSS_WEIGHT, None)
            self._channel_to_sockets('sss_color', self.IN_SSS_RADIUS, None)
            self._channel_to_sockets('sss_direction', self.IN_SSS_DIRECTION, None)

        self._channel_to_sockets('normal_map', self.IN_NORMAL_WEIGHT, self.IN_NORMAL_MAP)
        if self._properties.pbr_skin_normal_multiplier != 1.0:
            self._set_socket(self._shader_group, self.IN_NORMAL_WEIGHT, self._properties.pbr_skin_normal_multiplier, "MULTIPLY")

        if self._channel_enabled('detail_enable'):
            self._channel_to_sockets('detail_weight', self.IN_DETAIL_WEIGHT, self.IN_DETAIL_WEIGHT_MAP)
            detail_map_tex_node = self._channel_to_sockets('detail_normal_map', None, self.IN_DETAIL_NORMAL_MAP)
            if self._properties.pbr_skin_normal_multiplier != 1.0:
                self._set_socket(self._shader_group, self.IN_DETAIL_WEIGHT, self._properties.pbr_skin_normal_multiplier, "MULTIPLY")

            # Only apply mapping if tiling is enabled for this node
            detail_mapping_ids = ["detail_horizontal_tiles", "detail_horizontal_offset", "detail_vertical_tiles", "detail_vertical_offset"]
            if detail_map_tex_node and self._channel_enabled(*detail_mapping_ids):
                detail_mapping_node_loc = tuple_zip_sum((0, self.mapping_node_location_offset), self._mapping.location.to_tuple())
                detail_mapping_node = self._add_node(ShaderNodeMapping, "Detail Mapping", detail_mapping_node_loc, props={"vector_type": "POINT", "hide": True})
                self._link_socket(self._uv_map, detail_mapping_node, 0, 0)
                self._link_socket(detail_mapping_node, detail_map_tex_node, 0, 0)
                self._set_material_mapping(*detail_mapping_ids, mapping_node=detail_mapping_node)

        if self._channel_enabled('bump_enable'):
            self._channel_to_sockets('bump_strength', self.IN_BUMP_STRENGTH, self.IN_BUMP_STRENGTH_MAP)
            self._set_socket(self._shader_group, self.IN_BUMP_STRENGTH, self._properties.bump_strength_multiplier, "MULTIPLY")

        if self._channel_enabled('top_coat_enable'):
            self._channel_to_sockets('top_coat_weight', self.IN_TOP_COAT_WEIGHT, self.IN_TOP_COAT_WEIGHT_MAP)
            self._channel_to_sockets('top_coat_roughness', self.IN_TOP_COAT_ROUGHNESS, self.IN_TOP_COAT_ROUGHNESS_MAP)
            self._channel_to_sockets('top_coat_color', self.IN_TOP_COAT_COLOR, self.IN_TOP_COAT_COLOR_MAP, False)

        if self._channel_enabled('makeup_enable'):
            self._channel_to_sockets('makeup_weight', self.IN_MAKEUP_WEIGHT, self.IN_MAKEUP_WEIGHT_MAP)
            self._channel_to_sockets('makeup_base_color', self.IN_MAKEUP_BASE_COLOR, self.IN_MAKEUP_BASE_COLOR_MAP, False)
            self._channel_to_sockets('makeup_roughness_mult', self.IN_MAKEUP_ROUGHNESS_MULT, self.IN_MAKEUP_ROUGHNESS_MULT_MAP)
        # @formatter:on
