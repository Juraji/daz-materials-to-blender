from typing import Type

from bpy.types import ShaderNodeMapping

from .support import ShaderGroupBuilder, ShaderGroupApplier, DualLobeSpecularShaderGroupBuilder, RerouteGroup
from ..utils.b_shaders.principled_bdsf import PrincipledBSDFSockets
from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "PBR Skin"
__MATERIAL_TYPE_ID__ = "pbrskin"

from ..utils.math import tuple_zip_sum


class PBRSkinShaderGroupBuilder(ShaderGroupBuilder):
    in_diffuse_color = "Diffuse Color"
    in_diffuse_color_map = "Diffuse Color Map"
    in_roughness = "Roughness"
    in_roughness_map = "Roughness Map"
    in_metallic = "Metallic"
    in_metallic_map = "Metallic Map"
    in_opacity = "Opacity"
    in_opacity_map = "Opacity Map"

    in_dls_weight = "DLS Weight"
    in_dls_weight_map = "DLS Weight Map"
    in_dls_reflectivity = "DLS Reflectivity"
    in_dls_reflectivity_map = "DLS Reflectivity Map"
    in_dls_roughness_mult = "DLS Roughness Mult"
    in_dls_l1_roughness = "DLS Lobe 1 Roughness"
    in_dls_l1_roughness_map = "DLS Lobe 1 Roughness Map"
    in_dls_l2_roughness_mult = "DLS Lobe 2 Roughness Mult"
    in_dls_l2_roughness_mult_map = "DLS Lobe 2 Roughness Mult Map"
    in_dls_ratio = "DLS Ratio"
    in_dls_ratio_map = "DLS Ratio Map"

    in_sss_weight = "SSS Weight"
    in_sss_radius = "SSS Radius"
    in_sss_scale = "SSS Scale"
    in_sss_direction = "SSS Direction"

    in_normal_weight = "Normal Weight"
    in_normal_map = "Normal Map"
    in_detail_weight = "Detail Weight"
    in_detail_weight_map = "Detail Weight Map"
    in_detail_normal_map = "Detail Normal Map"
    in_bump_strength = "Bump Strength"
    in_bump_strength_map = "Bump Strength Map"

    in_top_coat_weight = "Top Coat Weight"
    in_top_coat_weight_map = "Top Coat Weight Map"
    in_top_coat_roughness = "Top Coat Roughness"
    in_top_coat_roughness_map = "Top Coat Roughness Map"
    in_top_coat_color = "Top Coat Color"
    in_top_coat_color_map = "Top Coat Color Map"

    in_makeup_weight = "Makeup Weight"
    in_makeup_weight_map = "Makeup Weight Map"
    in_makeup_base_color = "Makeup Base Color"
    in_makeup_base_color_map = "Makeup Base Color Map"
    in_makeup_roughness_mult = "Makeup Roughness Mult"
    in_makeup_roughness_mult_map = "Makeup Roughness Mult Map"
    in_makeup_metallic_weight = "Makeup Metallic Weight"
    in_makeup_metallic_weight_map = "Makeup Metallic Weight Map"
    in_makeup_reduce_normals = "Makeup Reduce Normals"

    out_surface = "Surface"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    @staticmethod
    def depends_on() -> set[Type[ShaderGroupBuilder]]:
        return {DualLobeSpecularShaderGroupBuilder}

    def setup_group(self):
        super().setup_group()

        # @formatter:off
        # Panels
        panel_pbr = self._add_panel("PBR", default_closed=False)
        panel_dls = self._add_panel("Dual Lobe Specular")
        panel_sss = self._add_panel("Sub Surface Scattering")
        panel_normals_bump = self._add_panel("Normals and Bump")
        panel_top_coat = self._add_panel("Top Coat")
        panel_makeup = self._add_panel("Makeup")

        # Input Sockets: PBR
        sock_diffuse_color = self._color_socket(self.in_diffuse_color, parent=panel_pbr)
        sock_diffuse_color_map = self._color_socket(self.in_diffuse_color_map, parent=panel_pbr)
        sock_roughness_weight = self._float_socket(self.in_roughness, 1.0, parent=panel_pbr)
        in_roughness_weight_map = self._color_socket(self.in_roughness_map, parent=panel_pbr)
        sock_metallic_weight = self._float_socket(self.in_metallic, parent=panel_pbr)
        sock_metallic_weight_map = self._color_socket(self.in_metallic_map, parent=panel_pbr)
        sock_opacity = self._float_socket(self.in_opacity, 1.0, parent=panel_pbr)
        sock_opacity_map = self._color_socket(self.in_opacity_map, parent=panel_pbr)

        # Input Sockets: DLS
        sock_dls_weight = self._float_socket(self.in_dls_weight, parent=panel_dls)
        sock_dls_weight_map = self._color_socket(self.in_dls_weight_map, parent=panel_dls)
        sock_dls_reflectivity = self._float_socket(self.in_dls_reflectivity, 0.5, parent=panel_dls)
        sock_dls_reflectivity_map = self._color_socket(self.in_dls_reflectivity_map, parent=panel_dls)
        sock_dls_roughness_mult = self._float_socket(self.in_dls_roughness_mult, 1.0, parent=panel_dls)
        sock_dls_l1_roughness = self._float_socket(self.in_dls_l1_roughness, 0.6, parent=panel_dls)
        sock_dls_l1_roughness_map = self._color_socket(self.in_dls_l1_roughness_map, parent=panel_dls)
        sock_dls_l2_roughness_mult = self._float_socket(self.in_dls_l2_roughness_mult, 0.4, parent=panel_dls)
        sock_dls_l2_roughness_mult_map = self._color_socket(self.in_dls_l2_roughness_mult_map, parent=panel_dls)
        sock_dls_ratio = self._float_socket(self.in_dls_ratio, 0.15, parent=panel_dls)
        sock_dls_ratio_map = self._color_socket(self.in_dls_ratio_map, parent=panel_dls)

        # Input Sockets: SSS
        sock_sss_weight = self._float_socket(self.in_sss_weight, 0.8, parent=panel_sss)
        sock_sss_radius = self._vector_socket(self.in_sss_radius, (1.0, 0.2, 0.1), parent=panel_sss)
        sock_sss_scale = self._float_socket(self.in_sss_scale, 0.004, parent=panel_sss, props={"subtype": "DISTANCE"})
        sock_sss_direction = self._float_socket(self.in_sss_direction, 0.8, parent=panel_sss)

        # Input Sockets: Normal/Bump
        sock_normal_weight = self._float_socket(self.in_normal_weight, 1.0, parent=panel_normals_bump)
        sock_normal_map = self._color_socket(self.in_normal_map, (0.5, 0.5, 1.0, 1.0), parent=panel_normals_bump)
        sock_detail_weight = self._float_socket(self.in_detail_weight, parent=panel_normals_bump)
        sock_detail_weight_map = self._color_socket(self.in_detail_weight_map, parent=panel_normals_bump)
        sock_detail_normal_map = self._color_socket(self.in_detail_normal_map, (0.5, 0.5, 1.0, 1.0), parent=panel_normals_bump)
        sock_bump_strength = self._float_socket(self.in_bump_strength, parent=panel_normals_bump)
        sock_bump_strength_map = self._color_socket(self.in_bump_strength_map, parent=panel_normals_bump)

        # Input Sockets: Top Coat
        sock_top_coat_weight = self._float_socket(self.in_top_coat_weight, parent=panel_top_coat)
        sock_top_coat_weight_map = self._color_socket(self.in_top_coat_weight_map, parent=panel_top_coat)
        sock_top_coat_roughness = self._float_socket(self.in_top_coat_roughness, 0.7, parent=panel_top_coat)
        sock_top_coat_roughness_map = self._color_socket(self.in_top_coat_roughness_map, parent=panel_top_coat)
        sock_top_coat_color = self._color_socket(self.in_top_coat_color, parent=panel_top_coat)
        sock_top_coat_color_map = self._color_socket(self.in_top_coat_color_map, parent=panel_top_coat)

        # Input Sockets: Makeup
        sock_makeup_weight = self._float_socket(self.in_makeup_weight, parent=panel_makeup)
        sock_makeup_weight_map = self._color_socket(self.in_makeup_weight_map, parent=panel_makeup)
        sock_makeup_base_color = self._color_socket(self.in_makeup_base_color, parent=panel_makeup)
        sock_makeup_base_color_map = self._color_socket(self.in_makeup_base_color_map, parent=panel_makeup)
        sock_makeup_roughness_mult = self._float_socket(self.in_makeup_roughness_mult, parent=panel_makeup)
        sock_makeup_roughness_mult_map = self._color_socket(self.in_makeup_roughness_mult_map, parent=panel_makeup)
        sock_makeup_metallic_weight = self._float_socket(self.in_makeup_metallic_weight, parent=panel_makeup)
        sock_makeup_metallic_weight_map = self._color_socket(self.in_makeup_metallic_weight_map, parent=panel_makeup)
        sock_makeup_reduce_normals = self._float_socket(self.in_makeup_reduce_normals, parent=panel_makeup)

        # Output Sockets:
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")

        # Frames
        frame_pbr = self._add_frame("PBR and Opacity")
        reroute_pbr_in = RerouteGroup(-2320, 80.0, frame_pbr)
        reroute_pbr_out = RerouteGroup(-1900, 80.0, frame_pbr)

        frame_normal_and_bump = self._add_frame("Normal, Detail and Bump")
        reroute_normal_in = RerouteGroup(-2320, 300.0, frame_normal_and_bump)

        frame_top_coat = self._add_frame("Top Coat")
        reroute_top_coat_in = RerouteGroup(-1620, -740.00, frame_top_coat)
        reroute_top_coat_out = RerouteGroup(-1380, -740.0, frame_top_coat)

        frame_makeup_layer = self._add_frame("Makeup Layer")
        reroute_makeup_in = RerouteGroup(-1620, -940.0, frame_makeup_layer)
        reroute_makeup_out = RerouteGroup(-880, -940.0, frame_makeup_layer)

        reroute_sss_in = RerouteGroup(-1620, -560.0)
        reroute_sss_out = RerouteGroup(-1280, -560.0)

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-2640, 60.0))

        # Nodes: PBR
        node_combine_diffuse = self._add_node__mix("Combine diffuse", (-2280, 80), parent=frame_pbr)
        self._link_socket(node_group_input, node_combine_diffuse, sock_diffuse_color_map, 6, reroute_pbr_in)
        self._link_socket(node_group_input, node_combine_diffuse, sock_diffuse_color, 7, reroute_pbr_in)

        node_combine_roughness = self._add_node__hsv("Combine Roughness", (-2280, 40), frame_pbr)
        self._link_socket(node_group_input, node_combine_roughness, sock_roughness_weight, 2, reroute_pbr_in)
        self._link_socket(node_group_input, node_combine_roughness, in_roughness_weight_map, 4, reroute_pbr_in)

        node_combine_metallic = self._add_node__hsv("Combine Metallic", (-2280, 0), frame_pbr)
        self._link_socket(node_group_input, node_combine_metallic, sock_metallic_weight, 2, reroute_pbr_in)
        self._link_socket(node_group_input, node_combine_metallic, sock_metallic_weight_map, 4, reroute_pbr_in)

        node_combine_opacity = self._add_node__hsv("Combine Opacity", (-2280, -40), frame_pbr)
        self._link_socket(node_group_input, node_combine_opacity, sock_opacity, 2, reroute_pbr_in)
        self._link_socket(node_group_input, node_combine_opacity, sock_opacity_map, 4, reroute_pbr_in)

        # Nodes: Normal/Bump
        node_normal_map = self._add_node__normal_map("Normal Map", (-2280, 320.0), frame_normal_and_bump)
        self._link_socket(node_group_input, node_normal_map, sock_normal_weight, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_normal_map, sock_normal_map, 1, reroute_normal_in)

        node_combine_detail_weight = self._add_node__hsv("Combine Detail Weight", (-2280, 280.0), frame_normal_and_bump)
        self._link_socket(node_group_input, node_combine_detail_weight, sock_detail_weight, 2, reroute_normal_in)
        self._link_socket(node_group_input, node_combine_detail_weight, sock_detail_weight_map, 4, reroute_normal_in)

        node_detail_normal_map = self._add_node__normal_map("Detail Normal Map", (-2280, 240.0), frame_normal_and_bump)
        self._link_socket(node_combine_detail_weight, node_detail_normal_map, 0, 0)
        self._link_socket(node_group_input, node_detail_normal_map, sock_detail_normal_map, 1, reroute_normal_in)

        node_combine_normal_and_detail_vectors = self._add_node__math_vector("Combine normal and detail vectors", (-2080, 300.0), parent=frame_normal_and_bump)
        self._link_socket(node_normal_map, node_combine_normal_and_detail_vectors, 0, 0)
        self._link_socket(node_detail_normal_map, node_combine_normal_and_detail_vectors, 0, 1)

        node_bump_map = self._add_node__bump("Bump map", (-2080, 260.0), frame_normal_and_bump)
        self._link_socket(node_group_input, node_bump_map, sock_bump_strength, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_bump_map, sock_bump_strength_map, 2, reroute_normal_in)
        self._link_socket(node_combine_normal_and_detail_vectors, node_bump_map, 0, 3)

        # Nodes: Top Coat
        node_combine_top_coat_weight = self._add_node__hsv("Combine Top Coat Weight", (-1580, -740.0), frame_top_coat)
        self._link_socket(node_group_input, node_combine_top_coat_weight, sock_top_coat_weight, 2, reroute_top_coat_in)
        self._link_socket(node_group_input, node_combine_top_coat_weight, sock_top_coat_weight_map, 4, reroute_top_coat_in)

        node_combine_top_coat_roughness = self._add_node__hsv("Combine Top Coat Roughness", (-1580, -820.0), frame_top_coat)
        self._link_socket(node_group_input, node_combine_top_coat_roughness, sock_top_coat_roughness, 2, reroute_top_coat_in)
        self._link_socket(node_group_input, node_combine_top_coat_roughness, sock_top_coat_roughness_map, 4, reroute_top_coat_in)

        node_combine_top_coat_color = self._add_node__mix("Combine Top Coat Color", (-1580, -780.0), parent=frame_top_coat)
        self._link_socket(node_group_input, node_combine_top_coat_color, sock_top_coat_color_map, 6, reroute_top_coat_in)
        self._link_socket(node_group_input, node_combine_top_coat_color, sock_top_coat_color, 7, reroute_top_coat_in)

        # Nodes: Base Layer BDSF
        s = PrincipledBSDFSockets
        node_base_layer_bdsf = self._add_node__princ_bdsf("Base Layer BDSF", (-820, -40.0), props={"subsurface_method": "RANDOM_WALK_SKIN"})
        self._link_socket(node_combine_diffuse, node_base_layer_bdsf, 2, s.BASE_COLOR, reroute_pbr_out)
        self._link_socket(node_combine_metallic, node_base_layer_bdsf, 0, s.METALLIC, reroute_pbr_out)
        self._link_socket(node_combine_roughness, node_base_layer_bdsf, 0, s.ROUGHNESS, reroute_pbr_out)
        self._link_socket(node_combine_opacity, node_base_layer_bdsf, 0, s.ALPHA, reroute_pbr_out)
        self._link_socket(node_bump_map, node_base_layer_bdsf, 0, s.NORMAL)
        self._link_socket(node_group_input, node_base_layer_bdsf, sock_sss_weight, s.SUBSURFACE_WEIGHT, (reroute_sss_in, reroute_sss_out))
        self._link_socket(node_group_input, node_base_layer_bdsf, sock_sss_radius, s.SUBSURFACE_RADIUS, (reroute_sss_in, reroute_sss_out))
        self._link_socket(node_group_input, node_base_layer_bdsf, sock_sss_scale, s.SUBSURFACE_SCALE, (reroute_sss_in, reroute_sss_out))
        self._link_socket(node_group_input, node_base_layer_bdsf, sock_sss_direction, s.SUBSURFACE_ANISOTROPY, (reroute_sss_in, reroute_sss_out))
        self._link_socket(node_combine_top_coat_weight, node_base_layer_bdsf, 0, s.COAT_WEIGHT, reroute_top_coat_out)
        self._link_socket(node_combine_top_coat_roughness, node_base_layer_bdsf, 0, s.COAT_ROUGHNESS, reroute_top_coat_out)
        self._link_socket(node_combine_top_coat_color, node_base_layer_bdsf, 2, s.COAT_TINT, reroute_top_coat_out)
        self._link_socket(node_bump_map, node_base_layer_bdsf, 0, s.COAT_NORMAL)

        # Nodes: Dual Lobe Specular Layer
        dls_builder = DualLobeSpecularShaderGroupBuilder
        node_dls_group = self._add_node__shader_group("DLS", dls_builder, (-1620, -180.0))
        self._link_socket(node_group_input, node_dls_group, sock_dls_weight, dls_builder.in_weight)
        self._link_socket(node_group_input, node_dls_group, sock_dls_weight_map, dls_builder.in_weight_map)
        self._link_socket(node_group_input, node_dls_group, sock_dls_reflectivity, dls_builder.in_reflectivity)
        self._link_socket(node_group_input, node_dls_group, sock_dls_reflectivity_map, dls_builder.in_reflectivity_map)
        self._link_socket(node_group_input, node_dls_group, sock_dls_roughness_mult, dls_builder.in_roughness_mult)
        self._link_socket(node_group_input, node_dls_group, sock_dls_l1_roughness, dls_builder.in_l1_roughness)
        self._link_socket(node_group_input, node_dls_group, sock_dls_l1_roughness_map, dls_builder.in_l1_roughness_map)
        self._link_socket(node_group_input, node_dls_group, sock_dls_l2_roughness_mult, dls_builder.in_l2_roughness_mult)
        self._link_socket(node_group_input, node_dls_group, sock_dls_l2_roughness_mult_map, dls_builder.in_l2_roughness_mult_map)
        self._link_socket(node_group_input, node_dls_group, sock_dls_ratio, dls_builder.in_ratio)
        self._link_socket(node_group_input, node_dls_group, sock_dls_ratio_map, dls_builder.in_ratio_map)
        self._link_socket(node_bump_map, node_dls_group, 0, dls_builder.in_normal)

        # Nodes: Makeup Layer
        node_combine_makeup_weight = self._add_node__hsv("Combine Makeup Weight", (-1580, -940.0), frame_makeup_layer)
        self._link_socket(node_group_input, node_combine_makeup_weight, sock_makeup_weight, 2, reroute_makeup_in)
        self._link_socket(node_group_input, node_combine_makeup_weight, sock_makeup_weight_map, 4, reroute_makeup_in)

        node_combine_makeup_base_color = self._add_node__mix("Combine Makeup Base Color", (-1580, -980.0), parent=frame_makeup_layer)
        self._link_socket(node_group_input, node_combine_makeup_base_color, sock_makeup_base_color, 6, reroute_makeup_in)
        self._link_socket(node_group_input, node_combine_makeup_base_color, sock_makeup_base_color_map, 7, reroute_makeup_in)

        node_combine_makeup_roughness_mult = self._add_node__hsv("Combine Makeup Roughness Mult", (-1580, -1020.0), frame_makeup_layer)
        self._link_socket(node_group_input, node_combine_makeup_roughness_mult, sock_makeup_roughness_mult, 2, reroute_makeup_in)
        self._link_socket(node_group_input, node_combine_makeup_roughness_mult, sock_makeup_roughness_mult_map, 4, reroute_makeup_in)

        node_combine_makeup_metalic_weight = self._add_node__hsv("Combine Makeup Metalic Weight", (-1580, -1060.0), frame_makeup_layer)
        self._link_socket(node_group_input, node_combine_makeup_metalic_weight, sock_makeup_metallic_weight, 2, reroute_makeup_in)
        self._link_socket(node_group_input, node_combine_makeup_metalic_weight, sock_makeup_metallic_weight_map, 4, reroute_makeup_in)

        node_combine_diff_dls_roughness_for_makeup = self._add_node__mix("Combine Diffuse and DLS Roughness Maps for Makeup", (-1380, -960.0), parent=frame_makeup_layer)
        self._link_socket(node_combine_roughness, node_combine_diff_dls_roughness_for_makeup, 0, 6, (reroute_pbr_out, reroute_makeup_in))
        self._link_socket(node_group_input, node_combine_diff_dls_roughness_for_makeup, sock_dls_l1_roughness_map,7, reroute_makeup_in)

        node_multiply_makeup_base_roughness = self._add_node__mix("Multiply Makeup Base Roughness", (-1380, -1000.0), parent=frame_makeup_layer)
        self._link_socket(node_combine_diff_dls_roughness_for_makeup, node_multiply_makeup_base_roughness, 2, 6)
        self._link_socket(node_combine_makeup_roughness_mult, node_multiply_makeup_base_roughness, 0, 7)

        node_makeup_normal_interpolation_base_value = self._add_node__normal_map("Makeup Normal Interpolation Base Value", (-1580, -1140.0), frame_makeup_layer)

        node_interpolate_makeup_normal = self._add_node__mix("Interpolate Makeup Normal", (-1380, -1100.0), data_type="VECTOR", parent=frame_makeup_layer)
        self._link_socket(node_group_input, node_interpolate_makeup_normal, sock_makeup_reduce_normals, 0, reroute_makeup_in)
        self._link_socket(node_bump_map, node_interpolate_makeup_normal, 0, 4, reroute_makeup_in)
        self._link_socket(node_makeup_normal_interpolation_base_value, node_interpolate_makeup_normal, 0, 5)

        node_makeup_layer_bsdf = self._add_node__princ_bdsf("Makeup Layer BSDF", (-1180, -940.0), frame_makeup_layer)
        self._link_socket(node_combine_makeup_base_color, node_makeup_layer_bsdf, 2, s.BASE_COLOR)
        self._link_socket(node_combine_makeup_metalic_weight, node_makeup_layer_bsdf, 0, s.METALLIC)
        self._link_socket(node_multiply_makeup_base_roughness, node_makeup_layer_bsdf, 2, s.ROUGHNESS)
        self._link_socket(node_interpolate_makeup_normal, node_makeup_layer_bsdf, 1, s.NORMAL)

        # Nodes: Mix Layers
        node_mix_makeup_shader = self._add_node__mix_shader("Mix Makeup Shader", (-200, 40.0))
        self._link_socket(node_combine_makeup_weight, node_mix_makeup_shader, 0, 0, reroute_makeup_out)
        self._link_socket(node_base_layer_bdsf, node_mix_makeup_shader, 0, 1)
        self._link_socket(node_makeup_layer_bsdf, node_mix_makeup_shader, 0, 2, reroute_makeup_out)

        node_mix_dls_shader = self._add_node__mix_shader("Mix DLS Shader", (-200, 0.0))
        self._link_socket(node_dls_group, node_mix_dls_shader, 0, 0)
        self._link_socket(node_mix_makeup_shader, node_mix_dls_shader, 0, 1)
        self._link_socket(node_dls_group, node_mix_dls_shader, 1, 2)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0, 0))
        self._link_socket(node_mix_dls_shader, node_group_output, 0, sock_out_surface)
        # @formatter:on

        self.hide_all_nodes(node_group_input,
                            node_base_layer_bdsf,
                            node_makeup_layer_bsdf,
                            node_dls_group,
                            node_group_output)


class PBRSkinShaderGroupApplier(ShaderGroupApplier):
    mapping_node_location_offset = -50

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        builder = PBRSkinShaderGroupBuilder

        # @formatter:off
        self._set_material_mapping("horizontal_tiles2", "horizontal_offset2", "vertical_tiles2", "vertical_offset2")

        self._channel_to_sockets('diffuse', builder.in_diffuse_color, builder.in_diffuse_color_map, False)

        if self._channel_enabled('diffuse_roughness'):
            # For some reason the diffuse roughness is set to 0 by default.
            # This makes the shader very glossy in Blender, hence we only set it if it's non-zero.
            self._channel_to_sockets('diffuse_roughness', builder.in_roughness, builder.in_roughness_map)

        self._channel_to_sockets('metallic_weight', builder.in_metallic, builder.in_metallic_map)
        self._channel_to_sockets('cutout_opacity', builder.in_opacity, builder.in_opacity_map)

        if self._channel_enabled('dual_lobe_specular_enable'):
            self._channel_to_sockets('dual_lobe_specular_weight', builder.in_dls_weight, builder.in_dls_weight_map)
            if self._properties.dls_weight_multiplier != 1.0:
                self._set_socket(self._shader_group, builder.in_dls_weight, self._properties.dls_weight_multiplier, "MULTIPLY")

            self._channel_to_sockets('dual_lobe_specular_reflectivity', builder.in_dls_reflectivity, builder.in_dls_reflectivity_map)
            self._channel_to_sockets('dual_lobe_specular_roughness_mult', builder.in_dls_roughness_mult, None)
            self._channel_to_sockets('specular_lobe_1_roughness', builder.in_dls_l1_roughness, builder.in_dls_l1_roughness_map)
            self._channel_to_sockets('specular_lobe_2_roughness_mult', builder.in_dls_l2_roughness_mult, builder.in_dls_l2_roughness_mult_map)
            self._channel_to_sockets('dual_lobe_specular_ratio', builder.in_dls_ratio, builder.in_dls_ratio_map)

        if self._channel_enabled('sub_surface_enable'):
            self._channel_to_sockets('translucency_weight', builder.in_sss_weight, None)
            self._channel_to_sockets('sss_color', builder.in_sss_radius, None)
            self._channel_to_sockets('sss_direction', builder.in_sss_direction, None)

        self._channel_to_sockets('normal_map', builder.in_normal_weight, builder.in_normal_map)
        if self._properties.pbr_skin_normal_multiplier != 1.0:
            self._set_socket(self._shader_group, builder.in_normal_weight, self._properties.pbr_skin_normal_multiplier, "MULTIPLY")

        if self._channel_enabled('detail_enable'):
            self._channel_to_sockets('detail_weight', builder.in_detail_weight, builder.in_detail_weight_map)
            detail_map_tex_node = self._channel_to_sockets('detail_normal_map', None, builder.in_detail_normal_map)
            if self._properties.pbr_skin_normal_multiplier != 1.0:
                self._set_socket(self._shader_group, builder.in_detail_weight, self._properties.pbr_skin_normal_multiplier, "MULTIPLY")

            # Only apply mapping if tiling is enabled for this node
            detail_mapping_ids = ["detail_horizontal_tiles", "detail_horizontal_offset", "detail_vertical_tiles", "detail_vertical_offset"]
            if detail_map_tex_node and self._channel_enabled(*detail_mapping_ids):
                detail_mapping_node_loc = tuple_zip_sum((0, self.mapping_node_location_offset), self._mapping.location.to_tuple())
                detail_mapping_node = self._add_node(ShaderNodeMapping, "Detail Mapping", detail_mapping_node_loc, props={"vector_type": "POINT", "hide": True})
                self._link_socket(self._uv_map, detail_mapping_node, 0, 0)
                self._link_socket(detail_mapping_node, detail_map_tex_node, 0, 0)
                self._set_material_mapping(*detail_mapping_ids, mapping_node=detail_mapping_node)

        if self._channel_enabled('bump_enable'):
            self._channel_to_sockets('bump_strength', builder.in_bump_strength, builder.in_bump_strength_map)

        if self._channel_enabled('top_coat_enable'):
            self._channel_to_sockets('top_coat_weight', builder.in_top_coat_weight, builder.in_top_coat_weight_map)
            self._channel_to_sockets('top_coat_roughness', builder.in_top_coat_roughness, builder.in_top_coat_roughness_map)
            self._channel_to_sockets('top_coat_color', builder.in_top_coat_color, builder.in_top_coat_color_map, False)

        if self._channel_enabled('makeup_enable'):
            self._channel_to_sockets('makeup_weight', builder.in_makeup_weight, builder.in_makeup_weight_map)
            self._channel_to_sockets('makeup_base_color', builder.in_makeup_base_color, builder.in_makeup_base_color_map, False)
            self._channel_to_sockets('makeup_roughness_mult', builder.in_makeup_roughness_mult, builder.in_makeup_roughness_mult_map)
        # @formatter:on
