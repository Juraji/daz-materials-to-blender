from unittest import case

from .base import ShaderGroupApplier
from .iray_uber_as_fake_glass import IrayUberAsFakeGlassShaderGroupApplier
from .library import IRAY_UBER
from ..utils.dson import DsonChannel



class IrayUberShaderGroupApplier(ShaderGroupApplier):
    # Base Diffuse
    IN_DIFFUSE = "Diffuse"
    IN_DIFFUSE_MAP = "Diffuse Map"
    IN_METALLIC_WEIGHT = "Metallic Weight"
    IN_METALLIC_WEIGHT_MAP = "Metallic Weight Map"
    IN_DIFFUSE_ROUGHNESS = "Diffuse Roughness"
    IN_DIFFUSE_ROUGHNESS_MAP = "Diffuse Roughness Map"

    # Base Bump
    IN_NORMAL = "Normal"
    IN_NORMAL_MAP = "Normal Map"
    IN_BUMP_STRENGTH = "Bump Strength"
    IN_BUMP_STRENGTH_MAP = "Bump Strength Map"

    # Base Diffuse Overlay
    IN_DIFFUSE_OVERLAY_WEIGHT = "Diffuse Overlay Weight"
    IN_DIFFUSE_OVERLAY_WEIGHT_MAP = "Diffuse Overlay Weight Map"
    IN_DIFFUSE_OVERLAY_WEIGHT_SQUARED = "Diffuse Overlay Weight Squared"
    IN_DIFFUSE_OVERLAY_COLOR = "Diffuse Overlay Color"
    IN_DIFFUSE_OVERLAY_COLOR_MAP = "Diffuse Overlay Color Map"
    IN_DIFFUSE_OVERLAY_ROUGHNESS = "Diffuse Overlay Roughness"
    IN_DIFFUSE_OVERLAY_ROUGHNESS_MAP = "Diffuse Overlay Roughness Map"

    # Base Diffuse Translucency
    IN_TRANSLUCENCY_WEIGHT = "Translucency Weight"
    IN_TRANSLUCENCY_WEIGHT_MAP = "Translucency Weight Map"
    IN_TRANSLUCENCY_COLOR = "Translucency Color"
    IN_TRANSLUCENCY_COLOR_MAP = "Translucency Color Map"
    IN_INVERT_TRANSMISSION_NORMAL = "Invert Transmission Normal"

    # Base Dual Lobe Specular
    IN_DUAL_LOBE_SPECULAR_WEIGHT = "Dual Lobe Specular Weight"
    IN_DUAL_LOBE_SPECULAR_WEIGHT_MAP = "Dual Lobe Specular Weight Map"
    IN_DUAL_LOBE_SPECULAR_REFLECTIVITY = "Dual Lobe Specular Reflectivity"
    IN_DUAL_LOBE_SPECULAR_REFLECTIVITY_MAP = "Dual Lobe Specular Reflectivity Map"
    IN_SPECULAR_LOBE_1_ROUGHNESS = "Specular Lobe 1 Roughness"
    IN_SPECULAR_LOBE_1_ROUGHNESS_MAP = "Specular Lobe 1 Roughness Map"
    IN_SPECULAR_LOBE_2_ROUGHNESS = "Specular Lobe 2 Roughness"
    IN_SPECULAR_LOBE_2_ROUGHNESS_MAP = "Specular Lobe 2 Roughness Map"
    IN_DUAL_LOBE_SPECULAR_RATIO = "Dual Lobe Specular Ratio"
    IN_DUAL_LOBE_SPECULAR_RATIO_MAP = "Dual Lobe Specular Ratio Map"

    # Glossy
    IN_GLOSSY_WEIGHT = "Glossy Weight"
    IN_GLOSSY_WEIGHT_MAP = "Glossy Weight Map"
    IN_GLOSSY_COLOR = "Glossy Color"
    IN_GLOSSY_COLOR_MAP = "Glossy Color Map"
    IN_GLOSSY_REFLECTIVITY = "Glossy Reflectivity"
    IN_GLOSSY_REFLECTIVITY_MAP = "Glossy Reflectivity Map"
    IN_GLOSSY_ROUGHNESS = "Glossy Roughness"
    IN_GLOSSY_ROUGHNESS_MAP = "Glossy Roughness Map"
    IN_GLOSSY_ANISOTROPY = "Glossy Anisotropy"
    IN_GLOSSY_ANISOTROPY_MAP = "Glossy Anisotropy Map"
    IN_GLOSSY_ANISOTROPY_ROTATIONS = "Glossy Anisotropy Rotations"
    IN_GLOSSY_ANISOTROPY_ROTATIONS_MAP = "Glossy Anisotropy Rotations Map"

    # Emission
    IN_EMISSION_COLOR = "Emission Color"
    IN_EMISSION_COLOR_MAP = "Emission Color Map"
    IN_EMISSION_TEMPERATURE = "Emission Temperature"
    IN_LUMINANCE = "Luminance"
    IN_LUMINANCE_MAP = "Luminance Map"

    # Geometry Cutout
    IN_CUTOUT_OPACITY = "Cutout Opacity"
    IN_CUTOUT_OPACITY_MAP = "Cutout Opacity Map"

    # Geometry Displacement
    IN_DISPLACEMENT_STRENGTH = "Displacement Strength"
    IN_DISPLACEMENT_STRENGTH_MAP = "Displacement Strength Map"
    IN_MINIMUM_DISPLACEMENT = "Minimum Displacement"
    IN_MAXIMUM_DISPLACEMENT = "Maximum Displacement"

    # Metallic Flakes Flakes
    IN_METALLIC_FLAKES_WEIGHT = "Metallic Flakes Weight"
    IN_METALLIC_FLAKES_WEIGHT_MAP = "Metallic Flakes Weight Map"
    IN_METALLIC_FLAKES_COLOR = "Metallic Flakes Color"
    IN_METALLIC_FLAKES_COLOR_MAP = "Metallic Flakes Color Map"
    IN_METALLIC_FLAKES_ROUGHNESS = "Metallic Flakes Roughness"
    IN_METALLIC_FLAKES_ROUGHNESS_MAP = "Metallic Flakes Roughness Map"
    IN_METALLIC_FLAKES_SIZE = "Metallic Flakes Size"
    IN_METALLIC_FLAKES_STRENGTH = "Metallic Flakes Strength"
    IN_METALLIC_FLAKES_DENSITY = "Metallic Flakes Density"

    # Top Coat
    IN_TOP_COAT_WEIGHT = "Top Coat Weight"
    IN_TOP_COAT_WEIGHT_MAP = "Top Coat Weight Map"
    IN_TOP_COAT_COLOR = "Top Coat Color"
    IN_TOP_COAT_COLOR_MAP = "Top Coat Color Map"
    IN_TOP_COAT_ROUGHNESS = "Top Coat Roughness"
    IN_TOP_COAT_ROUGHNESS_MAP = "Top Coat Roughness Map"

    # Base Thin Film
    IN_THIN_FILM_WEIGHT = "Thin Film Weight"
    IN_THIN_FILM_ROTATIONS = "Thin Film Iridescent Rotations"
    IN_THIN_FILM_THICKNESS = "Thin Film Thickness"
    IN_THIN_FILM_THICKNESS_MAP = "Thin Film Thickness Map"
    IN_THIN_FILM_IOR = "Thin Film IOR"
    IN_THIN_FILM_IOR_MAP = "Thin Film IOR Map"

    # Volume Scattering
    IN_SSS_WEIGHT = "SSS Weight"
    IN_SSS_COLOR = "SSS Color"
    IN_SCATTERING_MEASUREMENT_DISTANCE = "Scattering Measurement Distance"
    IN_SSS_DIRECTION = "SSS Direction"

    # Volume Transmission
    IN_REFRACTION_WEIGHT = "Refraction Weight"
    IN_REFRACTION_WEIGHT_MAP = "Refraction Weight Map"
    IN_IOR = "IOR"
    IN_TRANSMITTED_MEASUREMENT_DISTANCE = "Transmitted Measurement Distance"
    IN_TRANSMITTED_COLOR = "Transmitted Color"
    IN_TRANSMITTED_COLOR_MAP = "Transmitted Color Map"

    @staticmethod
    def group_name() -> str:
        return IRAY_UBER

    @staticmethod
    def material_type_id() -> str:
        return "iray_uber"

    def apply_shader_group(self, channels: dict[str, DsonChannel]):
        self._channels = channels

        if self._properties.iray_uber_replace_glass:
            refraction_w_ch = self._channels.get("refraction_weight")
            if refraction_w_ch is not None and refraction_w_ch.value == 1.0 and not refraction_w_ch.has_image():
                replacement = IrayUberAsFakeGlassShaderGroupApplier(self._properties, self._b_object, self._node_tree)
                replacement.apply_shader_group(channels)
                return

        super().apply_shader_group(channels)

        # @formatter:off
        # Geometry Tiling
        self._set_material_mapping("horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset")

        # Base Diffuse
        self._channel_to_sockets("diffuse", self.IN_DIFFUSE, self.IN_DIFFUSE_MAP, False)
        self._channel_to_sockets('metallic_weight', self.IN_METALLIC_WEIGHT, self.IN_METALLIC_WEIGHT_MAP)

        if self._channel_enabled('diffuse_roughness'):
            # For some reason the diffuse roughness is set to 0 by default.
            # This makes the shader very glossy in Blender, hence we only set it if it's non-zero.
            self._channel_to_sockets('diffuse_roughness', self.IN_DIFFUSE_ROUGHNESS, self.IN_DIFFUSE_ROUGHNESS_MAP)

        # Base Bump
        self._channel_to_sockets("bump_strength", self.IN_BUMP_STRENGTH, self.IN_BUMP_STRENGTH_MAP)
        self._channel_to_sockets("normal_map", self.IN_NORMAL, self.IN_NORMAL_MAP)

        if self._channel_enabled("bump_strength"):
            self._set_socket(self._shader_group, self.IN_BUMP_STRENGTH, self._properties.bump_strength_multiplier, "MULTIPLY")

        # Base Diffuse Overlay
        if self._channel_enabled("diffuse_overlay_weight"):
            self._channel_to_sockets("diffuse_overlay_weight", self.IN_DIFFUSE_OVERLAY_WEIGHT, self.IN_DIFFUSE_OVERLAY_WEIGHT_MAP)
            self._channel_to_sockets("diffuse_overlay_weight_squared", self.IN_DIFFUSE_OVERLAY_WEIGHT_SQUARED, None)
            self._channel_to_sockets("diffuse_overlay_color", self.IN_DIFFUSE_OVERLAY_COLOR, self.IN_DIFFUSE_OVERLAY_COLOR_MAP, False)
            self._channel_to_sockets("diffuse_overlay_roughness", self.IN_DIFFUSE_OVERLAY_ROUGHNESS, self.IN_DIFFUSE_OVERLAY_ROUGHNESS_MAP)

        # Base Diffuse Translucency
        if self._channel_enabled('translucency_weight'):
            self._channel_to_sockets("translucency_weight", self.IN_TRANSLUCENCY_WEIGHT, self.IN_TRANSLUCENCY_WEIGHT_MAP)
            self._channel_to_sockets("translucency_color", self.IN_TRANSLUCENCY_COLOR, self.IN_TRANSLUCENCY_COLOR_MAP, False)
            self._channel_to_sockets("invert_transmission_normal", self.IN_INVERT_TRANSMISSION_NORMAL, None)

        # Base Dual Lobe Specular
        if self._channel_enabled('dual_lobe_specular_weight'):
            self._channel_to_sockets('dual_lobe_specular_weight', self.IN_DUAL_LOBE_SPECULAR_WEIGHT, self.IN_DUAL_LOBE_SPECULAR_WEIGHT_MAP)
            if self._properties.dls_weight_multiplier != 1.0:
                self._set_socket(self._shader_group, self.IN_DUAL_LOBE_SPECULAR_WEIGHT, self._properties.dls_weight_multiplier, "MULTIPLY")

            self._channel_to_sockets('dual_lobe_specular_reflectivity', self.IN_DUAL_LOBE_SPECULAR_REFLECTIVITY, self.IN_DUAL_LOBE_SPECULAR_REFLECTIVITY_MAP)
            self._channel_to_sockets('specular_lobe_1_roughness', self.IN_SPECULAR_LOBE_1_ROUGHNESS, self.IN_SPECULAR_LOBE_1_ROUGHNESS_MAP)
            self._channel_to_sockets('specular_lobe_2_roughness', self.IN_SPECULAR_LOBE_2_ROUGHNESS, self.IN_SPECULAR_LOBE_2_ROUGHNESS_MAP)
            self._channel_to_sockets('dual_lobe_specular_ratio', self.IN_DUAL_LOBE_SPECULAR_RATIO, self.IN_DUAL_LOBE_SPECULAR_RATIO_MAP)

        # Glossy Layer
        self._channel_to_sockets("glossy_weight", self.IN_GLOSSY_WEIGHT, self.IN_GLOSSY_WEIGHT_MAP)
        self._channel_to_sockets("glossy_reflectivity", self.IN_GLOSSY_REFLECTIVITY, self.IN_GLOSSY_REFLECTIVITY_MAP)
        self._channel_to_sockets("glossy_anisotropy", self.IN_GLOSSY_ANISOTROPY, self.IN_GLOSSY_ANISOTROPY_MAP)
        self._channel_to_sockets("glossy_anisotropy_rotations", self.IN_GLOSSY_ANISOTROPY_ROTATIONS, self.IN_GLOSSY_ANISOTROPY_ROTATIONS)

        # Remap Glossy Color to Roughness
        if (self._properties.iray_uber_remap_glossy_color_to_roughness
                and self._channel_enabled("glossy_color")
                and not self._channel_enabled("glossy_roughness")):
            self._channel_to_sockets("glossy_color", self.IN_GLOSSY_ROUGHNESS, self.IN_GLOSSY_ROUGHNESS_MAP)
        else:
            self._channel_to_sockets("glossy_color", self.IN_GLOSSY_COLOR, self.IN_GLOSSY_COLOR_MAP)
            self._channel_to_sockets("glossy_roughness", self.IN_GLOSSY_ROUGHNESS, self.IN_GLOSSY_ROUGHNESS_MAP)

        if not self._channel_enabled("glossy_weight") and self._channel_enabled("glossy_color", "glossy_reflectivity", "glossy_roughness"):
            # Glossy Weight is only set in weighted mode.
            # So if it's set we leave it alone, else we check whether any of its props are set.
            # When that is true we set the weight to 1.
            self._set_socket(self._shader_group, self.IN_GLOSSY_WEIGHT, 1.0)

        # Base Thin Film
        if self._channel_enabled("thin_film_thickness"):
            self._set_socket(self._shader_group, self.IN_THIN_FILM_WEIGHT, 0.5)
            self._channel_to_sockets("thin_film_thickness", self.IN_THIN_FILM_THICKNESS, self.IN_THIN_FILM_THICKNESS_MAP)
            self._channel_to_sockets("thin_film_ior", self.IN_THIN_FILM_IOR, self.IN_THIN_FILM_IOR_MAP)

        # Emission
        if self._channel_enabled("emission_color"):
            self._channel_to_sockets("emission_color", self.IN_EMISSION_COLOR, self.IN_EMISSION_COLOR_MAP)
            self._channel_to_sockets("emission_temperature", self.IN_EMISSION_TEMPERATURE, None)

            # Emission clamping
            emission_color = self._channel_value("emission_color")
            emission_max_rgb = max(emission_color[0], emission_color[1], emission_color[2])
            if 0 <= emission_max_rgb <= self._properties.iray_uber_clamp_emission:
                self._set_socket(self._shader_group, self.IN_EMISSION_COLOR, (0.0, 0.0, 0.0, 1.0))

            if self._channel_enabled('luminance'):
                self._channel_to_sockets('luminance', self.IN_LUMINANCE, self.IN_LUMINANCE_MAP)

                # Override luminance using units and efficacy
                b_luminance = self._calculate_emission_luminance()
                self._set_socket(self._shader_group, self.IN_LUMINANCE, b_luminance)

        # Geometry Cutout
        self._channel_to_sockets("cutout_opacity", self.IN_CUTOUT_OPACITY, self.IN_CUTOUT_OPACITY_MAP)

        # Geometry Displacement
        if self._channel_enabled("displacement_strength"):
            self._channel_to_sockets("displacement_strength", self.IN_DISPLACEMENT_STRENGTH, self.IN_DISPLACEMENT_STRENGTH_MAP)
            self._channel_to_sockets("minimum_displacement", self.IN_MINIMUM_DISPLACEMENT, None)
            self._channel_to_sockets("maximum_displacement", self.IN_MAXIMUM_DISPLACEMENT, None)

        # Metallic Flakes Flakes
        if self._channel_enabled("metallic_flakes_weight"):
            self._channel_to_sockets("metallic_flakes_weight", self.IN_METALLIC_FLAKES_WEIGHT, self.IN_METALLIC_FLAKES_WEIGHT_MAP)
            self._channel_to_sockets("metallic_flakes_color", self.IN_METALLIC_FLAKES_COLOR, self.IN_METALLIC_FLAKES_COLOR_MAP, False)
            self._channel_to_sockets("metallic_flakes_roughness", self.IN_METALLIC_FLAKES_ROUGHNESS, self.IN_METALLIC_FLAKES_ROUGHNESS_MAP)
            self._channel_to_sockets("metallic_flakes_size", self.IN_METALLIC_FLAKES_SIZE, None)
            self._channel_to_sockets("metallic_flakes_strength", self.IN_METALLIC_FLAKES_STRENGTH, None)
            self._channel_to_sockets("metallic_flakes_density", self.IN_METALLIC_FLAKES_DENSITY, None)

        # Top Coat General
        if self._channel_enabled("top_coat_weight"):
            self._channel_to_sockets("top_coat_weight", self.IN_TOP_COAT_WEIGHT, self.IN_TOP_COAT_WEIGHT_MAP)
            self._channel_to_sockets("top_coat_color", self.IN_TOP_COAT_COLOR, self.IN_TOP_COAT_COLOR_MAP, False)
            self._channel_to_sockets("top_coat_roughness", self.IN_TOP_COAT_ROUGHNESS, self.IN_TOP_COAT_ROUGHNESS_MAP)

        # Volume Scattering
        if self._channel_enabled("sss_amount"):
            self._channel_to_sockets("sss_amount", self.IN_SSS_WEIGHT, None)
            self._channel_to_sockets("scattering_measurement_distance", self.IN_SCATTERING_MEASUREMENT_DISTANCE, None)
            self._channel_to_sockets("sss_color", self.IN_SSS_COLOR, None, False)
            self._channel_to_sockets("sss_direction", self.IN_SSS_DIRECTION, None)

        # Volume Transmission
        if self._channel_enabled("refraction_weight"):
            self._channel_to_sockets("refraction_weight", self.IN_REFRACTION_WEIGHT, self.IN_REFRACTION_WEIGHT_MAP)
            self._channel_to_sockets("refraction_index", self.IN_IOR, None)
            self._channel_to_sockets("transmitted_measurement_distance", self.IN_TRANSMITTED_MEASUREMENT_DISTANCE, None)
            self._channel_to_sockets("transmitted_color", self.IN_TRANSMITTED_COLOR, self.IN_TRANSMITTED_COLOR_MAP, False)
        # @formatter:on

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
