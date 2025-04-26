from typing import Type

from bpy.types import ShaderNodeBsdfDiffuse, ShaderNodeVolumeAbsorption, ShaderNodeBsdfTransparent, \
    ShaderNodeBsdfMetallic, ShaderNodeSubsurfaceScattering, ShaderNodeBsdfRefraction

from .support import AdvancedTopCoatShaderGroupBuilder, FakeGlassShaderGroupApplier, FakeGlassShaderGroupBuilder, \
    ShaderGroupApplier, ShaderGroupBuilder, RerouteGroup, AsymmetricalDisplacementShaderGroupBuilder, \
    DualLobeSpecularShaderGroupBuilder, BlackbodyEmissionShaderGroupBuilder, MetallicFlakesShaderGroupBuilder, \
    WeightedTranslucencyShaderGroupBuilder
from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "Iray Uber"
__MATERIAL_TYPE_ID__ = "iray_uber"


class IrayUberShaderGroupBuilder(ShaderGroupBuilder):
    """
    About Iray Uber, decisions had to be made.
    Given Iray Uber has 166 adjustable properties (counting values and maps separately).
    If all properties were to be implemented, this group would become a massive undertaking.

    So here's the decisions taken:
    - Only map and implement commonly used properties
    - Instead of building a shader for each Base Mising Type, this shader tries it's best to be the middle ground.
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

    # Glossy
    in_glossy_weight = "Glossy Weight"
    in_glossy_weight_map = "Glossy Weight Map"
    in_glossy_color = "Glossy Color"
    in_glossy_color_map = "Glossy Color Map"
    in_glossy_reflectivity = "Glossy Reflectivity"
    in_glossy_reflectivity_map = "Glossy Reflectivity Map"
    in_glossy_roughness = "Glossy Roughness"
    in_glossy_roughness_map = "Glossy Roughness Map"
    in_glossy_anisotropy = "Glossy Anisotropy"
    in_glossy_anisotropy_map = "Glossy Anisotropy Map"
    in_glossy_anisotropy_rotations = "Glossy Anisotropy Rotations"
    in_glossy_anisotropy_rotations_map = "Glossy Anisotropy Rotations Map"

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

    # Base Thin Film
    in_thin_film_weight = "Thin Film Weight"
    in_thin_film_rotations = "Thin Film Iridescent Rotations"
    in_thin_film_thickness = "Thin Film Thickness"
    in_thin_film_thickness_map = "Thin Film Thickness Map"
    in_thin_film_ior = "Thin Film IOR"
    in_thin_film_ior_map = "Thin Film IOR Map"

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
            AdvancedTopCoatShaderGroupBuilder,
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
        panel_base_diffuse = self._add_panel("Diffuse", False)
        panel_base_bump = self._add_panel("Bump", False)
        panel_base_diffuse_overlay = self._add_panel("Diffuse Overlay")
        panel_base_diffuse_translucency = self._add_panel("Diffuse Translucency")
        panel_base_dual_lobe_specular = self._add_panel("Dual Lobe Specular")
        panel_glossy = self._add_panel("Glossy")
        panel_emission = self._add_panel("Emission")
        panel_geometry_cutout = self._add_panel("Geometry Cutout")
        panel_geometry_displacement = self._add_panel("Geometry Displacement")
        panel_metallic_flakes_flakes = self._add_panel("Metallic Flakes Flakes")
        panel_top_coat_general = self._add_panel("Top Coat")
        panel_base_thin_film = self._add_panel("Thin Film")
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
        sock_normal_map = self._color_socket(self.in_normal_map_map, (0.5, 0.5, 1.0, 1.0), parent=panel_base_bump)
        sock_bump_strength = self._float_socket(self.in_bump_strength, parent=panel_base_bump)
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

        # Sockets: Glossy Layer
        sock_glossy_weight = self._float_socket(self.in_glossy_weight, parent=panel_glossy)
        sock_glossy_weight_map = self._color_socket(self.in_glossy_weight_map, parent=panel_glossy)
        sock_glossy_color = self._color_socket(self.in_glossy_color, parent=panel_glossy)
        sock_glossy_color_map = self._color_socket(self.in_glossy_color_map, parent=panel_glossy)
        sock_glossy_reflectivity = self._float_socket(self.in_glossy_reflectivity, 0.5, parent=panel_glossy)
        sock_glossy_reflectivity_map = self._color_socket(self.in_glossy_reflectivity_map, parent=panel_glossy)
        sock_glossy_roughness = self._float_socket(self.in_glossy_roughness, parent=panel_glossy)
        sock_glossy_roughness_map = self._color_socket(self.in_glossy_roughness_map, parent=panel_glossy)
        sock_glossy_anisotropy = self._float_socket(self.in_glossy_anisotropy, parent=panel_glossy)
        sock_glossy_anisotropy_map = self._color_socket(self.in_glossy_anisotropy_map, parent=panel_glossy)
        sock_glossy_anisotropy_rotations = self._float_socket(self.in_glossy_anisotropy_rotations, parent=panel_glossy)
        sock_glossy_anisotropy_rotations_map = self._color_socket(self.in_glossy_anisotropy_rotations_map, parent=panel_glossy)

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

        # Sockets: Base Thin Film
        sock_thin_film_weight = self._float_socket(self.in_thin_film_weight, parent=panel_base_thin_film)
        sock_thin_film_rotations = self._float_socket(self.in_thin_film_rotations, parent=panel_base_thin_film)
        sock_thin_film_thickness = self._float_socket(self.in_thin_film_thickness, parent=panel_base_thin_film)
        sock_thin_film_thickness_map = self._color_socket(self.in_thin_film_thickness_map, parent=panel_base_thin_film)
        sock_thin_film_ior = self._float_socket(self.in_thin_film_ior, 1.5, parent=panel_base_thin_film)
        sock_thin_film_ior_map = self._color_socket(self.in_thin_film_ior_map, parent=panel_base_thin_film)

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
        sock_transmitted_color = self._color_socket(self.in_transmitted_color, parent=panel_volume_transmission)
        sock_transmitted_color_map = self._color_socket(self.in_transmitted_color_map, parent=panel_volume_transmission)

        # Output Sockets:
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")
        sock_out_volume = self._shader_socket(self.out_volume, in_out="OUTPUT")
        sock_out_displacement = self._vector_socket(self.out_displacement, in_out="OUTPUT")

        # Frames and Reroute Groups
        frame_base = self._add_frame("Base")
        reroute_base_in = RerouteGroup(-2000.0, 800.0, frame_base)
        reroute_base_out = RerouteGroup(-1360.0, 800.0, frame_base)

        frame_normal = self._add_frame("Normal")
        reroute_normal_in = RerouteGroup(-3040.0, 640.0, frame_normal)

        frame_diff_overlay = self._add_frame("Diffuse Overlay")
        reroute_diff_overlay_in = RerouteGroup(-2000.0, 220.0, frame_diff_overlay)
        reroute_diff_overlay_out = RerouteGroup(-1360.0, 220.0, frame_diff_overlay)

        frame_transmission = self._add_frame("Refraction and Tranmission")
        reroute_transmission_in = RerouteGroup(-2000.0, 440.0, frame_transmission)
        reroute_transmission_out = RerouteGroup(-1360.0, 440.0, frame_transmission)

        reroute_passthrough_in = RerouteGroup(-2000.0, -1320.0)
        reroute_passthrough_out = RerouteGroup(-1600.0, -1320.0)
        reroute_passthrough = (reroute_passthrough_in, reroute_passthrough_out)

        # Builder refs
        translucency_b = WeightedTranslucencyShaderGroupBuilder
        dls_b = DualLobeSpecularShaderGroupBuilder
        emission_b = BlackbodyEmissionShaderGroupBuilder
        displacement_b = AsymmetricalDisplacementShaderGroupBuilder
        mflakes_b = MetallicFlakesShaderGroupBuilder
        top_coat_b = AdvancedTopCoatShaderGroupBuilder

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-3320.0, 400.0))

        # Nodes: Normal and Bump
        node_normal_map = self._add_node__normal_map("Normal Map", (-3000.0, 640.0), frame_normal)
        self._link_socket(node_group_input, node_normal_map, sock_normal, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_normal_map, sock_normal_map, 1, reroute_normal_in)

        node_bump = self._add_node__bump("Bump", (-3000.0, 600.0), frame_normal)
        self._link_socket(node_group_input, node_bump, sock_bump_strength, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_bump, sock_bump_strength_map, 2, reroute_normal_in)
        self._link_socket(node_normal_map, node_bump, 0, 3)

        # Nodes: PBR
        node_mix_diffuse_color = self._add_node__mix("Mix Diffuse Color", (-1900.0, 800.0), parent=frame_base)
        self._link_socket(node_group_input, node_mix_diffuse_color, sock_diffuse, 6, reroute_base_in)
        self._link_socket(node_group_input, node_mix_diffuse_color, sock_diffuse_map, 7, reroute_base_in)

        node_mix_diffuse_roughness = self._add_node__hsv("Mix Diffuse Roughness", (-1900.0, 760.0), parent=frame_base)
        self._link_socket(node_group_input, node_mix_diffuse_roughness, sock_diffuse_roughness, 2, reroute_base_in)
        self._link_socket(node_group_input, node_mix_diffuse_roughness, sock_diffuse_roughness_map, 4, reroute_base_in)

        node_mix_metallic_weight = self._add_node__hsv("Mix Metallic Weight", (-1900.0, 720.0), parent=frame_base)
        self._link_socket(node_group_input, node_mix_metallic_weight, sock_metallic_weight, 2, reroute_base_in)
        self._link_socket(node_group_input, node_mix_metallic_weight, sock_metallic_weight_map, 4, reroute_base_in)

        node_mix_cutout_opacity = self._add_node__hsv("Mix Cutout Opacity", (-1900.0, 680.0), parent=frame_base)
        self._link_socket(node_group_input, node_mix_cutout_opacity, sock_cutout_opacity, 2, reroute_base_in)
        self._link_socket(node_group_input, node_mix_cutout_opacity, sock_cutout_opacity_map, 4, reroute_base_in)

        node_diffuse_bsdf = self._add_node(ShaderNodeBsdfDiffuse, "Diffuse BSDF", (-1660.0, 780.0), frame_base)
        self._link_socket(node_mix_diffuse_color, node_diffuse_bsdf, 2, 0)
        self._link_socket(node_mix_diffuse_roughness, node_diffuse_bsdf, 0, 1)
        self._link_socket(node_bump, node_diffuse_bsdf, 0, 2, reroute_base_in)

        node_transparent_bsdf = self._add_node(ShaderNodeBsdfTransparent, "Transparent BSDF", (-1660.0, 740.0), frame_base)

        node_metallic_bsdf = self._add_node(ShaderNodeBsdfMetallic, "Metallic BSDF", (-1660.0, 680.0), frame_base)
        self._link_socket(node_mix_diffuse_color, node_metallic_bsdf, 2, 0)
        self._link_socket(node_mix_diffuse_roughness, node_metallic_bsdf, 0, 2)
        self._link_socket(node_bump, node_metallic_bsdf, 0, 7, reroute_base_in)

        node_subsurf_bsdf = self._add_node(ShaderNodeSubsurfaceScattering, "Subsurface Scattering", (-1660.0, 620.0), frame_base)
        self._link_socket(node_group_input, node_subsurf_bsdf, sock_sss_color, 0, reroute_base_in)
        self._link_socket(node_group_input, node_subsurf_bsdf, sock_sss_scale, 1, reroute_base_in)
        self._link_socket(node_group_input, node_subsurf_bsdf, sock_ior, 3, reroute_base_in)
        self._link_socket(node_group_input, node_subsurf_bsdf, sock_sss_direction, 4, reroute_base_in)
        self._link_socket(node_bump, node_subsurf_bsdf, 0, 5, reroute_base_in)

        # Nodes: Refraction and Tranmission
        node_mix_refraction_weight = self._add_node__hsv("Mix Refraction Weight", (-1940.0, 420.0), frame_transmission)
        self._link_socket(node_group_input, node_mix_refraction_weight, sock_refraction_weight, 2, reroute_transmission_in)
        self._link_socket(node_group_input, node_mix_refraction_weight, sock_refraction_weight_map, 4, reroute_transmission_in)

        node_limit_transmitted_dst = self._add_node__math("Limit Transmitted Distance", (-1940.0, 380.0), "MAXIMUM", parent=frame_transmission)
        self._link_socket(node_group_input, node_limit_transmitted_dst, sock_transmitted_distance, 0, reroute_transmission_in)
        self._set_socket(node_limit_transmitted_dst, 1, 0.001)

        node_mix_transmitted_color = self._add_node__mix("Mix Transmitted Color", (-1940.0, 340.0), parent=frame_transmission)
        self._link_socket(node_group_input, node_mix_transmitted_color, sock_transmitted_color, 6, reroute_transmission_in)
        self._link_socket(node_group_input, node_mix_transmitted_color, sock_transmitted_color_map, 7, reroute_transmission_in)

        node_refraction_bsdf = self._add_node(ShaderNodeBsdfRefraction, "Refraction BSDF", (-1740.0, 420.0), frame_transmission)
        self._link_socket(node_group_input, node_refraction_bsdf, sock_ior, 2, reroute_transmission_in)
        self._link_socket(node_bump, node_refraction_bsdf, 0, 3, reroute_transmission_in)

        node_transmitted_volume = self._add_node(ShaderNodeVolumeAbsorption, "Transmitted Volume", (-1740.0, 380.0), frame_transmission)
        self._link_socket(node_mix_transmitted_color, node_transmitted_volume, 2, 0)
        self._link_socket(node_limit_transmitted_dst, node_transmitted_volume, 0, 1)

        # Nodes: Diffuse Overlay
        node_mix_overlay_weight = self._add_node__hsv("Mix Overlay Weight", (-1940.0, 220.0), frame_diff_overlay)
        self._link_socket(node_group_input, node_mix_overlay_weight, sock_diffuse_overlay_weight, 2, reroute_diff_overlay_in)
        self._link_socket(node_group_input, node_mix_overlay_weight, sock_diffuse_overlay_weight_map, 4, reroute_diff_overlay_in)

        node_overlay_squared_exponent = self._add_node__math("Overlay Squared Exponent", (-1940.0, 180.0), "POWER", frame_diff_overlay)
        self._link_socket(node_group_input, node_overlay_squared_exponent, sock_diffuse_overlay_weight_squared, 0, reroute_diff_overlay_in)
        self._set_socket(node_overlay_squared_exponent, 1, 2)

        node_mix_overlay_color = self._add_node__mix("Mix Overlay Color", (-1940.0, 140.0), parent=frame_diff_overlay)
        self._link_socket(node_group_input, node_mix_overlay_color, sock_diffuse_overlay_color, 6, reroute_diff_overlay_in)
        self._link_socket(node_group_input, node_mix_overlay_color, sock_diffuse_overlay_color_map, 7, reroute_diff_overlay_in)

        node_mix_overlay_roughness = self._add_node__hsv("Mix Overlay Roughness", (-1940.0, 100.0), parent=frame_diff_overlay)
        self._link_socket(node_group_input, node_mix_overlay_roughness, sock_diffuse_overlay_roughness, 2, reroute_diff_overlay_in)
        self._link_socket(node_group_input, node_mix_overlay_roughness, sock_diffuse_overlay_roughness_map, 4, reroute_diff_overlay_in)

        node_overlay_squared_weight = self._add_node__math("Overlay Squared Weight", (-1740.0, 200.0), "MULTIPLY", frame_diff_overlay)
        self._link_socket(node_mix_overlay_weight, node_overlay_squared_weight, 0, 0)
        self._link_socket(node_mix_overlay_weight, node_overlay_squared_exponent, 0, 1)

        node_overlay_layer_bsdf = self._add_node(ShaderNodeBsdfDiffuse, "Overlay Layer BSDF", (-1740.0, 160.0), frame_diff_overlay)
        self._link_socket(node_mix_overlay_color, node_overlay_layer_bsdf, 2, 0)
        self._link_socket(node_mix_overlay_roughness, node_overlay_layer_bsdf, 0, 1)
        self._link_socket(node_bump, node_overlay_layer_bsdf, 0, 2, reroute_diff_overlay_in)

        # Nodes: Translucency
        node_translucency = self._add_node__shader_group("Translucency", translucency_b, (-2000.0, 20.0))
        self._link_socket(node_bump, node_translucency, 0, translucency_b.in_normal)
        self._link_socket(node_group_input, node_translucency, sock_translucency_weight, translucency_b.in_translucency_weight)
        self._link_socket(node_group_input, node_translucency, sock_translucency_weight_map, translucency_b.in_translucency_weight_map)
        self._link_socket(node_group_input, node_translucency, sock_translucency_color, translucency_b.in_translucency_color)
        self._link_socket(node_group_input, node_translucency, sock_translucency_color_map, translucency_b.in_translucency_color_map)
        self._link_socket(node_group_input, node_translucency, sock_invert_transmission_normal, translucency_b.in_invert_transmission_normal)

        # Nodes: DLS
        node_dls = self._add_node__shader_group("DLS", dls_b, (-2000.0, -220.0))
        self._link_socket(node_bump, node_dls, 0, dls_b.in_normal)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_weight, dls_b.in_weight)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_weight_map, dls_b.in_weight_map)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_reflectivity, dls_b.in_reflectivity)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_reflectivity_map, dls_b.in_reflectivity_map)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_1_roughness, dls_b.in_l1_roughness)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_1_roughness_map, dls_b.in_l1_roughness_map)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_2_roughness, dls_b.in_l2_roughness_mult)
        self._link_socket(node_group_input, node_dls, sock_specular_lobe_2_roughness_map, dls_b.in_l2_roughness_mult_map)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_ratio, dls_b.in_ratio)
        self._link_socket(node_group_input, node_dls, sock_dual_lobe_specular_ratio_map, dls_b.in_ratio_map)

        # Nodes: Emission
        node_emission = self._add_node__shader_group("Emission", emission_b, (-2000.0, -580.0))
        self._link_socket(node_group_input, node_emission, sock_emission_color, emission_b.in_color)
        self._link_socket(node_group_input, node_emission, sock_emission_color_map, emission_b.in_color_map)
        self._link_socket(node_group_input, node_emission, sock_emission_temperature, emission_b.in_temperature)
        self._link_socket(node_group_input, node_emission, sock_luminance, emission_b.in_luminance)
        self._link_socket(node_group_input, node_emission, sock_luminance_map, emission_b.in_luminance_map)
        self._link_socket(node_group_input, node_emission, sock_luminance_map, emission_b.in_luminance_map)

        # Nodes: Displacement
        node_displacement = self._add_node__shader_group("Displacement", displacement_b, (-2000.0, -800.0))
        self._link_socket(node_bump, node_displacement, 0, displacement_b.in_normal)
        self._link_socket(node_group_input, node_displacement, sock_displacement_strength, displacement_b.in_strength)
        self._link_socket(node_group_input, node_displacement, sock_displacement_strength_map, displacement_b.in_strength_map)
        self._link_socket(node_group_input, node_displacement, sock_minimum_displacement, displacement_b.in_min_displacement)
        self._link_socket(node_group_input, node_displacement, sock_maximum_displacement, displacement_b.in_max_displacement)

        # Nodes: Metallic Flakes
        node_mflakes = self._add_node__shader_group("Metallic Flakes", mflakes_b, (-2000.0, -1000.0))
        self._link_socket(node_bump, node_mflakes, 0, mflakes_b.in_normal)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_weight, mflakes_b.in_weight)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_weight_map, mflakes_b.in_weight_map)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_color, mflakes_b.in_color)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_color_map, mflakes_b.in_color_map)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_roughness, mflakes_b.in_roughness)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_roughness_map, mflakes_b.in_roughness_map)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_size, mflakes_b.in_flake_size)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_strength, mflakes_b.in_flake_strength)
        self._link_socket(node_group_input, node_mflakes, sock_metallic_flakes_density, mflakes_b.in_flake_density)

        # Nodes: Glossy
        node_glossy = self._add_node__shader_group("Glossy", top_coat_b, (-880.0, -580.0))
        self._link_socket(node_bump, node_glossy, 0, top_coat_b.in_top_coat_bump_vector, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_weight, top_coat_b.in_top_coat_weight, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_weight_map, top_coat_b.in_top_coat_weight_map, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_color, top_coat_b.in_top_coat_color, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_color_map, top_coat_b.in_top_coat_color_map, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_roughness, top_coat_b.in_top_coat_roughness, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_roughness_map, top_coat_b.in_top_coat_roughness_map, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_reflectivity, top_coat_b.in_top_coat_reflectivity, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_reflectivity_map, top_coat_b.in_top_coat_reflectivity_map, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_anisotropy, top_coat_b.in_top_coat_anisotropy, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_anisotropy_map, top_coat_b.in_top_coat_anisotropy_map, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_anisotropy_rotations, top_coat_b.in_top_coat_rotations, reroute_passthrough)
        self._link_socket(node_group_input, node_glossy, sock_glossy_anisotropy_rotations_map, top_coat_b.in_top_coat_rotations_map, reroute_passthrough)

        # Nodes: Top Coat
        node_top_coat = self._add_node__shader_group("Top Coat", top_coat_b, (-880.0, -1220.0))
        self._link_socket(node_bump, node_top_coat, 0, top_coat_b.in_top_coat_bump_vector, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_weight, top_coat_b.in_top_coat_weight, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_weight_map, top_coat_b.in_top_coat_weight_map, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_color, top_coat_b.in_top_coat_color, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_color_map, top_coat_b.in_top_coat_color_map, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_roughness, top_coat_b.in_top_coat_roughness, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_roughness_map, top_coat_b.in_top_coat_roughness_map, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_weight, top_coat_b.in_thin_film_weight, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_rotations, top_coat_b.in_thin_film_rotations, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_thickness, top_coat_b.in_thin_film_thickness, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_thickness_map, top_coat_b.in_thin_film_thickness_map, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_ior, top_coat_b.in_thin_film_ior, reroute_passthrough)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_ior_map, top_coat_b.in_thin_film_ior_map, reroute_passthrough)

        # Nodes: Mix Shaders
        node_mix_shader_subsurf = self._add_node__mix_shader("Mix Subsurface Scattering", (-220.0, 340.0))
        self._link_socket(node_group_input, node_mix_shader_subsurf, sock_sss_weight, 0, (reroute_base_in, reroute_base_out))
        self._link_socket(node_diffuse_bsdf, node_mix_shader_subsurf, 0,1, reroute_base_out)
        self._link_socket(node_subsurf_bsdf, node_mix_shader_subsurf, 0,2, reroute_base_out)

        node_mix_shader_metallic = self._add_node__mix_shader("Mix Metallic Shader", (-220.0, 300.0))
        self._link_socket(node_mix_metallic_weight, node_mix_shader_metallic, 0, 0, reroute_base_out)
        self._link_socket(node_mix_shader_subsurf, node_mix_shader_metallic, 0, 1)
        self._link_socket(node_metallic_bsdf, node_mix_shader_metallic, 0, 2, reroute_base_out)

        node_mix_shader_refraction = self._add_node__mix_shader("Mix Refraction Shader", (-220.0, 260.0))
        self._link_socket(node_mix_refraction_weight, node_mix_shader_refraction, 0, 0, reroute_transmission_out)
        self._link_socket(node_mix_shader_metallic, node_mix_shader_refraction, 0, 1)
        self._link_socket(node_refraction_bsdf, node_mix_shader_refraction, 0, 2, reroute_transmission_out)

        node_mix_shader_translucency = self._add_node__mix_shader("Mix Translucency Shader", (-220.0, 220.0))
        self._link_socket(node_translucency, node_mix_shader_translucency, translucency_b.out_fac, 0)
        self._link_socket(node_mix_shader_refraction, node_mix_shader_translucency, 0, 1)
        self._link_socket(node_translucency, node_mix_shader_translucency, translucency_b.out_shader, 2)

        node_mix_shader_mflakes = self._add_node__mix_shader("Mix Metallic Flakes Shader", (-220.0, 180.0))
        self._link_socket(node_mflakes, node_mix_shader_mflakes, mflakes_b.out_fac, 0)
        self._link_socket(node_mix_shader_translucency, node_mix_shader_mflakes, 0, 1)
        self._link_socket(node_mflakes, node_mix_shader_mflakes, mflakes_b.out_shader, 2)

        node_mix_shader_dls = self._add_node__mix_shader("Mix DLS Shader", (-220.0, 140.0))
        self._link_socket(node_dls, node_mix_shader_dls, dls_b.out_fac, 0)
        self._link_socket(node_mix_shader_mflakes, node_mix_shader_dls, 0, 1)
        self._link_socket(node_dls, node_mix_shader_dls, dls_b.out_shader, 2)

        node_mix_shader_glossy = self._add_node__mix_shader("Mix Glossy Shader", (-220.0, 100.0))
        self._link_socket(node_glossy, node_mix_shader_glossy, top_coat_b.out_fac, 0)
        self._link_socket(node_mix_shader_dls, node_mix_shader_glossy, 0, 1)
        self._link_socket(node_glossy, node_mix_shader_glossy, top_coat_b.out_shader, 2)

        node_mix_shader_top_coat = self._add_node__mix_shader("Mix Top Coat Shader", (-220.0, 60.0))
        self._link_socket(node_top_coat, node_mix_shader_top_coat, top_coat_b.out_fac, 0)
        self._link_socket(node_mix_shader_glossy, node_mix_shader_top_coat, 0, 1)
        self._link_socket(node_top_coat, node_mix_shader_top_coat, top_coat_b.out_shader, 2)

        node_mix_shader_emission = self._add_node__mix_shader("Mix Emission Shader", (-220.0, 20.0))
        self._link_socket(node_emission, node_mix_shader_emission, emission_b.out_fac, 0)
        self._link_socket(node_mix_shader_top_coat, node_mix_shader_emission, 0, 1)
        self._link_socket(node_emission, node_mix_shader_emission, emission_b.out_shader, 2)

        node_mix_shader_transparency = self._add_node__mix_shader("Mix Transparency Shader", (-220.0, -20.0))
        self._link_socket(node_mix_cutout_opacity, node_mix_shader_transparency, 0, 0, reroute_base_out)
        self._link_socket(node_transparent_bsdf, node_mix_shader_transparency, 0, 1, reroute_base_out)
        self._link_socket(node_mix_shader_emission, node_mix_shader_transparency, 0, 2)

        node_mix_shader_overlay = self._add_node__mix_shader("Mix Overlay Shader", (-220.0, -60.0))
        self._link_socket(node_overlay_squared_weight, node_mix_shader_overlay, 0, 0, reroute_diff_overlay_out)
        self._link_socket(node_mix_shader_transparency, node_mix_shader_overlay, 0, 1)
        self._link_socket(node_overlay_layer_bsdf, node_mix_shader_overlay, 0, 2, reroute_diff_overlay_out)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0, 0))
        self._link_socket(node_mix_shader_overlay, node_group_output, 0, sock_out_surface)
        self._link_socket(node_transmitted_volume, node_group_output, 0, sock_out_volume, reroute_transmission_out)
        self._link_socket(node_displacement, node_group_output, displacement_b.out_displacement, sock_out_displacement)
        # @formatter:on

        self.hide_all_nodes(node_group_input,
                            node_translucency,
                            node_dls,
                            node_emission,
                            node_displacement,
                            node_mflakes,
                            node_glossy,
                            node_top_coat,
                            node_group_output)


class IrayUberShaderGroupApplier(ShaderGroupApplier):

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        self._channels = channels

        if self._can_use_glass_shortcut():
            fake_glass = FakeGlassShaderGroupApplier(self._properties, self._node_tree)
            fake_glass.apply_shader_group(channels)
            return

        super().apply_shader_group(channels)

        builder = IrayUberShaderGroupBuilder

        # @formatter:off
        # Geometry Tiling
        self._set_material_mapping("horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset")

        # Base Diffuse
        self._channel_to_sockets("diffuse", builder.in_diffuse, builder.in_diffuse_map, False)
        self._channel_to_sockets('metallic_weight', builder.in_metallic_weight, builder.in_metallic_weight_map)

        if self._channel_enabled('diffuse_roughness'):
            # For some reason the diffuse roughness is set to 0 by default.
            # This makes the shader very glossy in Blender, hence we only set it if it's non-zero.
            self._channel_to_sockets('diffuse_roughness', builder.in_diffuse_roughness, builder.in_diffuse_roughness_map)

        # Base Bump
        self._channel_to_sockets("bump_strength", builder.in_bump_strength, builder.in_bump_strength_map)
        self._channel_to_sockets("normal_map", builder.in_normal_map, builder.in_normal_map_map)

        if self._channel_enabled("bump_strength"):
            self._set_socket(self._shader_group, builder.in_bump_strength, 0.01, "MULTIPLY")

        # Base Diffuse Overlay
        if self._channel_enabled("diffuse_overlay_weight"):
            self._channel_to_sockets("diffuse_overlay_weight", builder.in_diffuse_overlay_weight, builder.in_diffuse_overlay_weight_map)
            self._channel_to_sockets("diffuse_overlay_weight_squared", builder.in_diffuse_overlay_weight_squared, None)
            self._channel_to_sockets("diffuse_overlay_color", builder.in_diffuse_overlay_color, builder.in_diffuse_overlay_color_map, False)
            self._channel_to_sockets("diffuse_overlay_roughness", builder.in_diffuse_overlay_roughness, builder.in_diffuse_overlay_roughness_map)

        # Base Diffuse Translucency
        if self._channel_enabled('translucency_weight'):
            self._channel_to_sockets("translucency_weight", builder.in_translucency_weight, builder.in_translucency_weight_map)
            self._channel_to_sockets("translucency_color", builder.in_translucency_color, builder.in_translucency_color_map, False)
            self._channel_to_sockets("invert_transmission_normal", builder.in_invert_transmission_normal, None)

        # Base Dual Lobe Specular
        if self._channel_enabled('dual_lobe_specular_weight'):
            self._channel_to_sockets('dual_lobe_specular_weight', builder.in_dual_lobe_specular_weight, builder.in_dual_lobe_specular_weight_map)
            if self._properties.dls_weight_multiplier != 1.0:
                self._set_socket(self._shader_group, builder.in_dual_lobe_specular_weight, self._properties.dls_weight_multiplier, "MULTIPLY")

            self._channel_to_sockets('dual_lobe_specular_reflectivity', builder.in_dual_lobe_specular_reflectivity, builder.in_dual_lobe_specular_reflectivity_map)
            self._channel_to_sockets('specular_lobe_1_roughness', builder.in_specular_lobe_1_roughness, builder.in_specular_lobe_1_roughness_map)
            self._channel_to_sockets('specular_lobe_2_roughness', builder.in_specular_lobe_2_roughness, builder.in_specular_lobe_2_roughness_map)
            self._channel_to_sockets('dual_lobe_specular_ratio', builder.in_dual_lobe_specular_ratio, builder.in_dual_lobe_specular_ratio_map)

        # Glossy Layer
        self._channel_to_sockets("glossy_weight", builder.in_glossy_weight, builder.in_glossy_weight_map)
        self._channel_to_sockets("glossy_reflectivity", builder.in_glossy_reflectivity, builder.in_glossy_reflectivity_map)
        self._channel_to_sockets("glossy_anisotropy", builder.in_glossy_anisotropy, builder.in_glossy_anisotropy_map)
        self._channel_to_sockets("glossy_anisotropy_rotations", builder.in_glossy_anisotropy_rotations, builder.in_glossy_anisotropy_rotations)

        # Remap Glossy Color to Roughness
        if (self._properties.iray_uber_remap_glossy_color_to_roughness
                and self._channel_enabled("glossy_color")
                and not self._channel_enabled("glossy_roughness")):
            self._channel_to_sockets("glossy_color", builder.in_glossy_roughness, builder.in_glossy_roughness_map)
        else:
            self._channel_to_sockets("glossy_color", builder.in_glossy_color, builder.in_glossy_color_map)
            self._channel_to_sockets("glossy_roughness", builder.in_glossy_roughness, builder.in_glossy_roughness_map)

        if not self._channel_enabled("glossy_weight") and self._channel_enabled("glossy_color", "glossy_reflectivity", "glossy_roughness"):
            # Glossy Weight is only set in weighted mode.
            # So if it's set we leave it alone, else we check whether any of its props are set.
            # When that is true we set the weight to 1.
            self._set_socket(self._shader_group, builder.in_glossy_weight, 1.0)

        # Base Thin Film
        if self._channel_enabled("thin_film_thickness"):
            self._set_socket(self._shader_group, builder.in_thin_film_weight, 0.5)
            self._channel_to_sockets("thin_film_thickness", builder.in_thin_film_thickness, builder.in_thin_film_thickness_map)
            self._channel_to_sockets("thin_film_ior", builder.in_thin_film_ior, builder.in_thin_film_ior_map)

        # Emission
        self._channel_to_sockets("emission_color", builder.in_emission_color, builder.in_emission_color_map)
        self._channel_to_sockets("emission_temperature", builder.in_emission_temperature, None)

        # Emission clamping
        emission_color = self._channel_value("emission_color")
        emission_max_rgb = max(emission_color[0], emission_color[1], emission_color[2])
        if 0 <= emission_max_rgb <= self._properties.iray_uber_clamp_emission:
            self._set_socket(self._shader_group, builder.in_emission_color, (0.0, 0.0, 0.0, 1.0))

        if self._channel_enabled('luminance'):
            self._channel_to_sockets('luminance', builder.in_luminance, builder.in_luminance_map)

            # Override luminance using units and efficacy
            b_luminance = self._calculate_emission_luminance()
            self._set_socket(self._shader_group, builder.in_luminance, b_luminance)

        # Geometry Cutout
        self._channel_to_sockets("cutout_opacity", builder.in_cutout_opacity, builder.in_cutout_opacity_map)

        # Geometry Displacement
        if self._channel_enabled("displacement_strength"):
            self._channel_to_sockets("displacement_strength", builder.in_displacement_strength, builder.in_displacement_strength_map)
            self._channel_to_sockets("minimum_displacement", builder.in_minimum_displacement, None)
            self._channel_to_sockets("maximum_displacement", builder.in_maximum_displacement, None)

        # Metallic Flakes Flakes
        if self._channel_enabled("metallic_flakes_weight"):
            self._channel_to_sockets("metallic_flakes_weight", builder.in_metallic_flakes_weight, builder.in_metallic_flakes_weight_map)
            self._channel_to_sockets("metallic_flakes_color", builder.in_metallic_flakes_color, builder.in_metallic_flakes_color_map, False)
            self._channel_to_sockets("metallic_flakes_roughness", builder.in_metallic_flakes_roughness, builder.in_metallic_flakes_roughness_map)
            self._channel_to_sockets("metallic_flakes_size", builder.in_metallic_flakes_size, None)
            self._channel_to_sockets("metallic_flakes_strength", builder.in_metallic_flakes_strength, None)
            self._channel_to_sockets("metallic_flakes_density", builder.in_metallic_flakes_density, None)

        # Top Coat General
        if self._channel_enabled("top_coat_weight"):
            self._channel_to_sockets("top_coat_weight", builder.in_top_coat_weight, builder.in_top_coat_weight_map)
            self._channel_to_sockets("top_coat_color", builder.in_top_coat_color, builder.in_top_coat_color_map, False)
            self._channel_to_sockets("top_coat_roughness", builder.in_top_coat_roughness, builder.in_top_coat_roughness_map)

        # Volume Scattering
        if self._channel_enabled("sss_amount"):
            self._channel_to_sockets("sss_amount", builder.in_sss_weight, None)
            self._channel_to_sockets("scattering_measurement_distance", builder.in_scattering_measurement_distance, None)
            self._channel_to_sockets("sss_color", builder.in_sss_color, None, False)
            self._channel_to_sockets("sss_direction", builder.in_sss_direction, None)

        # Volume Transmission
        if self._channel_enabled("refraction_weight"):
            self._channel_to_sockets("refraction_weight", builder.in_refraction_weight, builder.in_refraction_weight_map)
            self._channel_to_sockets("refraction_index", builder.in_ior, None)
            self._channel_to_sockets("transmitted_measurement_distance", builder.in_transmitted_measurement_distance, None)
            self._channel_to_sockets("transmitted_color", builder.in_transmitted_color, builder.in_transmitted_color_map, False)
        # @formatter:on

    def _can_use_glass_shortcut(self):
        """
        If the refraction weight is 1 and the refraction index is in between 1.3 and 1.4 we can take a shortcut and use the
        fake glass shader group, instead of the full Iray Uber setup.
        """
        refraction_weight = self._channel_value("refraction_weight")
        refraction_index = self._channel_value("refraction_index")

        return refraction_weight == 1 and 1.3 <= refraction_index <= 1.4

    def _calculate_emission_luminance(self) -> float:
        base_luminance = self._channel_value("luminance")
        unit_opt = self._channel_value("luminance_units")
        efficacy = self._channel_value("luminous_efficacy")

        if unit_opt == 1:  # kcd/m^2
            multiplier = 1000
        elif unit_opt == 2:  # cd/ft^2
            multiplier = 10.7639
        elif unit_opt == 3:  # cd/cm^2
            multiplier = 10000
        elif unit_opt == 4:  # lumen → Watts using efficacy
            multiplier = 1.0 / efficacy
        else:  # cd/m^2 and Watts
            multiplier = 1

        return base_luminance * multiplier
