from bpy.types import ShaderNodeMapping

from .support import ShaderGroupApplier, ShaderGroupBuilder

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

    in_fine_detail_glossy_reflectivity = "Fine Detail Glossy Reflectivity"
    in_fine_detail_glossy_reflectivity_map = "Fine Detail Glossy Reflectivity Map"
    in_fine_detail_normal = "Fine Detail Normal"
    in_fine_detail_normal_map = "Fine Detail Normal Map"
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
    in_glossy_color = "Glossy Color"
    in_glossy_color_map = "Glossy Color Map"
    in_glossy_reflectivity = "Glossy Reflectivity"
    in_glossy_reflectivity_map = "Glossy Reflectivity Map"
    in_glossy_roughness = "Glossy Roughness"
    in_glossy_roughness_map = "Glossy Roughness Map"

    in_gradient_layer_normal_opacity = "Gradient Layer Normal Opacity"
    in_gradient_layer_normal_opacity_map = "Gradient Layer Normal Opacity Map"
    in_gradient_layer_grazing_opacity = "Gradient Layer Grazing Opacity"
    in_gradient_layer_grazing_opacity_map = "Gradient Layer Grazing Opacity Map"
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
        sock_normal = self._float_socket(self.in_base_normal, 1, parent=panel_bump)
        sock_normal_map = self._color_socket(self.in_base_normal_map, parent=panel_bump)
        sock_bump = self._float_socket(self.in_base_bump, 1, parent=panel_bump)
        sock_bump_map = self._color_socket(self.in_base_bump_map, parent=panel_bump)

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

        # Sockets: Fine Detail
        sock_fine_detail_glossy_reflectivity = self._float_socket(self.in_fine_detail_glossy_reflectivity, 0.5, parent=panel_fine_detail)
        sock_fine_detail_glossy_reflectivity_map = self._color_socket(self.in_fine_detail_glossy_reflectivity_map, parent=panel_fine_detail)
        sock_fine_detail_normal_map = self._float_socket(self.in_fine_detail_normal_map, 1, parent=panel_fine_detail)
        sock_fine_detail_horizontal_tiles = self._float_socket(self.in_fine_detail_horizontal_tiles, 1, parent=panel_fine_detail)
        sock_fine_detail_horizontal_offset = self._float_socket(self.in_fine_detail_horizontal_offset, parent=panel_fine_detail)
        sock_fine_detail_vertical_tiles = self._float_socket(self.in_fine_detail_vertical_tiles, 1, parent=panel_fine_detail)
        sock_fine_detail_vertical_offset = self._float_socket(self.in_fine_detail_vertical_offset, parent=panel_fine_detail)

        # Sockets: Geometry
        sock_cutout_opacity = self._float_socket(self.in_cutout_opacity, 1, parent=panel_geometry)
        sock_cutout_opacity_map = self._color_socket(self.in_cutout_opacity_map, parent=panel_geometry)
        sock_displacement_strength = self._float_socket(self.in_displacement_strength, 1, parent=panel_geometry)
        sock_displacement_strength_map = self._color_socket(self.in_displacement_strength_map, parent=panel_geometry)
        sock_minimum_displacement = self._float_socket(self.in_minimum_displacement, -0.1, parent=panel_geometry)
        sock_maximum_displacement = self._float_socket(self.in_maximum_displacement, 0.1, parent=panel_geometry)
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
        sock_glossy_color = self._color_socket(self.in_glossy_color, parent=panel_glossy)
        sock_glossy_color_map = self._color_socket(self.in_glossy_color_map, parent=panel_glossy)
        sock_glossy_reflectivity = self._float_socket(self.in_glossy_reflectivity, 0.5, parent=panel_glossy)
        sock_glossy_reflectivity_map = self._color_socket(self.in_glossy_reflectivity_map, parent=panel_glossy)
        sock_glossy_roughness = self._float_socket(self.in_glossy_roughness, parent=panel_glossy)
        sock_glossy_roughness_map = self._color_socket(self.in_glossy_roughness_map, parent=panel_glossy)

        # Sockets: Gradient Layer
        sock_gradient_layer_normal_opacity = self._float_socket(self.in_gradient_layer_normal_opacity, parent=panel_gradient_layer)
        sock_gradient_layer_normal_opacity_map = self._color_socket(self.in_gradient_layer_normal_opacity_map, parent=panel_gradient_layer)
        sock_gradient_layer_grazing_opacity = self._float_socket(self.in_gradient_layer_grazing_opacity, 1, parent=panel_gradient_layer)
        sock_gradient_layer_grazing_opacity_map = self._color_socket(self.in_gradient_layer_grazing_opacity_map, parent=panel_gradient_layer)
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

        geo_mapping_props = ["horizontal_tiles", "horizontal_offset", "vertical_tiles", "vertical_offset"]
        if self._channel_enabled(*geo_mapping_props):
            self._set_material_mapping(*geo_mapping_props)

        # Bump
        self._channel_to_inputs("normal_map", builder.in_base_normal, builder.in_base_normal_map)
        self._channel_to_inputs("bump_strength", builder.in_base_bump, builder.in_base_bump_map)

        # Fiber Layer
        if self._channel_enabled("fiber_layer_weight"):
            self._channel_to_inputs("metallic_weight", builder.in_metallic_weight, builder.in_metallic_weight_map)
            self._channel_to_inputs("diffuse_overlay_color", builder.in_diffuse_overlay_color, builder.in_diffuse_overlay_color_map)
            self._channel_to_inputs("diffuse_roughness", builder.in_diffuse_roughness, builder.in_diffuse_roughness_map)
            self._channel_to_inputs("translucency_weight", builder.in_translucency_weight, builder.in_translucency_weight_map)
            self._channel_to_inputs("translucency_color", builder.in_translucency_color, builder.in_translucency_color_map)

        # Fine Detail
        node_fd_glossy_tex = self._channel_to_inputs("fine_detail_normal_map", builder.in_fine_detail_normal, builder.in_fine_detail_normal_map)
        node_fd_normal_tex = self._channel_to_inputs("fine_detail_glossy_reflectivity", builder.in_fine_detail_glossy_reflectivity, builder.in_fine_detail_glossy_reflectivity_map)

        fd_mapping_props = ["fine_detail_horizontal_tiles", "fine_detail_horizontal_offset", "fine_detail_vertical_tiles", "fine_detail_vertical_offset"]
        if self._channel_enabled(*fd_mapping_props) and (node_fd_normal_tex or node_fd_glossy_tex):
            fd_mapping_node_loc = tuple_zip_sum((0, self.mapping_node_location_offset), self._mapping.location.to_tuple())
            fd_mapping_node = self._add_node(ShaderNodeMapping, "Fine Detail Mapping", fd_mapping_node_loc, props={"vector_type": "POINT", "hide": True})
            self._link_socket(self._uv_map, fd_mapping_node, 0, 0)
            self._set_material_mapping(*fd_mapping_props, mapping_node=fd_mapping_node)

            if node_fd_glossy_tex:
                self._link_socket(fd_mapping_node, node_fd_glossy_tex, 0, 0)
            if node_fd_normal_tex:
                self._link_socket(fd_mapping_node, node_fd_normal_tex, 0, 0)

        # Geometry
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

        # Thin Film
        self._channel_to_inputs("thin_film_thickness", builder.in_thin_film_thickness, builder.in_thin_film_thickness_map)
        self._channel_to_inputs("thin_film_ior", builder.in_thin_film_ior, builder.in_thin_film_ior_map)

            # Top Coat General
        if self._channel_enabled("top_coat_weight"):
            self._channel_to_inputs("top_coat_weight", builder.in_top_coat_weight, builder.in_top_coat_weight_map)
            self._channel_to_inputs("top_coat_color", builder.in_top_coat_color, builder.in_top_coat_color_map)
            self._channel_to_inputs("top_coat_roughness", builder.in_top_coat_roughness, builder.in_top_coat_roughness_map)
            self._channel_to_inputs("top_coat_reflectivity", builder.in_top_coat_reflectivity, builder.in_top_coat_reflectivity_map)
            self._channel_to_inputs("top_coat_anisotropy", builder.in_top_coat_anisotropy, builder.in_top_coat_anisotropy_map)
            self._channel_to_inputs("top_coat_rotations", builder.in_top_coat_rotations, builder.in_top_coat_anisotropy_map)

        if self._channel_enabled("top_coat_bump_mode"):
            self._channel_to_inputs("top_coat_bump", builder.in_top_coat_bump, builder.in_top_coat_bump_map)
        else:
            self._channel_to_inputs("top_coat_normal", builder.in_top_coat_normal, builder.in_top_coat_normal_map)
        # @formatter:off

