from typing import Type

from .support import FakeGlassShaderGroupApplier, FakeGlassShaderGroupBuilder, ShaderGroupApplier, ShaderGroupBuilder, \
    RerouteGroup, AsymmetricalDisplacementShaderGroupBuilder, DualLobeSpecularShaderGroupBuilder, \
    BlackbodyEmissionShaderGroupBuilder, MetallicFlakesShaderGroupBuilder, WeightedTranslucencyShaderGroupBuilder
from ..utils.b_shaders.principled_bdsf import PrincipledBSDFSockets
from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "Iray Uber (Metallicity/Roughness)"
__MATERIAL_TYPE_ID__ = "iray_uber__pbr_mr"


class IrayUberPBRMRShaderGroupBuilder(ShaderGroupBuilder):
    """
    About Iray Uber, decisions had to be made.
    Given Iray Uber has 166 adjustable properties (counting values and maps separately).
    If all properties were to be implemented, this group would become a massive undertaking.

    So here's the decisions taken:
    - Only map and implement commonly used properties
    - Only support PBR Metallicity/Roughness mixing
    """

    # Base Diffuse
    in_diffuse = "Diffuse"
    in_diffuse_map = "Diffuse Map"
    in_metallic_weight = "Metallic Weight"
    in_metallic_weight_map = "Metallic Weight Map"
    in_diffuse_roughness = "Diffuse Roughness"
    in_diffuse_roughness_map = "Diffuse Roughness Map"

    # Base Bump
    in_normal_map = "Normal"
    in_normal_map_map = "Normal Map"
    in_bump_strength = "Bump Strength"
    in_bump_strength_map = "Bump Strength Map"

    # Base Diffuse Overlay
    in_diffuse_overlay_weight = "Diffuse Overlay Weight"
    in_diffuse_overlay_weight_map = "Diffuse Overlay Weight Map"
    in_diffuse_overlay_weight_squared = "Diffuse Overlay Weight Squared"
    in_diffuse_overlay_color = "Diffuse Overlay Color"
    in_diffuse_overlay_color_map = "Diffuse Overlay Color Map"
    in_diffuse_overlay_roughness = "Diffuse Overlay Roughness"
    in_diffuse_overlay_roughness_map = "Diffuse Overlay Roughness Map"

    # Base Diffuse Translucency
    in_translucency_weight = "Translucency Weight"
    in_translucency_weight_map = "Translucency Weight Map"
    in_translucency_color = "Translucency Color"
    in_translucency_color_map = "Translucency Color Map"
    in_invert_transmission_normal = "Invert Transmission Normal"

    # Base Dual Lobe Specular
    in_dual_lobe_specular_weight = "Dual Lobe Specular Weight"
    in_dual_lobe_specular_weight_map = "Dual Lobe Specular Weight Map"
    in_dual_lobe_specular_reflectivity = "Dual Lobe Specular Reflectivity"
    in_dual_lobe_specular_reflectivity_map = "Dual Lobe Specular Reflectivity Map"
    in_specular_lobe_1_roughness = "Specular Lobe 1 Roughness"
    in_specular_lobe_1_roughness_map = "Specular Lobe 1 Roughness Map"
    in_specular_lobe_2_roughness = "Specular Lobe 2 Roughness"
    in_specular_lobe_2_roughness_map = "Specular Lobe 2 Roughness Map"
    in_dual_lobe_specular_ratio = "Dual Lobe Specular Ratio"
    in_dual_lobe_specular_ratio_map = "Dual Lobe Specular Ratio Map"

    # Base Thin Film
    in_base_thin_film = "Base Thin Film"
    in_base_thin_film_map = "Base Thin Film Map"
    in_base_thin_film_ior = "Base Thin Film IOR"
    in_base_thin_film_ior_map = "Base Thin Film IOR Map"

    # Emission
    in_emission_color = "Emission Color"
    in_emission_color_map = "Emission Color Map"
    in_emission_temperature = "Emission Temperature"
    in_luminance = "Luminance"
    in_luminance_map = "Luminance Map"

    # Geometry Cutout
    in_cutout_opacity = "Cutout Opacity"
    in_cutout_opacity_map = "Cutout Opacity Map"

    # Geometry Displacement
    in_displacement_strength = "Displacement Strength"
    in_displacement_strength_map = "Displacement Strength Map"
    in_minimum_displacement = "Minimum Displacement"
    in_maximum_displacement = "Maximum Displacement"

    # Metallic Flakes Flakes
    in_metallic_flakes_weight = "Metallic Flakes Weight"
    in_metallic_flakes_weight_map = "Metallic Flakes Weight Map"
    in_metallic_flakes_color = "Metallic Flakes Color"
    in_metallic_flakes_color_map = "Metallic Flakes Color Map"
    in_metallic_flakes_roughness = "Metallic Flakes Roughness"
    in_metallic_flakes_roughness_map = "Metallic Flakes Roughness Map"
    in_metallic_flakes_size = "Metallic Flakes Size"
    in_metallic_flakes_strength = "Metallic Flakes Strength"
    in_metallic_flakes_density = "Metallic Flakes Density"

    # Top Coat
    in_top_coat_weight = "Top Coat Weight"
    in_top_coat_weight_map = "Top Coat Weight Map"
    in_top_coat_color = "Top Coat Color"
    in_top_coat_color_map = "Top Coat Color Map"
    in_top_coat_roughness = "Top Coat Roughness"
    in_top_coat_roughness_map = "Top Coat Roughness Map"

    # Volume Scattering
    in_sss_weight = "SSS Weight"
    in_sss_color = "SSS Color"
    in_scattering_measurement_distance = "Scattering Measurement Distance"
    in_sss_direction = "SSS Direction"

    # Volume Transmission
    in_refraction_weight = "Refraction Weight"
    in_refraction_weight_map = "Refraction Weight Map"
    in_ior = "IOR"
    in_transmitted_measurement_distance = "Transmitted Measurement Distance"
    in_transmitted_color = "Transmitted Color"
    in_transmitted_color_map = "Transmitted Color Map"

    out_surface = "Surface"
    out_volume = "Volume"
    out_displacement = "Displacement"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    @staticmethod
    def depends_on() -> set[Type[ShaderGroupBuilder]]:
        return {
            AsymmetricalDisplacementShaderGroupBuilder,
            BlackbodyEmissionShaderGroupBuilder,
            DualLobeSpecularShaderGroupBuilder,
            MetallicFlakesShaderGroupBuilder,
            WeightedTranslucencyShaderGroupBuilder,
            FakeGlassShaderGroupBuilder,
        }

    def setup_group(self):
        super().setup_group()

        # @formatter:off
        # Panels
        panel_base_diffuse = self._add_panel("Base Diffuse", False)
        panel_base_bump = self._add_panel("Base Bump", False)
        panel_base_diffuse_overlay = self._add_panel("Base Diffuse Overlay")
        panel_base_diffuse_translucency = self._add_panel("Base Diffuse Translucency")
        panel_base_dual_lobe_specular = self._add_panel("Base Dual Lobe Specular")
        panel_base_thin_film = self._add_panel("Base Thin Film")
        panel_emission = self._add_panel("Emission")
        panel_geometry_cutout = self._add_panel("Geometry Cutout")
        panel_geometry_displacement = self._add_panel("Geometry Displacement")
        panel_metallic_flakes_flakes = self._add_panel("Metallic Flakes Flakes")
        panel_top_coat_general = self._add_panel("Top Coat")
        panel_volume_scattering = self._add_panel("Volume Scattering")
        panel_volume_transmission = self._add_panel("Volume Transmission")

        # Sockets: Base Diffuse
        sock_diffuse = self._color_socket(self.in_diffuse, parent=panel_base_diffuse)
        sock_diffuse_map = self._color_socket(self.in_diffuse_map, parent=panel_base_diffuse)
        sock_metallic_weight = self._float_socket(self.in_metallic_weight, parent=panel_base_diffuse)
        sock_metallic_weight_map = self._color_socket(self.in_metallic_weight_map, parent=panel_base_diffuse)
        sock_diffuse_roughness = self._float_socket(self.in_diffuse_roughness, 1.0, parent=panel_base_diffuse)
        sock_diffuse_roughness_map = self._color_socket(self.in_diffuse_roughness_map, parent=panel_base_diffuse)

        # Sockets: Base Bump
        sock_normal = self._float_socket(self.in_normal_map, 1, parent=panel_base_bump)
        sock_normal_map = self._color_socket(self.in_normal_map_map, parent=panel_base_bump)
        sock_bump_strength = self._float_socket(self.in_bump_strength, 1, parent=panel_base_bump)
        sock_bump_strength_map = self._color_socket(self.in_bump_strength_map, parent=panel_base_bump)

        # Sockets: Base Diffuse Overlay
        sock_diffuse_overlay_weight = self._float_socket(self.in_diffuse_overlay_weight, parent=panel_base_diffuse_overlay)
        sock_diffuse_overlay_weight_map = self._color_socket(self.in_diffuse_overlay_weight_map, parent=panel_base_diffuse_overlay)
        sock_diffuse_overlay_weight_squared = self._bool_socket(self.in_diffuse_overlay_weight_squared, parent=panel_base_diffuse_overlay)
        sock_diffuse_overlay_color = self._color_socket(self.in_diffuse_overlay_color, (0.7529411, 0.7529411, 0.7529411, 1.0), parent=panel_base_diffuse_overlay)
        sock_diffuse_overlay_color_map = self._color_socket(self.in_diffuse_overlay_color_map, parent=panel_base_diffuse_overlay)
        sock_diffuse_overlay_roughness = self._float_socket(self.in_diffuse_overlay_roughness, parent=panel_base_diffuse_overlay)
        sock_diffuse_overlay_roughness_map = self._color_socket(self.in_diffuse_overlay_roughness_map, parent=panel_base_diffuse_overlay)

        # Sockets: Base Diffuse Translucency
        sock_translucency_weight = self._float_socket(self.in_translucency_weight, parent=panel_base_diffuse_translucency)
        sock_translucency_weight_map = self._color_socket(self.in_translucency_weight_map, parent=panel_base_diffuse_translucency)
        sock_translucency_color = self._color_socket(self.in_translucency_color, parent=panel_base_diffuse_translucency)
        sock_translucency_color_map = self._color_socket(self.in_translucency_color_map, parent=panel_base_diffuse_translucency)
        sock_invert_transmission_normal = self._bool_socket(self.in_invert_transmission_normal, True, parent=panel_base_diffuse_translucency)

        # Sockets: Base Dual Lobe Specular
        sock_dual_lobe_specular_weight = self._float_socket(self.in_dual_lobe_specular_weight, parent=panel_base_dual_lobe_specular)
        sock_dual_lobe_specular_weight_map = self._color_socket(self.in_dual_lobe_specular_weight_map, parent=panel_base_dual_lobe_specular)
        sock_dual_lobe_specular_reflectivity = self._float_socket(self.in_dual_lobe_specular_reflectivity, 0.5, parent=panel_base_dual_lobe_specular)
        sock_dual_lobe_specular_reflectivity_map = self._color_socket(self.in_dual_lobe_specular_reflectivity_map, parent=panel_base_dual_lobe_specular)
        sock_specular_lobe_1_roughness = self._float_socket(self.in_specular_lobe_1_roughness, parent=panel_base_dual_lobe_specular)
        sock_specular_lobe_1_roughness_map = self._color_socket(self.in_specular_lobe_1_roughness_map, parent=panel_base_dual_lobe_specular)
        sock_specular_lobe_2_roughness = self._float_socket(self.in_specular_lobe_2_roughness, parent=panel_base_dual_lobe_specular)
        sock_specular_lobe_2_roughness_map = self._color_socket(self.in_specular_lobe_2_roughness_map, parent=panel_base_dual_lobe_specular)
        sock_dual_lobe_specular_ratio = self._float_socket(self.in_dual_lobe_specular_ratio, 0.85, parent=panel_base_dual_lobe_specular)
        sock_dual_lobe_specular_ratio_map = self._color_socket(self.in_dual_lobe_specular_ratio_map, parent=panel_base_dual_lobe_specular)

        # Sockets: Base Thin Film
        sock_base_thin_film = self._float_socket(self.in_base_thin_film, parent=panel_base_thin_film)
        sock_base_thin_film_map = self._color_socket(self.in_base_thin_film_map, parent=panel_base_thin_film)
        sock_base_thin_film_ior = self._float_socket(self.in_base_thin_film_ior, 1.5, parent=panel_base_thin_film)
        sock_base_thin_film_ior_map = self._color_socket(self.in_base_thin_film_ior_map, parent=panel_base_thin_film)

        # Sockets: Emission
        sock_emission_color = self._color_socket(self.in_emission_color, (0.0, 0.0, 0.0, 1.0), parent=panel_emission)
        sock_emission_color_map = self._color_socket(self.in_emission_color_map, parent=panel_emission)
        sock_emission_temperature = self._float_socket(self.in_emission_temperature, 6500, parent=panel_emission)
        sock_luminance = self._float_socket(self.in_luminance, 1500, parent=panel_emission)
        sock_luminance_map = self._color_socket(self.in_luminance_map, parent=panel_emission)

        # Sockets: Geometry Cutout
        sock_cutout_opacity = self._float_socket(self.in_cutout_opacity, 1, parent=panel_geometry_cutout)
        sock_cutout_opacity_map = self._color_socket(self.in_cutout_opacity_map, parent=panel_geometry_cutout)

        # Sockets: Geometry Displacement
        sock_displacement_strength = self._float_socket(self.in_displacement_strength, parent=panel_geometry_displacement)
        sock_displacement_strength_map = self._color_socket(self.in_displacement_strength_map, (0.5, 0.5, 0.5, 1.0), parent=panel_geometry_displacement)
        sock_minimum_displacement = self._float_socket(self.in_minimum_displacement, -0.1, parent=panel_geometry_displacement)
        sock_maximum_displacement = self._float_socket(self.in_maximum_displacement, 0.1, parent=panel_geometry_displacement)

        # Sockets: Metallic Flakes Flakes
        sock_metallic_flakes_weight = self._float_socket(self.in_metallic_flakes_weight, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_weight_map = self._color_socket(self.in_metallic_flakes_weight_map, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_color = self._color_socket(self.in_metallic_flakes_color, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_color_map = self._color_socket(self.in_metallic_flakes_color_map, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_roughness = self._float_socket(self.in_metallic_flakes_roughness, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_roughness_map = self._color_socket(self.in_metallic_flakes_roughness_map, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_size = self._float_socket(self.in_metallic_flakes_size, 0.001, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_strength = self._float_socket(self.in_metallic_flakes_strength, 1, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_density = self._float_socket(self.in_metallic_flakes_density, 1, parent=panel_metallic_flakes_flakes)

        # Sockets: Top Coat General
        sock_top_coat_weight = self._float_socket(self.in_top_coat_weight, parent=panel_top_coat_general)
        sock_top_coat_weight_map = self._color_socket(self.in_top_coat_weight_map, parent=panel_top_coat_general)
        sock_top_coat_color = self._color_socket(self.in_top_coat_color, parent=panel_top_coat_general)
        sock_top_coat_color_map = self._color_socket(self.in_top_coat_color_map, parent=panel_top_coat_general)
        sock_top_coat_roughness = self._float_socket(self.in_top_coat_roughness, parent=panel_top_coat_general)
        sock_top_coat_roughness_map = self._color_socket(self.in_top_coat_roughness_map, parent=panel_top_coat_general)

        # Sockets: Volume Scattering
        sock_sss_weight = self._float_socket(self.in_sss_weight, parent=panel_volume_scattering)
        sock_sss_color = self._color_socket(self.in_sss_color, (0.0, 0.0, 0.0, 1.0), parent=panel_volume_scattering)
        sock_sss_direction = self._float_socket(self.in_sss_direction, parent=panel_volume_scattering)
        sock_sss_scale = self._float_socket(self.in_scattering_measurement_distance, 0.1, parent=panel_volume_scattering)

        # Sockets: Volume Transmission
        sock_refraction_weight = self._float_socket(self.in_refraction_weight, parent=panel_volume_transmission)
        sock_refraction_weight_map = self._color_socket(self.in_refraction_weight_map, parent=panel_volume_transmission)
        sock_ior = self._float_socket(self.in_ior, 1.5, parent=panel_volume_transmission)
        sock_transmitted_distance = self._float_socket(self.in_transmitted_measurement_distance, 0.1, parent=panel_volume_transmission)
        sock_transmitted_color = self._color_socket(self.in_transmitted_color, (0.0, 0.0, 0.0, 1.0), parent=panel_volume_transmission)
        sock_transmitted_color_map = self._color_socket(self.in_transmitted_color_map, parent=panel_volume_transmission)

        # Output Sockets:
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")
        sock_out_volume = self._shader_socket(self.out_volume, in_out="OUTPUT")
        sock_out_displacement = self._vector_socket(self.out_displacement, in_out="OUTPUT")

        # Frames and Reroute Groups
        frame_pbr = self._add_frame("PBR")
        reroute_pbr_in = RerouteGroup(-2347, 800, frame_pbr)
        reroute_pbr_out = RerouteGroup(-1584, 755, frame_pbr)

        frame_normal = self._add_frame("Normal")
        reroute_normal_in = RerouteGroup(-3067, 713, frame_normal)

        frame_diff_overlay = self._add_frame("Diffuse Overlay")
        reroute_diff_overlay_in = RerouteGroup(-1367, 492, frame_diff_overlay)
        reroute_diff_overlay_out = RerouteGroup(-515, 489, frame_diff_overlay)

        frame_thin_film = self._add_frame("Thin Film")
        reroute_thin_film_in = RerouteGroup(-2107, -419, frame_thin_film)

        frame_top_coat = self._add_frame("Top coat")
        reroute_top_coat_in = RerouteGroup(-2267, -1586, frame_top_coat)
        reroute_top_coat_out = RerouteGroup(-1613, -1596, frame_top_coat)

        frame_transmission = self._add_frame("Refraction and Tranmission")
        reroute_transmission_in = RerouteGroup(-2327, -1979, frame_transmission)
        reroute_transmission_out = RerouteGroup(-1520, -1908, frame_transmission)

        reroute_sss_ior = RerouteGroup(1920.0, -1361.0)

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-3320, 400))

        # Nodes: PBR
        node_mix_diffuse_color = self._add_node__mix("Mix Diffuse Color and Map", (-2303, 821), parent=frame_pbr)
        self._link_socket(node_group_input, node_mix_diffuse_color, sock_diffuse, 6, reroute_pbr_in)
        self._link_socket(node_group_input, node_mix_diffuse_color, sock_diffuse_map, 7, reroute_pbr_in)

        node_mix_metallic_weight = self._add_node__hsv("Mix Metallic Weight and Map", (-2123, 801), parent=frame_pbr)
        self._link_socket(node_group_input, node_mix_metallic_weight, sock_metallic_weight, 2, reroute_pbr_in)
        self._link_socket(node_group_input, node_mix_metallic_weight, sock_metallic_weight_map, 4, reroute_pbr_in)

        node_mix_roughness_weight = self._add_node__hsv("Mix Rougness Weight and Map", (-1943, 801), parent=frame_pbr)
        self._link_socket(node_group_input, node_mix_roughness_weight, sock_diffuse_roughness, 2, reroute_pbr_in)
        self._link_socket(node_group_input, node_mix_roughness_weight, sock_diffuse_roughness_map, 4, reroute_pbr_in)

        node_mix_opacity = self._add_node__hsv("Mix Cutout Opacity and Map", (-1773, 801), parent=frame_pbr)
        self._link_socket(node_group_input, node_mix_opacity, sock_cutout_opacity, 2, reroute_pbr_in)
        self._link_socket(node_group_input, node_mix_opacity, sock_cutout_opacity_map, 4, reroute_pbr_in)

        # Nodes: Normal and Bump
        node_normal_map = self._add_node__normal_map("Normal Map", (-3021, 761), parent=frame_normal)
        self._link_socket(node_group_input, node_normal_map, sock_normal, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_normal_map, sock_normal_map, 1, reroute_normal_in)

        node_bump = self._add_node__bump("Bump", (-2821, 761), parent=frame_normal)
        self._link_socket(node_group_input, node_bump, sock_bump_strength, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_bump, sock_bump_strength_map, 2, reroute_normal_in)
        self._link_socket(node_normal_map, node_bump, 0, 3)

        node_normal_reroute_left = self._add_node__reroute((-2142, -710))
        self._link_socket(node_bump, node_normal_reroute_left, 0, 0)
        node_normal_reroute_right = self._add_node__reroute((-1265, 214))
        self._link_socket(node_bump, node_normal_reroute_right, 0, 0)

        # Nodes: Diffuse Overlay
        node_mix_overlay_weight = self._add_node__hsv("Mix Overlay Weight and Map", (-1284, 740), parent=frame_diff_overlay)
        self._link_socket(node_group_input, node_mix_overlay_weight, sock_diffuse_overlay_weight, 2, reroute_diff_overlay_in)
        self._link_socket(node_group_input, node_mix_overlay_weight, sock_diffuse_overlay_weight_map, 4, reroute_diff_overlay_in)

        node_overlay_sq_exponent = self._add_node__math("Overlay Squared Exponent", (-1284, 560), "POWER", parent=frame_diff_overlay)
        self._link_socket(node_group_input, node_overlay_sq_exponent, sock_diffuse_overlay_weight_squared, 0, reroute_diff_overlay_in)
        self._set_socket(node_overlay_sq_exponent, 1, 1.0)

        node_overlay_sq_value = self._add_node__math("Overlay Squared", (-1104, 640), parent=frame_diff_overlay)
        self._link_socket(node_mix_overlay_weight, node_overlay_sq_value, 0, 0)
        self._link_socket(node_overlay_sq_exponent, node_overlay_sq_value, 0, 1)

        node_mix_overlay_color = self._add_node__mix("Mix Overlay Color and Map", (-913, 700), parent=frame_diff_overlay)
        self._link_socket(node_group_input, node_mix_overlay_color, sock_diffuse_overlay_color, 6, reroute_diff_overlay_in)
        self._link_socket(node_group_input, node_mix_overlay_color, sock_diffuse_overlay_color_map, 7, reroute_diff_overlay_in)

        node_mix_overlay_roughness = self._add_node__hsv("Mix Overlay Roughness and Map", (-913, 460), parent=frame_diff_overlay)
        self._link_socket(node_group_input, node_mix_overlay_roughness, sock_diffuse_overlay_roughness, 2, reroute_diff_overlay_in)
        self._link_socket(node_group_input, node_mix_overlay_roughness, sock_diffuse_overlay_roughness_map, 4, reroute_diff_overlay_in)

        node_overlay_bsdf = self._add_node("ShaderNodeBsdfDiffuse", "Overlay Layer BSDF", (-700, 476), parent=frame_diff_overlay)
        self._link_socket(node_mix_overlay_color, node_overlay_bsdf, 2, 0)
        self._link_socket(node_mix_overlay_roughness, node_overlay_bsdf, 0, 1)
        self._link_socket(node_normal_reroute_right, node_overlay_bsdf, 0, 2)

        # Nodes: Translucency
        builder_trans = WeightedTranslucencyShaderGroupBuilder
        node_translucency = self._add_node__shader_group("Translucency", builder_trans,  (-2000, 225))
        self._link_socket(node_group_input, node_translucency, sock_translucency_weight, builder_trans.in_translucency_weight)
        self._link_socket(node_group_input, node_translucency, sock_translucency_weight_map, builder_trans.in_translucency_weight_map)
        self._link_socket(node_group_input, node_translucency, sock_translucency_color, builder_trans.in_translucency_color)
        self._link_socket(node_group_input, node_translucency, sock_translucency_color_map, builder_trans.in_translucency_color_map)
        self._link_socket(node_group_input, node_translucency, sock_invert_transmission_normal, builder_trans.in_invert_transmission_normal)
        self._link_socket(node_normal_reroute_left, node_translucency, 0, builder_trans.in_normal)

        # Nodes: DLS
        builder_dls = DualLobeSpecularShaderGroupBuilder
        node_dls = self._add_node__shader_group("DLS", builder_dls, (-2000, -14))
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_weight, builder_dls.in_weight)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_weight_map, builder_dls.in_weight_map)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_reflectivity, builder_dls.in_reflectivity)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_reflectivity_map, builder_dls.in_reflectivity_map)
        self._set_socket(node_dls, builder_dls.in_roughness_mult, 1)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_1_roughness, builder_dls.in_l1_roughness)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_1_roughness_map, builder_dls.in_l1_roughness_map)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_2_roughness, builder_dls.in_l2_roughness_mult)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_2_roughness_map, builder_dls.in_l2_roughness_mult_map)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_ratio, builder_dls.in_ratio)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_ratio_map, builder_dls.in_ratio_map)
        self._link_socket(node_normal_reroute_left, node_dls, 0, builder_trans.in_normal)

        # Nodes: Thin Film
        node_mix_thin_film = self._add_node__hsv("Mix Thin Film and Map", (-2071, -420), parent=frame_thin_film)
        self._link_socket(node_group_input, node_mix_thin_film, sock_base_thin_film, 2, reroute_thin_film_in)
        self._link_socket(node_group_input, node_mix_thin_film, sock_base_thin_film_map, 4, reroute_thin_film_in)

        node_mix_thin_film_ior = self._add_node__hsv("Mix Thin Film IOR and Map", (-1880, -420), parent=frame_thin_film)
        self._link_socket(node_group_input, node_mix_thin_film_ior, sock_base_thin_film_ior, 2, reroute_thin_film_in)
        self._link_socket(node_group_input, node_mix_thin_film_ior, sock_base_thin_film_ior_map, 4, reroute_thin_film_in)

        # Nodes: Blackbody Emission
        builder_emiss = BlackbodyEmissionShaderGroupBuilder
        node_bb_emission = self._add_node__shader_group("Blackbody Emission", builder_emiss, (-2000, -634))
        self._link_socket(node_group_input, node_bb_emission, sock_emission_color, builder_emiss.in_color)
        self._link_socket(node_group_input, node_bb_emission, sock_emission_color_map, builder_emiss.in_color_map)
        self._link_socket(node_group_input, node_bb_emission, sock_emission_temperature, builder_emiss.in_temperature)
        self._link_socket(node_group_input, node_bb_emission, sock_luminance, builder_emiss.in_luminance)
        self._link_socket(node_group_input, node_bb_emission, sock_luminance_map, builder_emiss.in_luminance_map)

        # Nodes: Displacement
        builder_disp = AsymmetricalDisplacementShaderGroupBuilder
        node_displacement = self._add_node__shader_group("Displacement", builder_disp, (-2000, -854))
        self._link_socket(node_group_input, node_displacement, sock_displacement_strength, builder_disp.in_strength)
        self._link_socket(node_group_input, node_displacement, sock_displacement_strength_map, builder_disp.in_strength_map)
        self._link_socket(node_group_input, node_displacement, sock_minimum_displacement, builder_disp.in_min_displacement)
        self._link_socket(node_group_input, node_displacement, sock_maximum_displacement, builder_disp.in_max_displacement)
        self._link_socket(node_normal_reroute_left, node_displacement, 0, builder_disp.in_normal)

        # Nodes: Metallic Flakes
        builder_flakes = MetallicFlakesShaderGroupBuilder
        node_flakes = self._add_node__shader_group("Metallic Flakes", builder_flakes, (-2000, -1054))
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_weight, builder_flakes.in_weight)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_weight_map, builder_flakes.in_weight_map)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_color, builder_flakes.in_color)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_color_map, builder_flakes.in_color_map)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_roughness, builder_flakes.in_roughness)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_roughness_map, builder_flakes.in_roughness_map)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_size, builder_flakes.in_flake_size)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_strength, builder_flakes.in_flake_strength)
        self._link_socket(node_group_input, node_flakes, sock_metallic_flakes_density, builder_flakes.in_flake_density)
        self._link_socket(node_normal_reroute_left, node_flakes, 0, builder_flakes.in_normal)

        # Nodes: Top Coat
        node_mix_top_coat_weight = self._add_node__hsv("Mix Top Coat Weight and Map", (-2221, -1558), parent=frame_top_coat)
        self._link_socket(node_group_input, node_mix_top_coat_weight, sock_top_coat_weight, 2, reroute_top_coat_in)
        self._link_socket(node_group_input, node_mix_top_coat_weight, sock_top_coat_weight_map, 4, reroute_top_coat_in)

        node_mix_top_coat_color = self._add_node__mix("Mix Top Coat Color and Map", (-2021, -1558), parent=frame_top_coat)
        self._link_socket(node_group_input, node_mix_top_coat_color, sock_top_coat_color, 6, reroute_top_coat_in)
        self._link_socket(node_group_input, node_mix_top_coat_color, sock_top_coat_color_map, 7, reroute_top_coat_in)

        node_mix_top_coat_roughness = self._add_node__hsv("Mix Top Coat Roughness and Map", (-1841, -1558), parent=frame_top_coat)
        self._link_socket(node_group_input, node_mix_top_coat_roughness, sock_top_coat_roughness, 2, reroute_top_coat_in)
        self._link_socket(node_group_input, node_mix_top_coat_roughness, sock_top_coat_roughness_map, 4, reroute_top_coat_in)

        # Nodes: Refraction and Transmission
        node_mix_refraction_weight = self._add_node__hsv("Mix Refraction Weight and Map", (-2103, -2099), parent=frame_transmission)
        self._link_socket(node_group_input, node_mix_refraction_weight, sock_refraction_weight, 2, reroute_transmission_in)
        self._link_socket(node_group_input, node_mix_refraction_weight, sock_refraction_weight_map, 4, reroute_transmission_in)

        node_limit_trans_distance = self._add_node__math("Limit Transmitted Distane", (-1983, -1899), "MAXIMUM", parent=frame_transmission)
        self._link_socket(node_group_input, node_limit_trans_distance, sock_transmitted_distance, 0, reroute_transmission_in)
        self._set_socket(node_limit_trans_distance, 0, 0.0001)

        node_mix_transmitted_color = self._add_node__mix("Mix Transmitted Color", (-2283, -1879), parent=frame_transmission)
        self._link_socket(node_group_input, node_mix_transmitted_color, sock_transmitted_color, 6, reroute_transmission_in)
        self._link_socket(node_group_input, node_mix_transmitted_color, sock_transmitted_color_map, 7, reroute_transmission_in)

        node_transmitted_vol = self._add_node("ShaderNodeVolumeAbsorption", "Transmitted Volume Absorpsion", (-1718, -1927), parent=frame_transmission)
        self._link_socket(node_mix_transmitted_color, node_transmitted_vol, 2,0)
        self._link_socket(node_limit_trans_distance, node_transmitted_vol, 0,1)

        # Nodes: Surface and mixing
        s = PrincipledBSDFSockets
        node_main_layer_bsdf = self._add_node__princ_bdsf("Main Layer BSDF", (-1080, 160))
        self._link_socket(node_mix_diffuse_color, node_main_layer_bsdf, 2, s.BASE_COLOR, reroute_pbr_out)
        self._link_socket(node_mix_metallic_weight, node_main_layer_bsdf, 0, s.METALLIC, reroute_pbr_out)
        self._link_socket(node_mix_roughness_weight, node_main_layer_bsdf, 0, s.ROUGHNESS, reroute_pbr_out)
        self._link_socket(node_group_input, node_main_layer_bsdf, sock_ior, s.IOR, reroute_sss_ior)
        self._link_socket(node_mix_opacity, node_main_layer_bsdf, 0, s.ALPHA, reroute_pbr_out)
        self._link_socket(node_normal_reroute_right, node_main_layer_bsdf, 0, s.NORMAL)
        self._link_socket(node_group_input, node_main_layer_bsdf, sock_sss_weight, s.SUBSURFACE_WEIGHT, reroute_sss_ior)
        self._link_socket(node_group_input, node_main_layer_bsdf, sock_sss_color, s.SUBSURFACE_RADIUS, reroute_sss_ior)
        self._link_socket(node_group_input, node_main_layer_bsdf, sock_sss_scale, s.SUBSURFACE_SCALE, reroute_sss_ior)
        self._link_socket(node_group_input, node_main_layer_bsdf, sock_sss_direction, s.SUBSURFACE_ANISOTROPY, reroute_sss_ior)
        self._link_socket(node_mix_refraction_weight, node_main_layer_bsdf, 0, s.TRANSMISSION_WEIGHT, reroute_transmission_out)
        self._link_socket(node_mix_top_coat_weight, node_main_layer_bsdf, 0, s.COAT_WEIGHT, reroute_top_coat_out)
        self._link_socket(node_mix_top_coat_roughness, node_main_layer_bsdf, 0, s.COAT_ROUGHNESS, reroute_top_coat_out)
        self._link_socket(node_mix_top_coat_color, node_main_layer_bsdf, 2, s.COAT_TINT, reroute_top_coat_out)
        self._link_socket(node_normal_reroute_right, node_main_layer_bsdf, 0, s.COAT_NORMAL)
        self._link_socket(node_bb_emission, node_main_layer_bsdf, builder_emiss.out_color, s.EMISSION)
        self._link_socket(node_bb_emission, node_main_layer_bsdf, builder_emiss.out_weight, s.EMISSION_STRENGTH)
        self._link_socket(node_mix_thin_film, node_main_layer_bsdf, 0, s.THIN_FILM_THICKNESS)
        self._link_socket(node_mix_thin_film_ior, node_main_layer_bsdf, 0, s.THIN_FILM_IOR)

        node_mix_shader_trans = self._add_node__mix_shader("Mix Translucency Shader", (-720, 0))
        self._link_socket(node_translucency, node_mix_shader_trans, builder_trans.out_fac,0)
        self._link_socket(node_main_layer_bsdf, node_mix_shader_trans, 0,1)
        self._link_socket(node_translucency, node_mix_shader_trans, builder_flakes.out_shader,2)

        node_mix_shader_flakes = self._add_node__mix_shader("Mix Metallic Flakes Shader", (-540, 0))
        self._link_socket(node_flakes, node_mix_shader_flakes, builder_flakes.out_fac,0)
        self._link_socket(node_mix_shader_trans, node_mix_shader_flakes, 0,1)
        self._link_socket(node_flakes, node_mix_shader_flakes, builder_flakes.out_shader,2)

        node_mix_shader_overlay = self._add_node__mix_shader("Mix Diffuse Overlay Shader", (-360, 0))
        self._link_socket(node_overlay_sq_value, node_mix_shader_overlay, 0,0, reroute_diff_overlay_out)
        self._link_socket(node_mix_shader_flakes, node_mix_shader_overlay, 0,1)
        self._link_socket(node_overlay_bsdf, node_mix_shader_overlay, 0,2, reroute_diff_overlay_out)

        node_mix_shader_dls = self._add_node__mix_shader("Mix DLS Shader", (-180, 0))
        self._link_socket(node_dls, node_mix_shader_dls, builder_dls.out_fac,0)
        self._link_socket(node_mix_shader_overlay, node_mix_shader_dls, 0,1)
        self._link_socket(node_dls, node_mix_shader_dls, builder_dls.out_shader, 2)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0, 0))
        self._link_socket(node_mix_shader_dls, node_group_output, 0, sock_out_surface)
        self._link_socket(node_transmitted_vol, node_group_output, 0, sock_out_volume, reroute_transmission_out)
        self._link_socket(node_displacement, node_group_output, builder_disp.out_displacement, sock_out_displacement)

        # @formatter:on


class IrayUberPBRMRShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        if self._can_use_glass_shortcut(channels):
            fake_glass = FakeGlassShaderGroupApplier(self._properties, self._node_tree)
            fake_glass.apply_shader_group(channels)
            return

        super().apply_shader_group(channels)

        builder = IrayUberPBRMRShaderGroupBuilder

        # @formatter:off
        # Geometry Tiling
        self._set_material_mapping(channels, "horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset")

        # Base Diffuse
        self._channel_to_inputs("diffuse", builder.in_diffuse, builder.in_diffuse_map)
        self._channel_to_inputs('metallic_weight', builder.in_metallic_weight, builder.in_metallic_weight_map)
        self._channel_to_inputs('diffuse_roughness', builder.in_diffuse_roughness, builder.in_diffuse_roughness_map)

        if self._channel_enabled("glossy_roughness"):
            # Often the glossy roughness is used as diffuse roughness, override if it is.
            self._channel_to_inputs('glossy_roughness', builder.in_diffuse_roughness, builder.in_diffuse_roughness_map)
        elif self._channel_enabled("glossy_color"):
            # Often the glossy roughness is used as diffuse roughness, override if it is.
            self._channel_to_inputs('glossy_color', builder.in_diffuse_roughness, builder.in_diffuse_roughness_map)

        # Base Bump
        self._channel_to_inputs("bump_strength", builder.in_bump_strength, builder.in_bump_strength_map)
        self._channel_to_inputs("normal_map", builder.in_normal_map, builder.in_normal_map_map)

        # Base Diffuse Overlay
        if self._channel_enabled("diffuse_overlay_weight"):
            self._channel_to_inputs("diffuse_overlay_weight", builder.in_diffuse_overlay_weight, builder.in_diffuse_overlay_weight_map)
            self._channel_to_inputs("diffuse_overlay_weight_squared", builder.in_diffuse_overlay_weight_squared, None)
            self._channel_to_inputs("diffuse_overlay_color", builder.in_diffuse_overlay_color, builder.in_diffuse_overlay_color_map)
            self._channel_to_inputs("diffuse_overlay_roughness", builder.in_diffuse_overlay_roughness, builder.in_diffuse_overlay_roughness_map)

        # Base Diffuse Translucency
        if self._channel_enabled('translucency_weight'):
            self._channel_to_inputs("translucency_weight", builder.in_translucency_weight, builder.in_translucency_weight_map)
            self._channel_to_inputs("translucency_color", builder.in_translucency_color, builder.in_translucency_color_map)
            self._channel_to_inputs("invert_transmission_normal", builder.in_invert_transmission_normal, None)

        # Base Dual Lobe Specular
        if self._channel_enabled('sock_dual_lobe_specular_weight'):
            self._channel_to_inputs('dual_lobe_specular_weight', builder.in_dual_lobe_specular_weight, builder.in_dual_lobe_specular_weight_map)
            if self._properties.dls_weight_multiplier != 1.0:
                self._set_socket(self._shader_group, builder.in_dual_lobe_specular_weight, self._properties.dls_weight_multiplier, "MULTIPLY")

            self._channel_to_inputs('dual_lobe_specular_reflectivity', builder.in_dual_lobe_specular_reflectivity, builder.in_dual_lobe_specular_reflectivity_map)
            self._channel_to_inputs('specular_lobe_1_roughness', builder.in_specular_lobe_1_roughness, builder.in_specular_lobe_1_roughness_map)
            self._channel_to_inputs('specular_lobe_2_roughness', builder.in_specular_lobe_2_roughness, builder.in_specular_lobe_2_roughness_map)
            self._channel_to_inputs('dual_lobe_specular_ratio', builder.in_dual_lobe_specular_ratio, builder.in_dual_lobe_specular_ratio_map)

        # Base Thin Film
        self._channel_to_inputs("base_thin_film", builder.in_base_thin_film, None)
        self._channel_to_inputs("base_thin_film_ior", builder.in_base_thin_film_ior, builder.in_base_thin_film_ior_map)

        # Emission
        self._channel_to_inputs("emission_color", builder.in_emission_color, None)
        self._channel_to_inputs("emission_temperature", builder.in_emission_temperature, None)

        if self._channel_enabled('luminance'):
            self._channel_to_inputs('luminance', builder.in_luminance, builder.in_luminance_map)

            # Override luminance using units and efficacy
            b_luminance = self._convert_emission_luminance(channels)
            self._set_socket(self._shader_group, builder.in_luminance, b_luminance)

        # Geometry Cutout
        self._channel_to_inputs("cutout_opacity", builder.in_cutout_opacity, builder.in_cutout_opacity_map)

        # Geometry Displacement
        if self._channel_enabled("displacement_strength"):
            self._channel_to_inputs("displacement_strength", builder.in_displacement_strength, builder.in_displacement_strength_map)
            self._channel_to_inputs("minimum_displacement", builder.in_minimum_displacement, None)
            self._channel_to_inputs("maximum_displacement", builder.in_maximum_displacement, None)

        # Metallic Flakes Flakes
        if self._channel_enabled("metallic_flakes_weight"):
            self._channel_to_inputs("metallic_flakes_weight", builder.in_metallic_flakes_weight, builder.in_metallic_flakes_weight_map)
            self._channel_to_inputs("metallic_flakes_color", builder.in_metallic_flakes_color, builder.in_metallic_flakes_color_map)
            self._channel_to_inputs("metallic_flakes_roughness", builder.in_metallic_flakes_roughness, builder.in_metallic_flakes_roughness_map)
            self._channel_to_inputs("metallic_flakes_size", builder.in_metallic_flakes_size, None)
            self._channel_to_inputs("metallic_flakes_strength", builder.in_metallic_flakes_strength, None)
            self._channel_to_inputs("metallic_flakes_density", builder.in_metallic_flakes_density, None)

        # Top Coat General
        if self._channel_enabled("top_coat_weight"):
            self._channel_to_inputs("top_coat_weight", builder.in_top_coat_weight, builder.in_top_coat_weight_map)
            self._channel_to_inputs("top_coat_color", builder.in_top_coat_color, builder.in_top_coat_color_map)
            self._channel_to_inputs("top_coat_roughness", builder.in_top_coat_roughness, builder.in_top_coat_roughness_map)

        # Volume Scattering
        if self._channel_enabled("sss_amount"):
            self._channel_to_inputs("sss_amount", builder.in_sss_weight, None)
            self._channel_to_inputs("scattering_measurement_distance", builder.in_scattering_measurement_distance, None)
            self._channel_to_inputs("sss_color", builder.in_sss_color, None)
            self._channel_to_inputs("sss_direction", builder.in_sss_direction, None)

        # Volume Transmission
        if self._channel_enabled("refraction_weight"):
            self._channel_to_inputs("refraction_weight", builder.in_refraction_weight, builder.in_refraction_weight_map)
            self._channel_to_inputs("refraction_index", builder.in_ior, None)
            self._channel_to_inputs("transmitted_measurement_distance", builder.in_transmitted_measurement_distance, None)
            self._channel_to_inputs("transmitted_color", builder.in_transmitted_color, builder.in_transmitted_color_map)
        # @formatter:on

    @staticmethod
    def _convert_emission_luminance(channels) -> float:
        base_luminance = channels['luminance'].value

        if "luminance_units" in channels:
            unit_opt = channels['luminance_units'].value

            if unit_opt == 1:  # kcd/m^2
                multiplier = 1000
            elif unit_opt == 2:  # cd/ft^2
                multiplier = 10.7639
            elif unit_opt == 3:  # cd/cm^2
                multiplier = 10000
            elif unit_opt == 4:  # lumen → Watts using efficacy
                if "luminous_efficacy" in channels:
                    multiplier = 1.0 / max(channels['luminous_efficacy'].value, 1e-6)
                else:
                    multiplier = 1.0 / 15
            else:  # cd/m^2 and Watts
                multiplier = 1

            return base_luminance * multiplier
        else:
            return base_luminance

    @staticmethod
    def _can_use_glass_shortcut(channels):
        """
        If the refraction weight is 1 and the refraction index is 1.38 we can take a shortcut and use the
        fake glass shader group, instead of the full Iray Uber setup.
        """
        refraction_weight_ch = channels.get("refraction_weight", None)
        refraction_index_ch = channels.get("refraction_index", None)

        if refraction_weight_ch is not None and refraction_index_ch is not None:
            return refraction_weight_ch.value == 1 and refraction_index_ch.value == 1.38
