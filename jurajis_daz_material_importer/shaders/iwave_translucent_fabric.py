from typing import Type

from bpy.types import ShaderNodeMapping, BlendDataNodeTrees, ShaderNodeBsdfDiffuse, ShaderNodeBsdfMetallic, \
    ShaderNodeBsdfTranslucent, ShaderNodeBsdfTransparent, ShaderNodeLayerWeight

from .support import AsymmetricalDisplacementShaderGroupBuilder, MetallicFlakesShaderGroupBuilder, ShaderGroupApplier, \
    ShaderGroupBuilder, AdvancedTopCoatShaderGroupBuilder, RerouteGroup
from ..properties import MaterialImportProperties
from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "iWave Translucent Fabric"
__MATERIAL_TYPE_ID__ = "translucent_fabric"

from ..utils.math import tuple_zip_sum


class IWaveTranslucentFabricShaderGroupBuilder(ShaderGroupBuilder):
    in_diffuse = "Diffuse"
    in_diffuse_map = "Diffuse Map"

    in_base_normal = "Normal"
    in_base_normal_map = "Normal Map"
    in_base_bump = "Bump"
    in_base_bump_map = "Bump Map"

    in_fiber_layer_weight = "Fiber Layer Weight"
    in_fiber_layer_weight_map = "Fiber Layer Weight Map"
    in_fiber_layer_metallic_weight = "Fiber Layer Metallic Weight"
    in_fiber_layer_metallic_weight_map = "Fiber Layer Metallic Weight Map"
    in_fiber_layer_color = "Fiber Layer Color"
    in_fiber_layer_color_map = "Fiber Layer Color Map"
    in_fiber_layer_roughness = "Fiber Layer Roughness"
    in_fiber_layer_roughness_map = "Fiber Layer Roughness Map"
    in_fiber_layer_translucency_weight = "Fiber Layer Translucency Weight"
    in_fiber_layer_translucency_weight_map = "Fiber Layer Translucency Weight Map"
    in_fiber_layer_translucency_color = "Fiber Layer Translucency Color"
    in_fiber_layer_translucency_color_map = "Fiber Layer Translucency Color Map"

    in_fine_detail_normal = "Fine Detail Normal"
    in_fine_detail_normal_map = "Fine Detail Normal Map"

    in_cutout_opacity = "Cutout Opacity"
    in_cutout_opacity_map = "Cutout Opacity Map"
    in_displacement_strength = "Displacement Strength"
    in_displacement_strength_map = "Displacement Strength Map"
    in_minimum_displacement = "Minimum Displacement"
    in_maximum_displacement = "Maximum Displacement"

    in_glossy_layered_weight = "Glossy Layered Weight"
    in_glossy_layered_weight_map = "Glossy Layered Weight Map"
    in_glossy_color = "Glossy Color"
    in_glossy_color_map = "Glossy Color Map"
    in_glossy_reflectivity = "Glossy Reflectivity"
    in_glossy_reflectivity_map = "Glossy Reflectivity Map"
    in_glossy_roughness = "Glossy Roughness"
    in_glossy_roughness_map = "Glossy Roughness Map"

    in_gradient_layer_grazing_opacity = "Gradient Layer Grazing Opacity"
    in_gradient_layer_grazing_opacity_map = "Gradient Layer Grazing Opacity Map"
    in_gradient_layer_normal_opacity = "Gradient Layer Normal Opacity"
    in_gradient_layer_normal_opacity_map = "Gradient Layer Normal Opacity Map"
    in_gradient_layer_exponent = "Gradient Layer Exponent"
    in_gradient_layer_exponent_map = "Gradient Layer Exponent Map"
    in_gradient_layer_grazing_color = "Gradient Layer Grazing Color"
    in_gradient_layer_grazing_color_map = "Gradient Layer Grazing Color Map"
    in_gradient_layer_normal_tint = "Gradient Layer Normal Tint"
    in_gradient_layer_normal_tint_map = "Gradient Layer Normal Tint Map"
    in_gradient_layer_normal_tint_weight = "Gradient Layer Normal Tint Weight"
    in_gradient_layer_normal_tint_weight_map = "Gradient Layer Normal Tint Weight Map"

    in_metallic_flakes_weight = "Metallic Flakes Weight"
    in_metallic_flakes_weight_map = "Metallic Flakes Weight Map"
    in_metallic_flakes_color = "Metallic Flakes Color"
    in_metallic_flakes_color_map = "Metallic Flakes Color Map"
    in_metallic_flakes_roughness = "Metallic Flakes Roughness"
    in_metallic_flakes_roughness_map = "Metallic Flakes Roughness Map"
    in_metallic_flakes_size = "Metallic Flakes Size"
    in_metallic_flakes_strength = "Metallic Flakes Strength"
    in_metallic_flakes_density = "Metallic Flakes Density"

    in_top_coat_weight = "Top Coat Weight"
    in_top_coat_weight_map = "Top Coat Weight Map"
    in_top_coat_color = "Top Coat Color"
    in_top_coat_color_map = "Top Coat Color Map"
    in_top_coat_roughness = "Top Coat Roughness"
    in_top_coat_roughness_map = "Top Coat Roughness Map"
    in_top_coat_reflectivity = "Top Coat Reflectivity"
    in_top_coat_reflectivity_map = "Top Coat Reflectivity Map"
    in_top_coat_normal = "Top Coat Normal"
    in_top_coat_normal_map = "Top Coat Normal Map"
    in_top_coat_bump = "Top Coat Bump"
    in_top_coat_bump_map = "Top Coat Bump Map"
    in_top_coat_anisotropy = "Top Coat Anisotropy"
    in_top_coat_anisotropy_map = "Top Coat Anisotropy Map"
    in_top_coat_rotations = "Top Coat Rotations"
    in_top_coat_rotations_map = "Top Coat Rotations Map"

    in_thin_film_weight = "Thin Film Weight"
    in_thin_film_rotations = "Thin Film Iredescent Rotations"
    in_thin_film_thickness = "Thin Film Thickness"
    in_thin_film_thickness_map = "Thin Film Thickness Map"
    in_thin_film_ior = "Thin Film Ior"
    in_thin_film_ior_map = "Thin Film Ior Map"

    out_surface = "Surface"
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
            MetallicFlakesShaderGroupBuilder,
            AdvancedTopCoatShaderGroupBuilder
        }

    def __init__(self, properties: MaterialImportProperties, node_trees: BlendDataNodeTrees):
        super().__init__(properties, node_trees)

    # noinspection PyUnusedLocal
    def setup_group(self):
        super().setup_group()

        # @formatter:off
        panel_base_diffuse = self._add_panel("Base Diffuse")
        panel_bump = self._add_panel("Normal and Bump")
        panel_fiber_layer = self._add_panel("Fiber Layer")
        panel_fine_detail = self._add_panel("Fine Detail")
        panel_geometry = self._add_panel("Geometry")
        panel_glossy = self._add_panel("Glossy")
        panel_gradient_layer = self._add_panel("Gradient Layer")
        panel_metallic_flakes_flakes = self._add_panel("Metallic Flakes Flakes")
        panel_top_coat_general = self._add_panel("Top Coat")
        panel_thin_film = self._add_panel("Thin Film")

        # Sockets: Base Diffuse
        sock_diffuse = self._color_socket(self.in_diffuse, parent=panel_base_diffuse)
        sock_diffuse_map = self._color_socket(self.in_diffuse_map, parent=panel_base_diffuse)

        # Sockets: Bump
        sock_normal = self._float_socket(self.in_base_normal, 1, parent=panel_bump)
        sock_normal_map = self._color_socket(self.in_base_normal_map, (0.5, 0.5, 1.0, 1.0), parent=panel_bump)
        sock_bump = self._float_socket(self.in_base_bump, 1, parent=panel_bump)
        sock_bump_map = self._color_socket(self.in_base_bump_map, parent=panel_bump)

        # Sockets: Fiber Layer
        sock_fiber_weight = self._float_socket(self.in_fiber_layer_weight, parent=panel_fiber_layer)
        sock_fiber_weight_map = self._color_socket(self.in_fiber_layer_weight_map, parent=panel_fiber_layer)
        sock_fiber_metallic_weight = self._float_socket(self.in_fiber_layer_metallic_weight, parent=panel_fiber_layer)
        sock_fiber_metallic_weight_map = self._color_socket(self.in_fiber_layer_metallic_weight_map, parent=panel_fiber_layer)
        sock_fiber_color = self._color_socket(self.in_fiber_layer_color, parent=panel_fiber_layer)
        sock_fiber_color_map = self._color_socket(self.in_fiber_layer_color_map, parent=panel_fiber_layer)
        sock_fiber_roughness = self._float_socket(self.in_fiber_layer_roughness, parent=panel_fiber_layer)
        sock_fiber_roughness_map = self._color_socket(self.in_fiber_layer_roughness_map, parent=panel_fiber_layer)
        sock_fiber_translucency_weight = self._float_socket(self.in_fiber_layer_translucency_weight, parent=panel_fiber_layer)
        sock_fiber_translucency_weight_map = self._color_socket(self.in_fiber_layer_translucency_weight_map, parent=panel_fiber_layer)
        sock_fiber_translucency_color = self._color_socket(self.in_fiber_layer_translucency_color, parent=panel_fiber_layer)
        sock_fiber_translucency_color_map = self._color_socket(self.in_fiber_layer_translucency_color_map, parent=panel_fiber_layer)

        # Sockets: Fine Detail
        sock_fine_detail_normal = self._float_socket(self.in_fine_detail_normal, 1, parent=panel_fine_detail)
        sock_fine_detail_normal_map = self._color_socket(self.in_fine_detail_normal_map, (0.5, 0.5, 1.0, 1.0), parent=panel_fine_detail)

        # Sockets: Geometry
        sock_cutout_opacity = self._float_socket(self.in_cutout_opacity, 1, parent=panel_geometry)
        sock_cutout_opacity_map = self._color_socket(self.in_cutout_opacity_map, parent=panel_geometry)
        sock_displacement_strength = self._float_socket(self.in_displacement_strength, 1, parent=panel_geometry)
        sock_displacement_strength_map = self._color_socket(self.in_displacement_strength_map, parent=panel_geometry)
        sock_minimum_displacement = self._float_socket(self.in_minimum_displacement, -0.1, parent=panel_geometry)
        sock_maximum_displacement = self._float_socket(self.in_maximum_displacement, 0.1, parent=panel_geometry)

        # Sockets: Glossy
        sock_glossy_layered_weight = self._float_socket(self.in_glossy_layered_weight, parent=panel_glossy)
        sock_glossy_layered_weight_map = self._color_socket(self.in_glossy_layered_weight_map, parent=panel_glossy)
        sock_glossy_color = self._color_socket(self.in_glossy_color, parent=panel_glossy)
        sock_glossy_color_map = self._color_socket(self.in_glossy_color_map, parent=panel_glossy)
        sock_glossy_reflectivity = self._float_socket(self.in_glossy_reflectivity, 0.5, parent=panel_glossy)
        sock_glossy_reflectivity_map = self._color_socket(self.in_glossy_reflectivity_map, parent=panel_glossy)
        sock_glossy_roughness = self._float_socket(self.in_glossy_roughness, parent=panel_glossy)
        sock_glossy_roughness_map = self._color_socket(self.in_glossy_roughness_map, parent=panel_glossy)

        # Sockets: Gradient Layer
        sock_gradient_layer_grazing_opacity = self._float_socket(self.in_gradient_layer_grazing_opacity, 1, parent=panel_gradient_layer)
        sock_gradient_layer_grazing_opacity_map = self._color_socket(self.in_gradient_layer_grazing_opacity_map, parent=panel_gradient_layer)
        sock_gradient_layer_normal_opacity = self._float_socket(self.in_gradient_layer_normal_opacity, parent=panel_gradient_layer)
        sock_gradient_layer_normal_opacity_map = self._color_socket(self.in_gradient_layer_normal_opacity_map, parent=panel_gradient_layer)
        sock_gradient_layer_exponent = self._float_socket(self.in_gradient_layer_exponent, 1, parent=panel_gradient_layer)
        sock_gradient_layer_exponent_map = self._color_socket(self.in_gradient_layer_exponent_map, parent=panel_gradient_layer)
        sock_gradient_layer_grazing_color = self._color_socket(self.in_gradient_layer_grazing_color, (0.0, 0.0, 0.0, 1.0), parent=panel_gradient_layer)
        sock_gradient_layer_grazing_color_map = self._color_socket(self.in_gradient_layer_grazing_color_map, parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint = self._color_socket(self.in_gradient_layer_normal_tint, (0.0, 0.0, 0.0, 1.0), parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint_map = self._color_socket(self.in_gradient_layer_normal_tint_map, parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint_weight = self._float_socket(self.in_gradient_layer_normal_tint_weight, parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint_weight_map = self._color_socket(self.in_gradient_layer_normal_tint_weight_map, parent=panel_gradient_layer)

        # Sockets: Metallic Flakes
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
        sock_top_coat_reflectivity = self._float_socket(self.in_top_coat_reflectivity, parent=panel_top_coat_general)
        sock_top_coat_reflectivity_map = self._color_socket(self.in_top_coat_reflectivity_map, parent=panel_top_coat_general)
        sock_top_coat_normal = self._float_socket(self.in_top_coat_normal, 1, parent=panel_top_coat_general)
        sock_top_coat_normal_map = self._color_socket(self.in_top_coat_normal_map, parent=panel_top_coat_general)
        sock_top_coat_bump = self._float_socket(self.in_top_coat_bump, 1, parent=panel_top_coat_general)
        sock_top_coat_bump_map = self._color_socket(self.in_top_coat_bump_map, parent=panel_top_coat_general)
        sock_top_coat_anisotropy = self._float_socket(self.in_top_coat_anisotropy, parent=panel_top_coat_general)
        sock_top_coat_anisotropy_map = self._color_socket(self.in_top_coat_anisotropy_map, parent=panel_top_coat_general)
        sock_top_coat_rotations = self._float_socket(self.in_top_coat_rotations, parent=panel_top_coat_general)
        sock_top_coat_rotations_map = self._color_socket(self.in_top_coat_rotations_map, parent=panel_top_coat_general)

        # Sockets: Thin Film
        sock_thin_film_weight = self._float_socket(self.in_thin_film_weight, parent=panel_thin_film)
        sock_thin_film_rotations = self._float_socket(self.in_thin_film_rotations, 30, parent=panel_thin_film)
        sock_thin_film_thickness = self._float_socket(self.in_thin_film_thickness, parent=panel_thin_film)
        sock_thin_film_thickness_map = self._color_socket(self.in_thin_film_thickness_map, parent=panel_thin_film)
        sock_thin_film_ior = self._float_socket(self.in_thin_film_ior, 1.5, parent=panel_thin_film)
        sock_thin_film_ior_map = self._color_socket(self.in_thin_film_ior_map, parent=panel_thin_film)

        # Output Sockets:
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")
        sock_out_displacement = self._vector_socket(self.out_displacement, in_out="OUTPUT")

        # Frames
        frame_normal = self._add_frame("Normal and Bump")
        reroute_normal_in = RerouteGroup(-3020.0, 800.0, frame_normal)

        frame_diffuse = self._add_frame("Diffuse")
        reroute_diffuse_in = RerouteGroup(-1960, 780.0, frame_diffuse)

        frame_fiber_layer = self._add_frame("Fiber Layer")
        reroute_fiber_layer_in = RerouteGroup(-1960, 640.0, frame_fiber_layer)
        reroute_fiber_layer_out = RerouteGroup(-1160, 640.0, frame_fiber_layer)

        frame_global_opacity = self._add_frame("global Opacity")

        frame_gradient_layer = self._add_frame("Gradient Layer")
        reroute_gradient_layer_in = RerouteGroup(-1960.0, -740, frame_gradient_layer)
        reroute_gradient_layer_out = RerouteGroup(-940, -740, frame_gradient_layer)

        reroute_metal_flakes = RerouteGroup(-940, -1120)
        reroute_top_coat = RerouteGroup(-940, -1440)


        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-3320, 400))

        # Nodes: Normal and Bump
        node_normal_map = self._add_node__normal_map("Normal Map", (-2980.0, 800.0), frame_normal)
        self._link_socket(node_group_input, node_normal_map, sock_normal, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_normal_map, sock_normal_map, 1, reroute_normal_in)

        node_detail_normal_map = self._add_node__normal_map("Detail Normal Map", (-2980.0, 760.0), frame_normal)
        self._link_socket(node_group_input, node_detail_normal_map, sock_fine_detail_normal, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_detail_normal_map, sock_fine_detail_normal_map, 1, reroute_normal_in)

        node_combine_normal_and_detail_vectors = self._add_node__math_vector("Combine normal and detail vectors", (-2780.0, 780.0), parent=frame_normal)
        self._link_socket(node_normal_map, node_combine_normal_and_detail_vectors, 0, 0)
        self._link_socket(node_detail_normal_map, node_combine_normal_and_detail_vectors, 0, 1)

        node_bump_map = self._add_node__bump("Bump map", (-2600.0, 780.0), frame_normal)
        self._link_socket(node_group_input, node_bump_map, sock_bump, 0, reroute_normal_in)
        self._link_socket(node_group_input, node_bump_map, sock_bump_map, 2, reroute_normal_in)
        self._link_socket(node_combine_normal_and_detail_vectors, node_bump_map, 0, 3)

        # Nodes: Diffuse
        node_mix_diffuse = self._add_node__mix("Mix Diffuse", (-1920.0, 780.0), parent=frame_diffuse)
        self._link_socket(node_group_input, node_mix_diffuse, sock_diffuse, 6, reroute_diffuse_in)
        self._link_socket(node_group_input, node_mix_diffuse, sock_diffuse_map, 7, reroute_diffuse_in)

        node_diffuse_layer = self._add_node(ShaderNodeBsdfDiffuse, "Diffuse BSDF", (-1740.0, 780.0), frame_diffuse)
        self._link_socket(node_mix_diffuse, node_diffuse_layer, 2, 0)
        self._link_socket(node_bump_map, node_diffuse_layer, 0, 2, reroute_diffuse_in)

        # Nodes: Fiber Layer
        node_mix_fiber_weight = self._add_node__hsv("Mix Fiber Weight", (-1920.0, 640.0), frame_fiber_layer)
        self._link_socket(node_group_input, node_mix_fiber_weight, sock_fiber_weight, 2, reroute_fiber_layer_in)
        self._link_socket(node_group_input, node_mix_fiber_weight, sock_fiber_weight_map, 4, reroute_fiber_layer_in)

        node_mix_fiber_metallic_weight = self._add_node__hsv("Mix Fiber Metallic Weight", (-1920.0, 600.0), frame_fiber_layer)
        self._link_socket(node_group_input, node_mix_fiber_metallic_weight, sock_fiber_metallic_weight, 2, reroute_fiber_layer_in)
        self._link_socket(node_group_input, node_mix_fiber_metallic_weight, sock_fiber_metallic_weight_map, 4, reroute_fiber_layer_in)

        node_mix_fiber_color = self._add_node__mix("Mix Fiber Color", (-1920.0, 560.0), parent=frame_fiber_layer)
        self._link_socket(node_group_input, node_mix_fiber_color, sock_fiber_color, 6, reroute_fiber_layer_in)
        self._link_socket(node_group_input, node_mix_fiber_color, sock_fiber_color_map, 7, reroute_fiber_layer_in)

        node_mix_fiber_roughness = self._add_node__hsv("Mix Fiber Roughness", (-1920.0, 520.0), frame_fiber_layer)
        self._link_socket(node_group_input, node_mix_fiber_roughness, sock_fiber_roughness, 2, reroute_fiber_layer_in)
        self._link_socket(node_group_input, node_mix_fiber_roughness, sock_fiber_roughness_map, 4, reroute_fiber_layer_in)

        node_mix_fiber_translucency_weight = self._add_node__hsv("Mix Fiber Translucency Weight", (-1920.0, 480.0), frame_fiber_layer)
        self._link_socket(node_group_input, node_mix_fiber_translucency_weight, sock_fiber_translucency_weight, 2, reroute_fiber_layer_in)
        self._link_socket(node_group_input, node_mix_fiber_translucency_weight, sock_fiber_translucency_weight_map, 4, reroute_fiber_layer_in)

        node_mix_fiber_translucency_color = self._add_node__mix("Mix Fiber Translucency Color", (-1920.0, 440.0), parent=frame_fiber_layer)
        self._link_socket(node_group_input, node_mix_fiber_translucency_color, sock_fiber_translucency_color, 6, reroute_fiber_layer_in)
        self._link_socket(node_group_input, node_mix_fiber_translucency_color, sock_fiber_translucency_color_map, 7, reroute_fiber_layer_in)

        node_fiber_metallic_bsdf = self._add_node(ShaderNodeBsdfMetallic, "Fiber Metallic BSDF", (-1640.0, 560.0), frame_fiber_layer)
        self._link_socket(node_mix_fiber_color, node_fiber_metallic_bsdf, 2, 0)
        self._link_socket(node_mix_fiber_roughness, node_fiber_metallic_bsdf, 0, 2)
        self._link_socket(node_bump_map, node_fiber_metallic_bsdf, 0, 7, reroute_fiber_layer_in)

        node_fiber_diffuse_bsdf = self._add_node(ShaderNodeBsdfDiffuse, "Fiber Diffuse BSDF", (-1640.0, 500.0), frame_fiber_layer)
        self._link_socket(node_mix_fiber_color, node_fiber_diffuse_bsdf, 2, 0)
        self._link_socket(node_mix_fiber_roughness, node_fiber_diffuse_bsdf, 0, 1)
        self._link_socket(node_bump_map, node_fiber_diffuse_bsdf, 0, 2,  reroute_fiber_layer_in)

        node_fiber_translucent_bsdf = self._add_node(ShaderNodeBsdfTranslucent, "Fiber Translucent BSDF", (-1640.0, 460.0), frame_fiber_layer)
        self._link_socket(node_mix_fiber_translucency_color, node_fiber_translucent_bsdf, 2, 0)
        self._link_socket(node_bump_map, node_fiber_translucent_bsdf, 0, 1,  reroute_fiber_layer_in)

        node_fiber_mix_met_diff = self._add_node__mix_shader("Fiber Mix Metallic and Diffuse", (-1320.0, 520.0), frame_fiber_layer)
        self._link_socket(node_mix_fiber_metallic_weight, node_fiber_mix_met_diff, 0, 0)
        self._link_socket(node_fiber_diffuse_bsdf, node_fiber_mix_met_diff, 0, 1)
        self._link_socket(node_fiber_metallic_bsdf, node_fiber_mix_met_diff, 0, 1)

        node_fiber_layer_bsdf = self._add_node__mix_shader("Fiber Mix M/D and Translucent", (-1320.0, 480.0), frame_fiber_layer)
        self._link_socket(node_mix_fiber_translucency_weight, node_fiber_layer_bsdf, 0, 0)
        self._link_socket(node_fiber_mix_met_diff, node_fiber_layer_bsdf, 0, 1)
        self._link_socket(node_fiber_translucent_bsdf, node_fiber_layer_bsdf, 0, 2)

        # Nodes: Cutout Opacity
        node_mix_global_opacity_weight = self._add_node__hsv("Mix Cutout Opacity", (-1960.0, 260.0), frame_global_opacity)
        self._link_socket(node_group_input, node_mix_global_opacity_weight, sock_cutout_opacity, 2)
        self._link_socket(node_group_input, node_mix_global_opacity_weight, sock_cutout_opacity_map, 4)

        node_global_opacity_bsdf = self._add_node(ShaderNodeBsdfTransparent, "Cutout Opacity BSDF", (-1960.0, 220.0), frame_global_opacity)

        # Nodes: Asymetrical Displacement
        displacement_b = AsymmetricalDisplacementShaderGroupBuilder
        node_displacement = self._add_node__shader_group("Asymmetrical Displacement", displacement_b, (-1960.0, 140.0))
        self._link_socket(node_group_input, node_displacement, sock_displacement_strength, displacement_b.in_strength)
        self._link_socket(node_group_input, node_displacement, sock_displacement_strength_map, displacement_b.in_strength_map)
        self._link_socket(node_group_input, node_displacement, sock_minimum_displacement, displacement_b.in_min_displacement)
        self._link_socket(node_group_input, node_displacement, sock_maximum_displacement, displacement_b.in_max_displacement)
        self._link_socket(node_bump_map, node_displacement, 0, displacement_b.in_normal)

        # Nodes: Glossy Layer
        glossy_b = AdvancedTopCoatShaderGroupBuilder
        node_glossy_layer = self._add_node__shader_group("Glossy Layer", glossy_b, (-1960.0, -60.0))
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_layered_weight, glossy_b.in_top_coat_weight)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_layered_weight_map, glossy_b.in_top_coat_weight_map)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_color, glossy_b.in_top_coat_color)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_color_map, glossy_b.in_top_coat_color_map)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_roughness, glossy_b.in_top_coat_roughness)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_roughness_map, glossy_b.in_top_coat_roughness_map)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_reflectivity, glossy_b.in_top_coat_reflectivity)
        self._link_socket(node_group_input, node_glossy_layer, sock_glossy_reflectivity_map, glossy_b.in_top_coat_reflectivity_map)
        self._link_socket(node_bump_map, node_glossy_layer, 0, glossy_b.in_top_coat_bump_vector)

        # Nodes: Gradient Layer
        node_mix_gradient_grazing_op = self._add_node__hsv("Mix Gradient Layer Grazing Opacity", (-1940.0, -740), frame_gradient_layer)
        self._link_socket(node_group_input, node_mix_gradient_grazing_op, sock_gradient_layer_grazing_opacity, 2, reroute_gradient_layer_in)
        self._link_socket(node_group_input, node_mix_gradient_grazing_op, sock_gradient_layer_grazing_opacity_map, 4, reroute_gradient_layer_in)

        node_mix_gradient_normal_op = self._add_node__hsv("Mix Gradient Layer Normal Opacity", (-1940.0, -780), frame_gradient_layer)
        self._link_socket(node_group_input, node_mix_gradient_normal_op, sock_gradient_layer_normal_opacity, 2, reroute_gradient_layer_in)
        self._link_socket(node_group_input, node_mix_gradient_normal_op, sock_gradient_layer_normal_opacity_map, 4, reroute_gradient_layer_in)

        node_mix_gradient_exponent = self._add_node__hsv("Mix Gradient Layer Exponent", (-1940.0, -820), frame_gradient_layer)
        self._link_socket(node_group_input, node_mix_gradient_exponent, sock_gradient_layer_exponent, 2, reroute_gradient_layer_in)
        self._link_socket(node_group_input, node_mix_gradient_exponent, sock_gradient_layer_exponent_map, 4, reroute_gradient_layer_in)

        node_mix_gradient_grazing_color = self._add_node__mix("Mix Gradient Layer Grazing Color", (-1940.0, -860), parent=frame_gradient_layer)
        self._link_socket(node_group_input, node_mix_gradient_grazing_color, sock_gradient_layer_grazing_color, 6, reroute_gradient_layer_in)
        self._link_socket(node_group_input, node_mix_gradient_grazing_color, sock_gradient_layer_grazing_color_map, 7, reroute_gradient_layer_in)

        node_mix_gradient_normal_tint = self._add_node__mix("Mix Gradient Layer Normal Tint", (-1940.0, -900), parent=frame_gradient_layer)
        self._link_socket(node_group_input, node_mix_gradient_normal_tint, sock_gradient_layer_normal_tint, 6, reroute_gradient_layer_in)
        self._link_socket(node_group_input, node_mix_gradient_normal_tint, sock_gradient_layer_normal_tint_map, 7, reroute_gradient_layer_in)

        node_mix_gradient_normal_tint_weight = self._add_node__hsv("Mix Gradient Layer Normal Tint Weight", (-1940.0, -940), frame_gradient_layer)
        self._link_socket(node_group_input, node_mix_gradient_normal_tint_weight, sock_gradient_layer_normal_tint_weight, 2, reroute_gradient_layer_in)
        self._link_socket(node_group_input, node_mix_gradient_normal_tint_weight, sock_gradient_layer_normal_tint_weight_map, 4, reroute_gradient_layer_in)

        node_gradient_layer_weight = self._add_node(ShaderNodeLayerWeight, "Gradient Layer Weight", (-1720.0, -740), frame_gradient_layer)
        self._link_socket(node_bump_map, node_gradient_layer_weight, 0, 1, reroute_gradient_layer_in)

        node_gradient_apply_exponent = self._add_node__math("Gradient Layer Apply Exponent", (-1720.0, -820), "POWER", frame_gradient_layer)
        self._link_socket(node_gradient_layer_weight, node_gradient_apply_exponent, 1, 0)
        self._link_socket(node_mix_gradient_exponent, node_gradient_apply_exponent, 0, 1)

        node_mix_gradient_normal_vs_grazing_op = self._add_node__mix("Mix Gradient Layer Normal vs Grazing Opacity", (-1520.0, -800), blend_type="MIX", parent=frame_gradient_layer)
        self._link_socket(node_gradient_apply_exponent, node_mix_gradient_normal_vs_grazing_op, 0, 0)
        self._link_socket(node_mix_gradient_normal_op, node_mix_gradient_normal_vs_grazing_op, 0, 6)
        self._link_socket(node_mix_gradient_grazing_op, node_mix_gradient_normal_vs_grazing_op, 0, 7)

        node_mix_gradient_normal_vs_grazing_color = self._add_node__mix("Mix Gradient Layer Normal vs Grazing Color", (-1520.0, -880), blend_type="MIX", parent=frame_gradient_layer)
        self._link_socket(node_gradient_apply_exponent, node_mix_gradient_normal_vs_grazing_color, 0, 0)
        self._link_socket(node_mix_gradient_normal_tint, node_mix_gradient_normal_vs_grazing_color, 2, 6)
        self._link_socket(node_mix_gradient_grazing_color, node_mix_gradient_normal_vs_grazing_color, 2, 7)

        node_gradient_transparent_bsdf = self._add_node(ShaderNodeBsdfTransparent, "Gradient Layer Transparent BSDF", (-1300.0, -760), frame_gradient_layer)

        node_gradient_diffuse_bsdf = self._add_node(ShaderNodeBsdfDiffuse, "Gradient Layer Diffuse BSDF", (-1300.0, -900), frame_gradient_layer)
        self._link_socket(node_mix_gradient_normal_vs_grazing_color, node_gradient_diffuse_bsdf, 2, 0)
        self._link_socket(node_bump_map, node_gradient_diffuse_bsdf, 0, 2, reroute_gradient_layer_in)

        node_gradient_layer_bsdf = self._add_node__mix_shader("Gradient Layer BSDF", (-1100.0, -840), frame_gradient_layer)
        self._link_socket(node_mix_gradient_normal_vs_grazing_op, node_gradient_layer_bsdf, 2, 0)
        self._link_socket(node_gradient_transparent_bsdf, node_gradient_layer_bsdf, 0, 1)
        self._link_socket(node_gradient_diffuse_bsdf, node_gradient_layer_bsdf, 0, 2)

        # Nodes: Metallic Flakes
        metallic_flakes_b = MetallicFlakesShaderGroupBuilder
        node_metallic_flakes = self._add_node__shader_group("Metallic Flakes", metallic_flakes_b, (-1960.0, -1080.0))
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_weight, metallic_flakes_b.in_weight)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_weight_map, metallic_flakes_b.in_weight_map)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_color, metallic_flakes_b.in_color)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_color_map, metallic_flakes_b.in_color_map)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_roughness, metallic_flakes_b.in_roughness)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_roughness_map, metallic_flakes_b.in_roughness_map)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_size, metallic_flakes_b.in_flake_size)
        self._link_socket(node_group_input, node_metallic_flakes, sock_metallic_flakes_density, metallic_flakes_b.in_flake_density)
        self._link_socket(node_bump_map, node_metallic_flakes, 0, metallic_flakes_b.in_normal)

        # Nodes: Top Coat and Thin Film
        coat_b = AdvancedTopCoatShaderGroupBuilder
        node_top_coat = self._add_node__shader_group("Top Coat", coat_b, (-1960.0, -1400.0))
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_weight, coat_b.in_top_coat_weight)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_weight_map, coat_b.in_top_coat_weight_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_color, coat_b.in_top_coat_color)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_color_map, coat_b.in_top_coat_color_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_roughness, coat_b.in_top_coat_roughness)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_roughness_map, coat_b.in_top_coat_roughness_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_reflectivity, coat_b.in_top_coat_reflectivity)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_reflectivity_map, coat_b.in_top_coat_reflectivity_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_normal, coat_b.in_top_coat_normal)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_normal_map, coat_b.in_top_coat_normal_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_bump, coat_b.in_top_coat_bump)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_bump_map, coat_b.in_top_coat_bump_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_anisotropy, coat_b.in_top_coat_anisotropy)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_anisotropy_map, coat_b.in_top_coat_anisotropy_map)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_rotations, coat_b.in_top_coat_rotations)
        self._link_socket(node_group_input, node_top_coat, sock_top_coat_rotations_map, coat_b.in_top_coat_rotations_map)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_weight, coat_b.in_thin_film_weight)

        self._link_socket(node_group_input, node_top_coat, sock_thin_film_rotations, coat_b.in_thin_film_rotations)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_thickness, coat_b.in_thin_film_thickness)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_thickness_map, coat_b.in_thin_film_thickness_map)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_ior, coat_b.in_thin_film_ior)
        self._link_socket(node_group_input, node_top_coat, sock_thin_film_ior_map, coat_b.in_thin_film_ior_map)

        # Nodes: Mix Shaders
        node_mix_gradient_layer = self._add_node__mix_shader("Mix Gradient Layer", (-220.0, 200.0))
        self._link_socket(node_mix_gradient_normal_tint_weight, node_mix_gradient_layer, 0,0, reroute_gradient_layer_out)
        self._link_socket(node_diffuse_layer, node_mix_gradient_layer, 0,1)
        self._link_socket(node_gradient_layer_bsdf, node_mix_gradient_layer, 0,2, reroute_gradient_layer_out)

        node_mix_fiber_layer = self._add_node__mix_shader("Mix Fiber Layer", (-220.0, 160.0))
        self._link_socket(node_mix_fiber_weight, node_mix_fiber_layer, 0,0, reroute_fiber_layer_out)
        self._link_socket(node_mix_gradient_layer, node_mix_fiber_layer, 0,1)
        self._link_socket(node_fiber_layer_bsdf, node_mix_fiber_layer, 0,2, reroute_fiber_layer_out)

        node_mix_glossy_layer = self._add_node__mix_shader("Mix Glossy Layer", (-220.0, 120.0))
        self._link_socket(node_glossy_layer, node_mix_glossy_layer, glossy_b.out_fac,0)
        self._link_socket(node_mix_fiber_layer, node_mix_glossy_layer, 0,1)
        self._link_socket(node_glossy_layer, node_mix_glossy_layer, glossy_b.out_shader,2)

        node_mix_flakes_layer = self._add_node__mix_shader("Mix Metallic Flakes Layer", (-220.0, 80.0))
        self._link_socket(node_metallic_flakes, node_mix_flakes_layer, metallic_flakes_b.out_fac,0, reroute_metal_flakes)
        self._link_socket(node_mix_glossy_layer, node_mix_flakes_layer, 0,1)
        self._link_socket(node_metallic_flakes, node_mix_flakes_layer, metallic_flakes_b.out_shader,2, reroute_metal_flakes)

        node_mix_coat_layer = self._add_node__mix_shader("Mix Top Coat Layer", (-220.0, 40.0))
        self._link_socket(node_top_coat, node_mix_coat_layer, coat_b.out_fac,0, reroute_top_coat)
        self._link_socket(node_mix_flakes_layer, node_mix_coat_layer, 0,1)
        self._link_socket(node_top_coat, node_mix_coat_layer, coat_b.out_shader,2, reroute_top_coat)

        node_mix_global_opacity = self._add_node__mix_shader("Mix Global Opacity", (-220.0, 0.0))
        self._link_socket(node_mix_global_opacity_weight, node_mix_global_opacity, 0,0)
        self._link_socket(node_global_opacity_bsdf, node_mix_global_opacity, 0,1)
        self._link_socket(node_mix_coat_layer, node_mix_global_opacity, 0,2)

        # Group Output
        node_group_output = self._add_node__group_output("Group Output", (0, 0))
        self._link_socket(node_mix_global_opacity, node_group_output, 0, sock_out_surface)
        self._link_socket(node_displacement, node_group_output, 0, sock_out_displacement)
        # @formatter:on

        self.hide_all_nodes(
            node_group_input,
            node_group_output,
            node_displacement,
            node_glossy_layer,
            node_metallic_flakes,
            node_top_coat)


class IWaveTranslucentFabricShaderGroupApplier(ShaderGroupApplier):
    mapping_node_location_offset = -50

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        builder = IWaveTranslucentFabricShaderGroupBuilder

        # # @formatter:off
        # Base Diffuse
        self._channel_to_inputs("diffuse", builder.in_diffuse, builder.in_diffuse_map, False)

        # Geometry
        geo_mapping_props = ["horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset"]
        if self._channel_enabled(*geo_mapping_props):
            self._set_material_mapping(*geo_mapping_props)

        self._channel_to_inputs("displacement_strength", builder.in_displacement_strength, builder.in_displacement_strength_map)
        self._channel_to_inputs("minimum_displacement", builder.in_minimum_displacement, None)
        self._channel_to_inputs("maximum_displacement", builder.in_maximum_displacement, None)

        node_cutout_tex = self._channel_to_inputs("cutout_opacity", builder.in_cutout_opacity, builder.in_cutout_opacity_map)
        cutout_mapping_props = ["cutout_opacity_horizontal_tiles", "cutout_opacity_horizontal_offset", "cutout_opacity_vertical_tiles", "cutout_opacity_vertical_offset"]
        if self._channel_enabled(*cutout_mapping_props) and node_cutout_tex:
            cutout_mapping_node_loc = tuple_zip_sum((0, self.mapping_node_location_offset * 2), self._mapping.location.to_tuple())
            cutout_mapping_node = self._add_node(ShaderNodeMapping, "Cutout Opacity Mapping", cutout_mapping_node_loc, props={"vector_type": "POINT", "hide": True})
            self._link_socket(self._uv_map, cutout_mapping_node, 0, 0)
            self._link_socket(cutout_mapping_node, node_cutout_tex, 0, 0)
            self._set_material_mapping(*cutout_mapping_props, mapping_node=cutout_mapping_node)

        # Bump
        self._channel_to_inputs("normal_map", builder.in_base_normal, builder.in_base_normal_map)
        self._channel_to_inputs("bump_strength", builder.in_base_bump, builder.in_base_bump_map)

        # Fiber Layer
        if self._channel_enabled("fiber_layer_weight"):
            self._channel_to_inputs("metallic_weight", builder.in_fiber_layer_metallic_weight, builder.in_fiber_layer_metallic_weight_map)
            self._channel_to_inputs("diffuse_overlay_color", builder.in_fiber_layer_color, builder.in_fiber_layer_color_map)
            self._channel_to_inputs("diffuse_roughness", builder.in_fiber_layer_roughness, builder.in_fiber_layer_roughness_map)
            self._channel_to_inputs("translucency_weight", builder.in_fiber_layer_translucency_weight, builder.in_fiber_layer_translucency_weight_map)
            self._channel_to_inputs("translucency_color", builder.in_fiber_layer_translucency_color, builder.in_fiber_layer_translucency_color_map)

        # Fine Detail
        node_fd_normal_tex = self._channel_to_inputs("fine_detail_normal_map", builder.in_fine_detail_normal, builder.in_fine_detail_normal_map, force_new_image_node=True)

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
            self._channel_to_inputs("glossy_layered_weight", builder.in_glossy_layered_weight, builder.in_glossy_layered_weight_map)
            self._channel_to_inputs("glossy_color", builder.in_glossy_color, builder.in_glossy_color_map)
            self._channel_to_inputs("glossy_reflectivity", builder.in_glossy_reflectivity, builder.in_glossy_reflectivity_map)
            self._channel_to_inputs("glossy_roughness", builder.in_glossy_roughness, builder.in_glossy_roughness_map)

        # Gradient Layer
        self._channel_to_inputs("gradient_layer_normal_reflectivity", builder.in_gradient_layer_normal_opacity, builder.in_gradient_layer_normal_opacity_map)
        self._channel_to_inputs("gradient_layer_grazing_reflectivity", builder.in_gradient_layer_grazing_opacity, builder.in_gradient_layer_grazing_opacity_map)
        self._channel_to_inputs("gradient_layer_exponent", builder.in_gradient_layer_exponent, builder.in_gradient_layer_exponent_map)
        self._channel_to_inputs("gradient_layer_grazing_color", builder.in_gradient_layer_grazing_color, builder.in_gradient_layer_grazing_color_map)
        self._channel_to_inputs("gradient_layer_normal_tint", builder.in_gradient_layer_normal_tint, builder.in_gradient_layer_normal_tint_map)
        self._channel_to_inputs("gradient_layer_normal_tint_weight", builder.in_gradient_layer_normal_tint_weight, builder.in_gradient_layer_normal_tint_weight_map)

        # Metallic Flakes
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
            self._channel_to_inputs("top_coat_reflectivity", builder.in_top_coat_reflectivity, builder.in_top_coat_reflectivity_map)
            self._channel_to_inputs("top_coat_anisotropy", builder.in_top_coat_anisotropy, builder.in_top_coat_anisotropy_map)
            self._channel_to_inputs("top_coat_rotations", builder.in_top_coat_rotations, builder.in_top_coat_anisotropy_map)

            self._channel_to_inputs("top_coat_normal", builder.in_top_coat_normal, builder.in_top_coat_normal_map)
            self._channel_to_inputs("top_coat_bump", builder.in_top_coat_bump, builder.in_top_coat_bump_map)

        # Thin Film
        if self._channel_enabled("thin_film_thickness"):
            self._set_socket(self._shader_group, builder.in_thin_film_weight, 0.5)
            self._channel_to_inputs("thin_film_thickness", builder.in_thin_film_thickness, builder.in_thin_film_thickness_map)
            self._channel_to_inputs("thin_film_ior", builder.in_thin_film_ior, builder.in_thin_film_ior_map)
        # @formatter:on
