from .base import ShaderGroupApplier, ShaderGroupBuilder
from .dls import DualLobeSpecularShaderGroupBuilder
from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "DAZ Iray Uber (PBR Metallicity/Roughness)"
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
    in_bump_strength = "Bump Strength"
    in_bump_strength_map = "Bump Strength Map"
    in_normal_map = "Normal Map"
    in_normal_map_map = "Normal Map Map"

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
    in_sss_reflectance_tint = "SSS Reflectance Tint"

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

    # Metallic Flakes Thin Film
    in_metallic_flakes_thin_film = "Metallic Flakes Thin Film"
    in_metallic_flakes_thin_film_map = "Metallic Flakes Thin Film Map"
    in_metallic_flakes_thin_film_ior = "Metallic Flakes Thin Film IOR"
    in_metallic_flakes_thin_film_ior_map = "Metallic Flakes Thin Film IOR Map"

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
    in_transmitted_measurement_distance = "Transmitted Measurement Distance"
    in_transmitted_color = "Transmitted Color"
    in_transmitted_color_map = "Transmitted Color Map"

    out_surface = "Surface"
    out_displacement = "Displacement"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    @staticmethod
    def depends_on() -> set[str]:
        return {DualLobeSpecularShaderGroupBuilder.group_name()}

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
        sock_bump_strength = self._float_socket(self.in_bump_strength, 1, parent=panel_base_bump)
        sock_bump_strength_map = self._color_socket(self.in_bump_strength_map, parent=panel_base_bump)
        sock_normal_map = self._float_socket(self.in_normal_map, 1, parent=panel_base_bump)
        sock_normal_map_map = self._color_socket(self.in_normal_map_map, parent=panel_base_bump)

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
        sock_sss_reflectance_tint = self._color_socket(self.in_sss_reflectance_tint, parent=panel_base_diffuse_translucency)

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
        sock_displacement_strength_map = self._color_socket(self.in_displacement_strength_map, parent=panel_geometry_displacement)
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

        # Sockets: Metallic Flakes Thin Film
        sock_metallic_flakes_thin_film = self._float_socket(self.in_metallic_flakes_thin_film, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_thin_film_map = self._color_socket(self.in_metallic_flakes_thin_film_map, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_thin_film_ior = self._float_socket(self.in_metallic_flakes_thin_film_ior, 1.5, parent=panel_metallic_flakes_flakes)
        sock_metallic_flakes_thin_film_ior_map = self._color_socket(self.in_metallic_flakes_thin_film_ior_map, parent=panel_metallic_flakes_flakes)

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
        sock_scattering_measurement_distance = self._float_socket(self.in_scattering_measurement_distance, 0.1, parent=panel_volume_scattering)

        # Sockets: Volume Transmission
        sock_transmitted_measurement_distance = self._float_socket(self.in_transmitted_measurement_distance, 0.1, parent=panel_volume_transmission)
        sock_transmitted_color = self._color_socket(self.in_transmitted_color, (0.0, 0.0, 0.0, 1.0), parent=panel_volume_transmission)
        sock_transmitted_color_map = self._color_socket(self.in_transmitted_color_map, parent=panel_volume_transmission)
        # @formatter:on

        # Output Sockets:
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")
        sock_out_displacement = self._shader_socket(self.out_displacement, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-1045, 0))

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0, 0))


class IrayUberPBRMRShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def add_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().add_shader_group(channels)

        builder = IrayUberPBRMRShaderGroupBuilder

        # @formatter:off
        # Geometry Tiling
        self._set_material_mapping(channels, "horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset")

        # Base Diffuse
        self._channel_to_inputs("diffuse", builder.in_diffuse, builder.in_diffuse_map)
        self._channel_to_inputs('metallic_weight', builder.in_metallic_weight, builder.in_metallic_weight_map)
        self._channel_to_inputs('diffuse_roughness', builder.in_diffuse_roughness, builder.in_diffuse_roughness_map)

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
            self._channel_to_inputs("sss_reflectance_tint", builder.in_sss_reflectance_tint, None)

        # Base Dual Lobe Specular
        if self._channel_enabled('sock_dual_lobe_specular_weight'):
            self._channel_to_inputs('dual_lobe_specular_weight', builder.in_dual_lobe_specular_weight, builder.in_dual_lobe_specular_weight_map)
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

            # Metallic Flakes Thin Film
            self._channel_to_inputs("metallic_flakes_thin_film", builder.in_metallic_flakes_thin_film, builder.in_metallic_flakes_thin_film_map)
            self._channel_to_inputs("metallic_flakes_thin_film_ior", builder.in_metallic_flakes_thin_film_ior, builder.in_metallic_flakes_thin_film_ior_map)

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
        if self._channel_enabled("transmitted_color"):
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
