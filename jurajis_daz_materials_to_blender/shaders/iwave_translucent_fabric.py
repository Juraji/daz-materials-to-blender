from bpy.types import ShaderNodeMapping

from .base import ShaderGroupApplier
from .library import IWAVE_TRANSLUCENT_FABRIC
from ..utils.dson import DsonMaterialChannel
from ..utils.math import tuple_zip_sum


class IWaveTranslucentFabricShaderGroupApplier(ShaderGroupApplier):
    IN_DIFFUSE = "Diffuse"
    IN_DIFFUSE_MAP = "Diffuse Map"

    IN_BASE_NORMAL = "Normal"
    IN_BASE_NORMAL_MAP = "Normal Map"
    IN_BASE_BUMP = "Bump"
    IN_BASE_BUMP_MAP = "Bump Map"

    IN_FIBER_LAYER_WEIGHT = "Fiber Layer Weight"
    IN_FIBER_LAYER_WEIGHT_MAP = "Fiber Layer Weight Map"
    IN_FIBER_LAYER_METALLIC_WEIGHT = "Fiber Layer Metallic Weight"
    IN_FIBER_LAYER_METALLIC_WEIGHT_MAP = "Fiber Layer Metallic Weight Map"
    IN_FIBER_LAYER_COLOR = "Fiber Layer Color"
    IN_FIBER_LAYER_COLOR_MAP = "Fiber Layer Color Map"
    IN_FIBER_LAYER_ROUGHNESS = "Fiber Layer Roughness"
    IN_FIBER_LAYER_ROUGHNESS_MAP = "Fiber Layer Roughness Map"
    IN_FIBER_LAYER_TRANSLUCENCY_WEIGHT = "Fiber Layer Translucency Weight"
    IN_FIBER_LAYER_TRANSLUCENCY_WEIGHT_MAP = "Fiber Layer Translucency Weight Map"
    IN_FIBER_LAYER_TRANSLUCENCY_COLOR = "Fiber Layer Translucency Color"
    IN_FIBER_LAYER_TRANSLUCENCY_COLOR_MAP = "Fiber Layer Translucency Color Map"

    IN_FINE_DETAIL_NORMAL = "Fine Detail Normal"
    IN_FINE_DETAIL_NORMAL_MAP = "Fine Detail Normal Map"

    IN_CUTOUT_OPACITY = "Cutout Opacity"
    IN_CUTOUT_OPACITY_MAP = "Cutout Opacity Map"
    IN_DISPLACEMENT_STRENGTH = "Displacement Strength"
    IN_DISPLACEMENT_STRENGTH_MAP = "Displacement Strength Map"
    IN_MINIMUM_DISPLACEMENT = "Minimum Displacement"
    IN_MAXIMUM_DISPLACEMENT = "Maximum Displacement"

    IN_GLOSSY_LAYERED_WEIGHT = "Glossy Layered Weight"
    IN_GLOSSY_LAYERED_WEIGHT_MAP = "Glossy Layered Weight Map"
    IN_GLOSSY_COLOR = "Glossy Color"
    IN_GLOSSY_COLOR_MAP = "Glossy Color Map"
    IN_GLOSSY_REFLECTIVITY = "Glossy Reflectivity"
    IN_GLOSSY_REFLECTIVITY_MAP = "Glossy Reflectivity Map"
    IN_GLOSSY_ROUGHNESS = "Glossy Roughness"
    IN_GLOSSY_ROUGHNESS_MAP = "Glossy Roughness Map"

    IN_GRADIENT_LAYER_GRAZING_OPACITY = "Gradient Layer Grazing Opacity"
    IN_GRADIENT_LAYER_GRAZING_OPACITY_MAP = "Gradient Layer Grazing Opacity Map"
    IN_GRADIENT_LAYER_NORMAL_OPACITY = "Gradient Layer Normal Opacity"
    IN_GRADIENT_LAYER_NORMAL_OPACITY_MAP = "Gradient Layer Normal Opacity Map"
    IN_GRADIENT_LAYER_EXPONENT = "Gradient Layer Exponent"
    IN_GRADIENT_LAYER_EXPONENT_MAP = "Gradient Layer Exponent Map"
    IN_GRADIENT_LAYER_GRAZING_COLOR = "Gradient Layer Grazing Color"
    IN_GRADIENT_LAYER_GRAZING_COLOR_MAP = "Gradient Layer Grazing Color Map"
    IN_GRADIENT_LAYER_NORMAL_TINT = "Gradient Layer Normal Tint"
    IN_GRADIENT_LAYER_NORMAL_TINT_MAP = "Gradient Layer Normal Tint Map"
    IN_GRADIENT_LAYER_NORMAL_TINT_WEIGHT = "Gradient Layer Normal Tint Weight"
    IN_GRADIENT_LAYER_NORMAL_TINT_WEIGHT_MAP = "Gradient Layer Normal Tint Weight Map"

    IN_METALLIC_FLAKES_WEIGHT = "Metallic Flakes Weight"
    IN_METALLIC_FLAKES_WEIGHT_MAP = "Metallic Flakes Weight Map"
    IN_METALLIC_FLAKES_COLOR = "Metallic Flakes Color"
    IN_METALLIC_FLAKES_COLOR_MAP = "Metallic Flakes Color Map"
    IN_METALLIC_FLAKES_ROUGHNESS = "Metallic Flakes Roughness"
    IN_METALLIC_FLAKES_ROUGHNESS_MAP = "Metallic Flakes Roughness Map"
    IN_METALLIC_FLAKES_SIZE = "Metallic Flakes Size"
    IN_METALLIC_FLAKES_STRENGTH = "Metallic Flakes Strength"
    IN_METALLIC_FLAKES_DENSITY = "Metallic Flakes Density"

    IN_TOP_COAT_WEIGHT = "Top Coat Weight"
    IN_TOP_COAT_WEIGHT_MAP = "Top Coat Weight Map"
    IN_TOP_COAT_COLOR = "Top Coat Color"
    IN_TOP_COAT_COLOR_MAP = "Top Coat Color Map"
    IN_TOP_COAT_ROUGHNESS = "Top Coat Roughness"
    IN_TOP_COAT_ROUGHNESS_MAP = "Top Coat Roughness Map"
    IN_TOP_COAT_REFLECTIVITY = "Top Coat Reflectivity"
    IN_TOP_COAT_REFLECTIVITY_MAP = "Top Coat Reflectivity Map"
    IN_TOP_COAT_NORMAL = "Top Coat Normal"
    IN_TOP_COAT_NORMAL_MAP = "Top Coat Normal Map"
    IN_TOP_COAT_BUMP = "Top Coat Bump"
    IN_TOP_COAT_BUMP_MAP = "Top Coat Bump Map"
    IN_TOP_COAT_ANISOTROPY = "Top Coat Anisotropy"
    IN_TOP_COAT_ANISOTROPY_MAP = "Top Coat Anisotropy Map"
    IN_TOP_COAT_ROTATIONS = "Top Coat Rotations"
    IN_TOP_COAT_ROTATIONS_MAP = "Top Coat Rotations Map"

    IN_THIN_FILM_WEIGHT = "Thin Film Weight"
    IN_THIN_FILM_ROTATIONS = "Thin Film Iredescent Rotations"
    IN_THIN_FILM_THICKNESS = "Thin Film Thickness"
    IN_THIN_FILM_THICKNESS_MAP = "Thin Film Thickness Map"
    IN_THIN_FILM_IOR = "Thin Film Ior"
    IN_THIN_FILM_IOR_MAP = "Thin Film Ior Map"

    @staticmethod
    def group_name() -> str:
        return IWAVE_TRANSLUCENT_FABRIC

    @staticmethod
    def material_type_id() -> str:
        return "translucent_fabric"

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        # # @formatter:off
        # Base Diffuse
        self._channel_to_sockets("diffuse", self.IN_DIFFUSE, self.IN_DIFFUSE_MAP, False)

        # Geometry
        geo_mapping_props = ["horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset"]
        if self._channel_enabled(*geo_mapping_props):
            self._set_material_mapping(*geo_mapping_props)

        self._channel_to_sockets("displacement_strength", self.IN_DISPLACEMENT_STRENGTH, self.IN_DISPLACEMENT_STRENGTH_MAP)
        self._channel_to_sockets("minimum_displacement", self.IN_MINIMUM_DISPLACEMENT, None)
        self._channel_to_sockets("maximum_displacement", self.IN_MAXIMUM_DISPLACEMENT, None)

        node_cutout_tex = self._channel_to_sockets("cutout_opacity", self.IN_CUTOUT_OPACITY, self.IN_CUTOUT_OPACITY_MAP)
        cutout_mapping_props = ["cutout_opacity_horizontal_tiles", "cutout_opacity_horizontal_offset", "cutout_opacity_vertical_tiles", "cutout_opacity_vertical_offset"]
        if self._channel_enabled(*cutout_mapping_props) and node_cutout_tex:
            cutout_mapping_node_loc = tuple_zip_sum((0, self.mapping_node_location_offset * 2), self._mapping.location.to_tuple())
            cutout_mapping_node = self._add_node(ShaderNodeMapping, "Cutout Opacity Mapping", cutout_mapping_node_loc, props={"vector_type": "POINT", "hide": True})
            self._link_socket(self._uv_map, cutout_mapping_node, 0, 0)
            self._link_socket(cutout_mapping_node, node_cutout_tex, 0, 0)
            self._set_material_mapping(*cutout_mapping_props, mapping_node=cutout_mapping_node)

        # Bump
        self._channel_to_sockets("normal_map", self.IN_BASE_NORMAL, self.IN_BASE_NORMAL_MAP)
        self._channel_to_sockets("bump_strength", self.IN_BASE_BUMP, self.IN_BASE_BUMP_MAP)

        # Fiber Layer
        if self._channel_enabled("fiber_layer_weight"):
            self._channel_to_sockets("metallic_weight", self.IN_FIBER_LAYER_METALLIC_WEIGHT, self.IN_FIBER_LAYER_METALLIC_WEIGHT_MAP)
            self._channel_to_sockets("diffuse_overlay_color", self.IN_FIBER_LAYER_COLOR, self.IN_FIBER_LAYER_COLOR_MAP)
            self._channel_to_sockets("diffuse_roughness", self.IN_FIBER_LAYER_ROUGHNESS, self.IN_FIBER_LAYER_ROUGHNESS_MAP)
            self._channel_to_sockets("translucency_weight", self.IN_FIBER_LAYER_TRANSLUCENCY_WEIGHT, self.IN_FIBER_LAYER_TRANSLUCENCY_WEIGHT_MAP)
            self._channel_to_sockets("translucency_color", self.IN_FIBER_LAYER_TRANSLUCENCY_COLOR, self.IN_FIBER_LAYER_TRANSLUCENCY_COLOR_MAP)

        # Fine Detail
        node_fd_normal_tex = self._channel_to_sockets("fine_detail_normal_map", self.IN_FINE_DETAIL_NORMAL, self.IN_FINE_DETAIL_NORMAL_MAP, force_new_image_node=True)

        fd_mapping_props = ["fine_detail_horizontal_tiles", "fine_detail_horizontal_offset", "fine_detail_vertical_tiles", "fine_detail_vertical_offset"]
        if self._channel_enabled(*fd_mapping_props) and node_fd_normal_tex:
            fd_mapping_node_loc = tuple_zip_sum((0, self.mapping_node_location_offset), self._mapping.location.to_tuple())
            fd_mapping_node = self._add_node(ShaderNodeMapping, "Fine Detail Mapping", fd_mapping_node_loc, props={"vector_type": "POINT", "hide": True})
            self._link_socket(self._uv_map, fd_mapping_node, 0, 0)
            self._set_material_mapping(*fd_mapping_props, mapping_node=fd_mapping_node)

            if node_fd_normal_tex:
                self._link_socket(fd_mapping_node, node_fd_normal_tex, 0, 0)

        # Glossy
        if self._channel_enabled("glossy_layered_weight"):
            self._channel_to_sockets("glossy_layered_weight", self.IN_GLOSSY_LAYERED_WEIGHT, self.IN_GLOSSY_LAYERED_WEIGHT_MAP)
            self._channel_to_sockets("glossy_color", self.IN_GLOSSY_COLOR, self.IN_GLOSSY_COLOR_MAP)
            self._channel_to_sockets("glossy_reflectivity", self.IN_GLOSSY_REFLECTIVITY, self.IN_GLOSSY_REFLECTIVITY_MAP)
            self._channel_to_sockets("glossy_roughness", self.IN_GLOSSY_ROUGHNESS, self.IN_GLOSSY_ROUGHNESS_MAP)

        # Gradient Layer
        self._channel_to_sockets("gradient_layer_normal_reflectivity", self.IN_GRADIENT_LAYER_NORMAL_OPACITY, self.IN_GRADIENT_LAYER_NORMAL_OPACITY_MAP)
        self._channel_to_sockets("gradient_layer_grazing_reflectivity", self.IN_GRADIENT_LAYER_GRAZING_OPACITY, self.IN_GRADIENT_LAYER_GRAZING_OPACITY_MAP)
        self._channel_to_sockets("gradient_layer_exponent", self.IN_GRADIENT_LAYER_EXPONENT, self.IN_GRADIENT_LAYER_EXPONENT_MAP)
        self._channel_to_sockets("gradient_layer_grazing_color", self.IN_GRADIENT_LAYER_GRAZING_COLOR, self.IN_GRADIENT_LAYER_GRAZING_COLOR_MAP)
        self._channel_to_sockets("gradient_layer_normal_tint", self.IN_GRADIENT_LAYER_NORMAL_TINT, self.IN_GRADIENT_LAYER_NORMAL_TINT_MAP)
        self._channel_to_sockets("gradient_layer_normal_tint_weight", self.IN_GRADIENT_LAYER_NORMAL_TINT_WEIGHT, self.IN_GRADIENT_LAYER_NORMAL_TINT_WEIGHT_MAP)

        # Metallic Flakes
        if self._channel_enabled("metallic_flakes_weight"):
            self._channel_to_sockets("metallic_flakes_weight", self.IN_METALLIC_FLAKES_WEIGHT, self.IN_METALLIC_FLAKES_WEIGHT_MAP)
            self._channel_to_sockets("metallic_flakes_color", self.IN_METALLIC_FLAKES_COLOR, self.IN_METALLIC_FLAKES_COLOR_MAP)
            self._channel_to_sockets("metallic_flakes_roughness", self.IN_METALLIC_FLAKES_ROUGHNESS, self.IN_METALLIC_FLAKES_ROUGHNESS_MAP)
            self._channel_to_sockets("metallic_flakes_size", self.IN_METALLIC_FLAKES_SIZE, None)
            self._channel_to_sockets("metallic_flakes_strength", self.IN_METALLIC_FLAKES_STRENGTH, None)
            self._channel_to_sockets("metallic_flakes_density", self.IN_METALLIC_FLAKES_DENSITY, None)

            # Top Coat General
        if self._channel_enabled("top_coat_weight"):
            self._channel_to_sockets("top_coat_weight", self.IN_TOP_COAT_WEIGHT, self.IN_TOP_COAT_WEIGHT_MAP)
            self._channel_to_sockets("top_coat_color", self.IN_TOP_COAT_COLOR, self.IN_TOP_COAT_COLOR_MAP)
            self._channel_to_sockets("top_coat_roughness", self.IN_TOP_COAT_ROUGHNESS, self.IN_TOP_COAT_ROUGHNESS_MAP)
            self._channel_to_sockets("top_coat_reflectivity", self.IN_TOP_COAT_REFLECTIVITY, self.IN_TOP_COAT_REFLECTIVITY_MAP)
            self._channel_to_sockets("top_coat_anisotropy", self.IN_TOP_COAT_ANISOTROPY, self.IN_TOP_COAT_ANISOTROPY_MAP)
            self._channel_to_sockets("top_coat_rotations", self.IN_TOP_COAT_ROTATIONS, self.IN_TOP_COAT_ANISOTROPY_MAP)

            self._channel_to_sockets("top_coat_normal", self.IN_TOP_COAT_NORMAL, self.IN_TOP_COAT_NORMAL_MAP)
            self._channel_to_sockets("top_coat_bump", self.IN_TOP_COAT_BUMP, self.IN_TOP_COAT_BUMP_MAP)

        # Thin Film
        if self._channel_enabled("thin_film_thickness"):
            self._set_socket(self._shader_group, self.IN_THIN_FILM_WEIGHT, 0.5)
            self._channel_to_sockets("thin_film_thickness", self.IN_THIN_FILM_THICKNESS, self.IN_THIN_FILM_THICKNESS_MAP)
            self._channel_to_sockets("thin_film_ior", self.IN_THIN_FILM_IOR, self.IN_THIN_FILM_IOR_MAP)
        # @formatter:on
