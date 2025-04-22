from .support import ShaderGroupApplier, ShaderGroupBuilder

from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "iWave Translucent Fabric"
__MATERIAL_TYPE_ID__ = "translucent_fabric"


class IWaveTranslucentFabricShaderGroupBuilder(ShaderGroupBuilder):
    in_diffuse = "Diffuse"
    in_diffuse_map = "Diffuse Map"

    in_normal_map = "Normal Map"
    in_normal_map_map = "Normal Map Map"
    in_crumple_normal_map = "Crumple Normal Map"
    in_crumple_normal_map_map = "Crumple Normal Map Map"

    in_fiber_layer_weight = "Fiber Layer Weight"
    in_fiber_layer_weight_map = "Fiber Layer Weight Map"
    in_metallic_weight = "Metallic Weight"
    in_metallic_weight_map = "Metallic Weight Map"
    in_diffuse_overlay_color = "Diffuse Overlay Color"
    in_diffuse_overlay_color_map = "Diffuse Overlay Color Map"
    in_diffuse_roughness = "Diffuse Roughness"
    in_diffuse_roughness_map = "Diffuse Roughness Map"
    in_translucency_weight = "Translucency Weight"
    in_translucency_weight_map = "Translucency Weight Map"
    in_translucency_color = "Translucency Color"
    in_translucency_color_map = "Translucency Color Map"
    in_fiber_layer_weight_map_horizontal_tiles = "Fiber Layer Weight Map Horizontal Tiles"
    in_fiber_layer_weight_map_horizontal_offset = "Fiber Layer Weight Map Horizontal Offset"
    in_fiber_layer_weight_map_vertical_tiles = "Fiber Layer Weight Map Vertical Tiles"
    in_fiber_layer_weight_map_vertical_offset = "Fiber Layer Weight Map Vertical Offset"

    in_fine_detail_blend_weight = "Fine Detail Blend Weight"
    in_fine_detail_map = "Fine Detail Map"
    in_fine_detail_blend_mode = "Fine Detail Blend Mode"
    in_fine_detail_glossy_reflectivity = "Fine Detail Glossy Reflectivity"
    in_fine_detail_glossy_reflectivity_map = "Fine Detail Glossy Reflectivity Map"
    in_fine_detail_normal_map = "Fine Detail Normal Map"
    in_fine_detail_normal_map_map = "Fine Detail Normal Map Map"
    in_fine_detail_and_crumple_normal = "Fine Detail And Crumple Normal"
    in_fine_detail_and_crumple_normal_map = "Fine Detail And Crumple Normal Map"
    in_fine_detail_and_crumple_bump = "Fine Detail And Crumple Bump"
    in_fine_detail_and_crumple_bump_map = "Fine Detail And Crumple Bump Map"
    in_fine_detail_horizontal_tiles = "Fine Detail Horizontal Tiles"
    in_fine_detail_horizontal_offset = "Fine Detail Horizontal Offset"
    in_fine_detail_vertical_tiles = "Fine Detail Vertical Tiles"
    in_fine_detail_vertical_offset = "Fine Detail Vertical Offset"

    in_cutout_opacity = "Cutout Opacity"
    in_cutout_opacity_map = "Cutout Opacity Map"
    in_displacement_strength = "Displacement Strength"
    in_displacement_strength_map = "Displacement Strength Map"
    in_minimum_displacement = "Minimum Displacement"
    in_maximum_displacement = "Maximum Displacement"
    in_subd_displacement_level = "Subd Displacement Level"
    in_horizontal_tiles = "Horizontal Tiles"
    in_horizontal_offset = "Horizontal Offset"
    in_vertical_tiles = "Vertical Tiles"
    in_vertical_offset = "Vertical Offset"
    in_cutout_opacity_horizontal_tiles = "Cutout Opacity Horizontal Tiles"
    in_cutout_opacity_horizontal_offset = "Cutout Opacity Horizontal Offset"
    in_cutout_opacity_vertical_tiles = "Cutout Opacity Vertical Tiles"
    in_cutout_opacity_vertical_offset = "Cutout Opacity Vertical Offset"

    in_glossy_layered_weight = "Glossy Layered Weight"
    in_glossy_layered_weight_map = "Glossy Layered Weight Map"
    in_share_glossy_inputs = "Share Glossy Inputs"
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

    in_gradient_layer_grazing_color = "Gradient Layer Grazing Color"
    in_gradient_layer_grazing_color_map = "Gradient Layer Grazing Color Map"
    in_gradient_layer_normal_tint = "Gradient Layer Normal Tint"
    in_gradient_layer_normal_tint_map = "Gradient Layer Normal Tint Map"
    in_gradient_layer_normal_tint_weight = "Gradient Layer Normal Tint Weight"
    in_gradient_layer_normal_tint_weight_map = "Gradient Layer Normal Tint Weight Map"
    in_gradient_layer_normal_reflectivity = "Gradient Layer Normal Reflectivity"
    in_gradient_layer_normal_reflectivity_map = "Gradient Layer Normal Reflectivity Map"
    in_gradient_layer_grazing_reflectivity = "Gradient Layer Grazing Reflectivity"
    in_gradient_layer_grazing_reflectivity_map = "Gradient Layer Grazing Reflectivity Map"
    in_gradient_layer_exponent = "Gradient Layer Exponent"
    in_gradient_layer_exponent_map = "Gradient Layer Exponent Map"
    in_gradient_layer_strength = "Gradient Layer Strength"
    in_gradient_layer_metallic_weight = "Gradient Layer Metallic Weight"
    in_gradient_layer_glossy_layered_weight = "Gradient Layer Glossy Layered Weight"
    in_gradient_layer_refraction_index = "Gradient Layer Refraction Index"
    in_gradient_layer_refraction_weight = "Gradient Layer Refraction Weight"

    in_metallic_flakes_weight = "Metallic Flakes Weight"
    in_metallic_flakes_weight_map = "Metallic Flakes Weight Map"
    in_metallic_flakes_color = "Metallic Flakes Color"
    in_metallic_flakes_color_map = "Metallic Flakes Color Map"
    in_metallic_flakes_roughness = "Metallic Flakes Roughness"
    in_metallic_flakes_roughness_map = "Metallic Flakes Roughness Map"
    in_metallic_flakes_size = "Metallic Flakes Size"
    in_metallic_flakes_strength = "Metallic Flakes Strength"
    in_metallic_flakes_density = "Metallic Flakes Density"

    in_thin_film_thickness = "Thin Film Thickness"
    in_thin_film_thickness_map = "Thin Film Thickness Map"
    in_thin_film_ior = "Thin Film Ior"
    in_thin_film_ior_map = "Thin Film Ior Map"

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

    out_surface = "Surface"
    out_volume = "Volume"
    out_displacement = "Displacement"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    # noinspection PyUnusedLocal
    def setup_group(self):
        super().setup_group()

        # @formatter:off
        panel_base_diffuse = self._add_panel("Base Diffuse")
        panel_bump = self._add_panel("Bump")
        panel_fiber_layer = self._add_panel("Fiber Layer")
        panel_fine_detail = self._add_panel("Fine Detail")
        panel_geometry = self._add_panel("Geometry")
        panel_glossy = self._add_panel("Glossy")
        panel_gradient_layer = self._add_panel("Gradient Layer")
        panel_metallic_flakes_flakes = self._add_panel("Metallic Flakes Flakes")
        panel_thin_film = self._add_panel("Thin Film")
        panel_top_coat_general = self._add_panel("Top Coat")

        # Sockets: Base Diffuse
        sock_diffuse = self._color_socket(self.in_diffuse, parent=panel_base_diffuse)
        sock_diffuse_map = self._color_socket(self.in_diffuse_map, parent=panel_base_diffuse)

        # Sockets: Bump
        sock_normal_map = self._float_socket(self.in_normal_map, 1, parent=panel_bump)
        sock_normal_map_map = self._color_socket(self.in_normal_map_map, parent=panel_bump)
        sock_crumple_normal_map = self._float_socket(self.in_crumple_normal_map, 1, parent=panel_bump)
        sock_crumple_normal_map_map = self._color_socket(self.in_crumple_normal_map_map, parent=panel_bump)

        # Sockets: Fiber Layer
        sock_fiber_layer_weight = self._float_socket(self.in_fiber_layer_weight, parent=panel_fiber_layer)
        sock_fiber_layer_weight_map = self._color_socket(self.in_fiber_layer_weight_map, parent=panel_fiber_layer)
        sock_metallic_weight = self._float_socket(self.in_metallic_weight, parent=panel_fiber_layer)
        sock_metallic_weight_map = self._color_socket(self.in_metallic_weight_map, parent=panel_fiber_layer)
        sock_diffuse_overlay_color = self._color_socket(self.in_diffuse_overlay_color, parent=panel_fiber_layer)
        sock_diffuse_overlay_color_map = self._color_socket(self.in_diffuse_overlay_color_map, parent=panel_fiber_layer)
        sock_diffuse_roughness = self._float_socket(self.in_diffuse_roughness, parent=panel_fiber_layer)
        sock_diffuse_roughness_map = self._color_socket(self.in_diffuse_roughness_map, parent=panel_fiber_layer)
        sock_translucency_weight = self._float_socket(self.in_translucency_weight, parent=panel_fiber_layer)
        sock_translucency_weight_map = self._color_socket(self.in_translucency_weight_map, parent=panel_fiber_layer)
        sock_translucency_color = self._color_socket(self.in_translucency_color, parent=panel_fiber_layer)
        sock_translucency_color_map = self._color_socket(self.in_translucency_color_map, parent=panel_fiber_layer)
        sock_fiber_layer_weight_map_horizontal_tiles = self._float_socket(self.in_fiber_layer_weight_map_horizontal_tiles, 1, parent=panel_fiber_layer)
        sock_fiber_layer_weight_map_horizontal_offset = self._float_socket(self.in_fiber_layer_weight_map_horizontal_offset, parent=panel_fiber_layer)
        sock_fiber_layer_weight_map_vertical_tiles = self._float_socket(self.in_fiber_layer_weight_map_vertical_tiles, 1, parent=panel_fiber_layer)
        sock_fiber_layer_weight_map_vertical_offset = self._float_socket(self.in_fiber_layer_weight_map_vertical_offset, parent=panel_fiber_layer)

        # Sockets: Fine Detail
        sock_fine_detail_blend_weight = self._float_socket(self.in_fine_detail_blend_weight, parent=panel_fine_detail)
        sock_fine_detail_map = self._color_socket(self.in_fine_detail_map, parent=panel_fine_detail)
        sock_fine_detail_blend_mode = self._float_socket(self.in_fine_detail_blend_mode, 2, parent=panel_fine_detail)
        sock_fine_detail_glossy_reflectivity = self._float_socket(self.in_fine_detail_glossy_reflectivity, 0.5, parent=panel_fine_detail)
        sock_fine_detail_glossy_reflectivity_map = self._color_socket(self.in_fine_detail_glossy_reflectivity_map, parent=panel_fine_detail)
        sock_fine_detail_normal_map = self._float_socket(self.in_fine_detail_normal_map, 1, parent=panel_fine_detail)
        sock_fine_detail_normal_map_map = self._color_socket(self.in_fine_detail_normal_map_map, parent=panel_fine_detail)
        sock_fine_detail_and_crumple_normal = self._float_socket(self.in_fine_detail_and_crumple_normal, 1, parent=panel_fine_detail)
        sock_fine_detail_and_crumple_normal_map = self._color_socket(self.in_fine_detail_and_crumple_normal_map, parent=panel_fine_detail)
        sock_fine_detail_and_crumple_bump = self._float_socket(self.in_fine_detail_and_crumple_bump, 1, parent=panel_fine_detail)
        sock_fine_detail_and_crumple_bump_map = self._color_socket(self.in_fine_detail_and_crumple_bump_map, parent=panel_fine_detail)
        sock_fine_detail_horizontal_tiles = self._float_socket(self.in_fine_detail_horizontal_tiles, 1, parent=panel_fine_detail)
        sock_fine_detail_horizontal_offset = self._float_socket(self.in_fine_detail_horizontal_offset, parent=panel_fine_detail)
        sock_fine_detail_vertical_tiles = self._float_socket(self.in_fine_detail_vertical_tiles, 1, parent=panel_fine_detail)
        sock_fine_detail_vertical_offset = self._float_socket(self.in_fine_detail_vertical_offset, parent=panel_fine_detail)

        # Sockets: Geometry Cutout
        sock_cutout_opacity = self._float_socket(self.in_cutout_opacity, 1, parent=panel_geometry)
        sock_cutout_opacity_map = self._color_socket(self.in_cutout_opacity_map, parent=panel_geometry)
        sock_displacement_strength = self._float_socket(self.in_displacement_strength, 1, parent=panel_geometry)
        sock_displacement_strength_map = self._color_socket(self.in_displacement_strength_map, parent=panel_geometry)
        sock_minimum_displacement = self._float_socket(self.in_minimum_displacement, -0.1, parent=panel_geometry)
        sock_maximum_displacement = self._float_socket(self.in_maximum_displacement, 0.1, parent=panel_geometry)
        sock_subd_displacement_level = self._float_socket(self.in_subd_displacement_level, parent=panel_geometry)
        sock_horizontal_tiles = self._float_socket(self.in_horizontal_tiles, 1, parent=panel_geometry)
        sock_horizontal_offset = self._float_socket(self.in_horizontal_offset, parent=panel_geometry)
        sock_vertical_tiles = self._float_socket(self.in_vertical_tiles, 1, parent=panel_geometry)
        sock_vertical_offset = self._float_socket(self.in_vertical_offset, parent=panel_geometry)
        sock_cutout_opacity_horizontal_tiles = self._float_socket(self.in_cutout_opacity_horizontal_tiles, 1, parent=panel_geometry)
        sock_cutout_opacity_horizontal_offset = self._float_socket(self.in_cutout_opacity_horizontal_offset, parent=panel_geometry)
        sock_cutout_opacity_vertical_tiles = self._float_socket(self.in_cutout_opacity_vertical_tiles, 1, parent=panel_geometry)
        sock_cutout_opacity_vertical_offset = self._float_socket(self.in_cutout_opacity_vertical_offset, parent=panel_geometry)

        # Sockets: Glossy
        sock_glossy_layered_weight = self._float_socket(self.in_glossy_layered_weight, parent=panel_glossy)
        sock_glossy_layered_weight_map = self._color_socket(self.in_glossy_layered_weight_map, parent=panel_glossy)
        sock_share_glossy_inputs = self._bool_socket(self.in_share_glossy_inputs, True, parent=panel_glossy)
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

        # Sockets: Gradient Layer
        sock_gradient_layer_grazing_color = self._color_socket(self.in_gradient_layer_grazing_color, (0.0, 0.0, 0.0, 1.0), parent=panel_gradient_layer)
        sock_gradient_layer_grazing_color_map = self._color_socket(self.in_gradient_layer_grazing_color_map, parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint = self._color_socket(self.in_gradient_layer_normal_tint, (0.0, 0.0, 0.0, 1.0), parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint_map = self._color_socket(self.in_gradient_layer_normal_tint_map, parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint_weight = self._float_socket(self.in_gradient_layer_normal_tint_weight, parent=panel_gradient_layer)
        sock_gradient_layer_normal_tint_weight_map = self._color_socket(self.in_gradient_layer_normal_tint_weight_map, parent=panel_gradient_layer)
        sock_gradient_layer_normal_reflectivity = self._float_socket(self.in_gradient_layer_normal_reflectivity, parent=panel_gradient_layer)
        sock_gradient_layer_normal_reflectivity_map = self._color_socket(self.in_gradient_layer_normal_reflectivity_map, parent=panel_gradient_layer)
        sock_gradient_layer_grazing_reflectivity = self._float_socket(self.in_gradient_layer_grazing_reflectivity, 1, parent=panel_gradient_layer)
        sock_gradient_layer_grazing_reflectivity_map = self._color_socket(self.in_gradient_layer_grazing_reflectivity_map, parent=panel_gradient_layer)
        sock_gradient_layer_exponent = self._float_socket(self.in_gradient_layer_exponent, 1, parent=panel_gradient_layer)
        sock_gradient_layer_exponent_map = self._color_socket(self.in_gradient_layer_exponent_map, parent=panel_gradient_layer)
        sock_gradient_layer_strength = self._float_socket(self.in_gradient_layer_strength, 1, parent=panel_gradient_layer)
        sock_gradient_layer_metallic_weight = self._float_socket(self.in_gradient_layer_metallic_weight, parent=panel_gradient_layer)
        sock_gradient_layer_glossy_layered_weight = self._float_socket(self.in_gradient_layer_glossy_layered_weight, parent=panel_gradient_layer)
        sock_gradient_layer_refraction_index = self._float_socket(self.in_gradient_layer_refraction_index, 1, parent=panel_gradient_layer)
        sock_gradient_layer_refraction_weight = self._float_socket(self.in_gradient_layer_refraction_weight, 1, parent=panel_gradient_layer)

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

        # Sockets: Thin Film
        sock_thin_film_thickness = self._float_socket(self.in_thin_film_thickness, parent=panel_thin_film)
        sock_thin_film_thickness_map = self._color_socket(self.in_thin_film_thickness_map, parent=panel_thin_film)
        sock_thin_film_ior = self._float_socket(self.in_thin_film_ior, 1.5, parent=panel_thin_film)
        sock_thin_film_ior_map = self._color_socket(self.in_thin_film_ior_map, parent=panel_thin_film)

        # Sockets: Top Coat General
        sock_top_coat_weight = self._float_socket(self.in_top_coat_weight, parent=panel_top_coat_general)
        sock_top_coat_weight_map = self._color_socket(self.in_top_coat_weight_map, parent=panel_top_coat_general)
        sock_top_coat_color = self._color_socket(self.in_top_coat_color, parent=panel_top_coat_general)
        sock_top_coat_color_map = self._color_socket(self.in_top_coat_color_map, parent=panel_top_coat_general)
        sock_top_coat_roughness = self._float_socket(self.in_top_coat_roughness, parent=panel_top_coat_general)
        sock_top_coat_roughness_map = self._color_socket(self.in_top_coat_roughness_map, parent=panel_top_coat_general)
        sock_top_coat_reflectivity = self._float_socket(self.in_top_coat_reflectivity, 0.5, parent=panel_top_coat_general)
        sock_top_coat_reflectivity_map = self._color_socket(self.in_top_coat_reflectivity_map, parent=panel_top_coat_general)
        sock_top_coat_normal = self._float_socket(self.in_top_coat_normal, 1, parent=panel_top_coat_general)
        sock_top_coat_normal_map = self._color_socket(self.in_top_coat_normal_map, parent=panel_top_coat_general)
        sock_top_coat_bump = self._float_socket(self.in_top_coat_bump, 1, parent=panel_top_coat_general)
        sock_top_coat_bump_map = self._color_socket(self.in_top_coat_bump_map, parent=panel_top_coat_general)
        sock_top_coat_anisotropy = self._float_socket(self.in_top_coat_anisotropy, parent=panel_top_coat_general)
        sock_top_coat_anisotropy_map = self._color_socket(self.in_top_coat_anisotropy_map, parent=panel_top_coat_general)
        sock_top_coat_rotations = self._float_socket(self.in_top_coat_rotations, parent=panel_top_coat_general)
        sock_top_coat_rotations_map = self._color_socket(self.in_top_coat_rotations_map, parent=panel_top_coat_general)

        # Output Sockets:
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")
        sock_out_volume = self._shader_socket(self.out_volume, in_out="OUTPUT")
        sock_out_displacement = self._vector_socket(self.out_displacement, in_out="OUTPUT")
        # @formatter:on


class IWaveTranslucentFabricShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        # @formatter:off
        # in_diffuse
        # in_diffuse_map

#         in_normal_map
#         in_normal_map_map
#         in_crumple_normal_map
#         in_crumple_normal_map_map

#         in_fiber_layer_weight
#         in_fiber_layer_weight_map
#         in_metallic_weight
#         in_metallic_weight_map
#         in_diffuse_overlay_color
#         in_diffuse_overlay_color_map
#         in_diffuse_roughness
#         in_diffuse_roughness_map
#         in_translucency_weight
#         in_translucency_weight_map
#         in_translucency_color
#         in_translucency_color_map
#         in_fiber_layer_weight_map_horizontal_tiles
#         in_fiber_layer_weight_map_horizontal_offset
#         in_fiber_layer_weight_map_vertical_tiles
#         in_fiber_layer_weight_map_vertical_offset

#         in_fine_detail_blend_weight
#         in_fine_detail_map
#         in_fine_detail_blend_mode
#         in_fine_detail_glossy_reflectivity
#         in_fine_detail_glossy_reflectivity_map
#         in_fine_detail_normal_map
#         in_fine_detail_normal_map_map
#         in_fine_detail_and_crumple_normal
#         in_fine_detail_and_crumple_normal_map
#         in_fine_detail_and_crumple_bump
#         in_fine_detail_and_crumple_bump_map
#         in_fine_detail_horizontal_tiles
#         in_fine_detail_horizontal_offset
#         in_fine_detail_vertical_tiles
#         in_fine_detail_vertical_offset

#         in_cutout_opacity
#         in_cutout_opacity_map
#         in_displacement_strength
#         in_displacement_strength_map
#         in_minimum_displacement
#         in_maximum_displacement
#         in_subd_displacement_level
#         in_horizontal_tiles
#         in_horizontal_offset
#         in_vertical_tiles
#         in_vertical_offset
#         in_cutout_opacity_horizontal_tiles
#         in_cutout_opacity_horizontal_offset
#         in_cutout_opacity_vertical_tiles
#         in_cutout_opacity_vertical_offset

#         in_glossy_layered_weight
#         in_glossy_layered_weight_map
#         in_share_glossy_inputs
#         in_glossy_color
#         in_glossy_color_map
#         in_glossy_reflectivity
#         in_glossy_reflectivity_map
#         in_glossy_roughness
#         in_glossy_roughness_map
#         in_glossy_anisotropy
#         in_glossy_anisotropy_map
#         in_glossy_anisotropy_rotations
#         in_glossy_anisotropy_rotations_map

#         in_gradient_layer_grazing_color
#         in_gradient_layer_grazing_color_map
#         in_gradient_layer_normal_tint
#         in_gradient_layer_normal_tint_map
#         in_gradient_layer_normal_tint_weight
#         in_gradient_layer_normal_tint_weight_map
#         in_gradient_layer_normal_reflectivity
#         in_gradient_layer_normal_reflectivity_map
#         in_gradient_layer_grazing_reflectivity
#         in_gradient_layer_grazing_reflectivity_map
#         in_gradient_layer_exponent
#         in_gradient_layer_exponent_map
#         in_gradient_layer_strength
#         in_gradient_layer_metallic_weight
#         in_gradient_layer_glossy_layered_weight
#         in_gradient_layer_refraction_index
#         in_gradient_layer_refraction_weight

#         in_metallic_flakes_weight
#         in_metallic_flakes_weight_map
#         in_metallic_flakes_color
#         in_metallic_flakes_color_map
#         in_metallic_flakes_roughness
#         in_metallic_flakes_roughness_map
#         in_metallic_flakes_size
#         in_metallic_flakes_strength
#         in_metallic_flakes_density

#         in_thin_film_thickness
#         in_thin_film_thickness_map
#         in_thin_film_ior
#         in_thin_film_ior_map

#         in_top_coat_weight
#         in_top_coat_weight_map
#         in_top_coat_color
#         in_top_coat_color_map
#         in_top_coat_roughness
#         in_top_coat_roughness_map
#         in_top_coat_reflectivity
#         in_top_coat_reflectivity_map
#         in_top_coat_normal
#         in_top_coat_normal_map
#         in_top_coat_bump
#         in_top_coat_bump_map
#         in_top_coat_anisotropy
#         in_top_coat_anisotropy_map
#         in_top_coat_rotations
#         in_top_coat_rotations_map
        # @formatter:off

