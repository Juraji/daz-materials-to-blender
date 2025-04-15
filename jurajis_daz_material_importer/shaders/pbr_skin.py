import bpy

from .dls import DualLobeSpecularShaderGroupBuilder
from .material_shader import ShaderGroupBuilder, ShaderGroupApplier

__GROUP_NAME__ = "DAZ PBR Skin"


class PBRSkinShaderGroupBuilder(ShaderGroupBuilder):
    in_diffuse_color = "Diffuse Color"
    in_diffuse_color_map = "Diffuse Color Map"
    in_roughness_weight = "Roughness Weight"
    in_roughness_weight_map = "Roughness Weight Map"
    in_metallic_weight = "Metallic Weight"
    in_metallic_weight_map = "Metallic Weight Map"
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

    in_normal_mult = "Normal"
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

    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def setup_group(self):
        super().setup_group()

        # Panels
        panel_pbr = self.add_panel("PBR", default_closed=False)
        panel_dls = self.add_panel("Dual Lobe Specular")
        panel_sss = self.add_panel("Sub Surface Scattering")
        panel_normals_bump = self.add_panel("Normals and Bump")
        panel_top_coat = self.add_panel("Top Coat")
        panel_makeup = self.add_panel("Makeup")

        # Input Sockets: PBR
        sock_diffuse_color = self.color_socket(self.in_diffuse_color, parent=panel_pbr)
        sock_diffuse_color_map = self.color_socket(self.in_diffuse_color_map, parent=panel_pbr)
        sock_roughness_weight = self.float_socket(self.in_roughness_weight, 1.0, parent=panel_pbr)
        in_roughness_weight_map = self.color_socket(self.in_roughness_weight_map, parent=panel_pbr)
        sock_metallic_weight = self.float_socket(self.in_metallic_weight, parent=panel_pbr)
        sock_metallic_weight_map = self.color_socket(self.in_metallic_weight_map, parent=panel_pbr)
        sock_opacity = self.float_socket(self.in_opacity, 1.0, parent=panel_pbr)
        sock_opacity_map = self.color_socket(self.in_opacity_map, parent=panel_pbr)

        # Input Sockets: DLS
        sock_dls_weight = self.float_socket(self.in_dls_weight, parent=panel_dls)
        sock_dls_weight_map = self.color_socket(self.in_dls_weight_map, parent=panel_dls)
        sock_dls_reflectivity = self.float_socket(self.in_dls_reflectivity, 0.5, parent=panel_dls)
        sock_dls_reflectivity_map = self.color_socket(self.in_dls_reflectivity_map, parent=panel_dls)
        sock_dls_roughness_mult = self.float_socket(self.in_dls_roughness_mult, 1.0, parent=panel_dls)
        sock_dls_l1_roughness = self.float_socket(self.in_dls_l1_roughness, 0.6, parent=panel_dls)
        sock_dls_l1_roughness_map = self.color_socket(self.in_dls_l1_roughness_map, parent=panel_dls)
        sock_dls_l2_roughness_mult = self.float_socket(self.in_dls_l2_roughness_mult, 0.4, parent=panel_dls)
        sock_dls_l2_roughness_mult_map = self.color_socket(self.in_dls_l2_roughness_mult_map, parent=panel_dls)
        sock_dls_ratio = self.float_socket(self.in_dls_ratio, 0.15, parent=panel_dls)
        sock_dls_ratio_map = self.color_socket(self.in_dls_ratio_map, parent=panel_dls)

        # Input Sockets: SSS
        sock_sss_weight = self.float_socket(self.in_sss_weight, 0.8, parent=panel_sss)
        sock_sss_radius = self.vector_socket(self.in_sss_radius, (1.0, 0.2, 0.1), parent=panel_sss)
        sock_sss_scale = self.float_socket(self.in_sss_scale, 0.004, parent=panel_sss, props={"subtype": "DISTANCE"})
        sock_sss_direction = self.float_socket(self.in_sss_direction, 0.8, parent=panel_sss)

        # Input Sockets: Normal/Bump
        sock_normal_mult = self.float_socket(self.in_normal_mult, 1.0, parent=panel_normals_bump)
        sock_normal_map = self.color_socket(self.in_normal_map, (0.5, 0.5, 1.0, 1.0), parent=panel_normals_bump)
        sock_detail_weight = self.float_socket(self.in_detail_weight, parent=panel_normals_bump)
        sock_detail_weight_map = self.color_socket(self.in_detail_weight_map, parent=panel_normals_bump)
        sock_detail_normal_map = self.color_socket(self.in_detail_normal_map, (0.5, 0.5, 1.0, 1.0),
                                                   parent=panel_normals_bump)
        sock_bump_strength = self.float_socket(self.in_bump_strength, parent=panel_normals_bump)
        sock_bump_strength_map = self.color_socket(self.in_bump_strength_map, parent=panel_normals_bump)

        # Input Sockets: Top Coat
        sock_top_coat_weight = self.float_socket(self.in_top_coat_weight, parent=panel_top_coat)
        sock_top_coat_weight_map = self.color_socket(self.in_top_coat_weight_map, parent=panel_top_coat)
        sock_top_coat_roughness = self.float_socket(self.in_top_coat_roughness, 0.7, parent=panel_top_coat)
        sock_top_coat_roughness_map = self.color_socket(self.in_top_coat_roughness_map, parent=panel_top_coat)
        sock_top_coat_color = self.color_socket(self.in_top_coat_color, parent=panel_top_coat)
        sock_top_coat_color_map = self.color_socket(self.in_top_coat_color_map, parent=panel_top_coat)

        # Input Sockets: Makeup
        sock_makeup_weight = self.float_socket(self.in_makeup_weight, parent=panel_makeup)
        sock_makeup_weight_map = self.color_socket(self.in_makeup_weight_map, parent=panel_makeup)
        sock_makeup_base_color = self.color_socket(self.in_makeup_base_color, parent=panel_makeup)
        sock_makeup_base_color_map = self.color_socket(self.in_makeup_base_color_map, parent=panel_makeup)
        sock_makeup_roughness_mult = self.float_socket(self.in_makeup_roughness_mult, parent=panel_makeup)
        sock_makeup_roughness_mult_map = self.color_socket(self.in_makeup_roughness_mult_map, parent=panel_makeup)
        sock_makeup_metallic_weight = self.float_socket(self.in_makeup_metallic_weight, parent=panel_makeup)
        sock_makeup_metallic_weight_map = self.color_socket(self.in_makeup_metallic_weight_map, parent=panel_makeup)
        sock_makeup_reduce_normals = self.float_socket(self.in_makeup_reduce_normals, parent=panel_makeup)

        # Output Sockets:
        sock_out_surface = self.shader_socket(self.out_surface, in_out="OUTPUT")

        # Frames
        frame_pbr = self.add_frame("PBR and Opacity", (-210, 601))
        frame_normal_and_bump = self.add_frame("Normal, Detail and Bump", (-188, -302))
        frame_top_coat = self.add_frame("Top Coat", (5, -814))
        frame_makeup_layer = self.add_frame("Makeup Layer", (-1, -1326))

        # Nodes: Group Input
        node_group_input = self.add_node__group_input("Group Input", (-1045, -90))

        # Nodes: PBR
        node_combine_diffuse = self.add_node__mix("Combine diffuse", (-158, -39), parent=frame_pbr)
        self.link_socket(node_group_input, node_combine_diffuse, sock_diffuse_color_map, 6)
        self.link_socket(node_group_input, node_combine_diffuse, sock_diffuse_color, 7)

        node_combine_roughness = self.add_node__hsv("Combine Roughness", (28, -39), frame_pbr)
        self.link_socket(node_group_input, node_combine_roughness, sock_roughness_weight, 2)
        self.link_socket(node_group_input, node_combine_roughness, in_roughness_weight_map, 4)

        node_combine_metallic = self.add_node__hsv("Combine Metallic", (240, -39), frame_pbr)
        self.link_socket(node_group_input, node_combine_metallic, sock_metallic_weight, 2)
        self.link_socket(node_group_input, node_combine_metallic, sock_metallic_weight_map, 4)

        node_combine_opacity = self.add_node__hsv("Combine Opacity", (446, -43), frame_pbr)
        self.link_socket(node_group_input, node_combine_opacity, sock_opacity, 2)
        self.link_socket(node_group_input, node_combine_opacity, sock_opacity_map, 4)

        # Nodes: Normal/Bump
        node_normal_map = self.add_node__normal_map("Normal Map", (248, -88), frame_normal_and_bump)
        self.link_socket(node_group_input, node_normal_map, sock_normal_mult, 0)
        self.link_socket(node_group_input, node_normal_map, sock_normal_map, 1)

        node_combine_detail_weight = self.add_node__hsv(
            "Combine Detail Weight", (28, -240), frame_normal_and_bump)
        self.link_socket(node_group_input, node_combine_detail_weight, sock_detail_weight, 2)
        self.link_socket(node_group_input, node_combine_detail_weight, sock_detail_weight_map, 4)

        node_detail_normal_map = self.add_node__normal_map(
            "Detail Normal Map", (247, -266), frame_normal_and_bump)
        self.link_socket(node_combine_detail_weight, node_detail_normal_map, 0, 0)
        self.link_socket(node_group_input, node_detail_normal_map, sock_detail_normal_map, 1)

        node_combine_normal_and_detail_vectors = self.add_node__math_vector(
            "Combine normal and detail vectors", (458, -151), frame_normal_and_bump, {"operation": "ADD"})
        self.link_socket(node_normal_map, node_combine_normal_and_detail_vectors, 0, 0)
        self.link_socket(node_detail_normal_map, node_combine_normal_and_detail_vectors, 0, 1)

        node_bump_map = self.add_node__bump("Bump map", (683, -39), frame_normal_and_bump)
        self.link_socket(node_group_input, node_bump_map, sock_bump_strength, 0)
        self.link_socket(node_group_input, node_bump_map, sock_bump_strength_map, 2)
        self.link_socket(node_combine_normal_and_detail_vectors, node_bump_map, 0, 3)

        # Nodes: Top Coat
        node_combine_top_coat_weight = self.add_node__hsv(
            "Combine Top Coat Weight", (36, -44), frame_top_coat)
        self.link_socket(node_group_input, node_combine_top_coat_weight, sock_top_coat_weight, 2)
        self.link_socket(node_group_input, node_combine_top_coat_weight, sock_top_coat_weight_map, 4)

        node_combine_top_coat_roughness = self.add_node__hsv(
            "Combine Top Coat Roughness", (232, -39), frame_top_coat)
        self.link_socket(node_group_input, node_combine_top_coat_roughness, sock_top_coat_roughness, 2)
        self.link_socket(node_group_input, node_combine_top_coat_roughness, sock_top_coat_roughness_map, 4)

        node_combine_top_coat_color = self.add_node__mix(
            "Combine Top Coat Color", (31, -240), parent=frame_top_coat)
        self.link_socket(node_group_input, node_combine_top_coat_color, sock_top_coat_color_map, 6)
        self.link_socket(node_group_input, node_combine_top_coat_color, sock_top_coat_color, 7)

        # Nodes: Base Layer BDSF
        node_base_layer_bdsf = self.add_node__princ_bdsf(
            "Base Layer BDSF", (776, 0), props={"subsurface_method": "RANDOM_WALK_SKIN"})
        self.link_socket(node_combine_diffuse, node_base_layer_bdsf, 2, 0)
        self.link_socket(node_combine_metallic, node_base_layer_bdsf, 0, 1)
        self.link_socket(node_combine_roughness, node_base_layer_bdsf, 0, 2)
        self.link_socket(node_combine_opacity, node_base_layer_bdsf, 0, 4)
        self.link_socket(node_bump_map, node_base_layer_bdsf, 0, 5)
        self.link_socket(node_group_input, node_base_layer_bdsf, sock_sss_weight, 8)
        self.link_socket(node_group_input, node_base_layer_bdsf, sock_sss_radius, 9)
        self.link_socket(node_group_input, node_base_layer_bdsf, sock_sss_scale, 10)
        self.link_socket(node_group_input, node_base_layer_bdsf, sock_sss_direction, 12)
        self.link_socket(node_combine_top_coat_weight, node_base_layer_bdsf, 0, 19)
        self.link_socket(node_combine_top_coat_roughness, node_base_layer_bdsf, 0, 20)
        self.link_socket(node_combine_top_coat_color, node_base_layer_bdsf, 2, 22)
        self.link_socket(node_bump_map, node_base_layer_bdsf, 0, 23)

        # Nodes: Dual Lobe Specular Layer
        dls_builder = DualLobeSpecularShaderGroupBuilder
        node_dls_group = self.add_node_shader_group("DLS", (18, 218), props={
            "width": 400,
            "node_tree": bpy.data.node_groups[dls_builder.group_name()]
        })
        self.link_socket(node_group_input, node_dls_group, sock_dls_weight, dls_builder.in_weight)
        self.link_socket(node_group_input, node_dls_group, sock_dls_weight_map, dls_builder.in_weight_map)
        self.link_socket(node_group_input, node_dls_group, sock_dls_reflectivity, dls_builder.in_reflectivity)
        self.link_socket(node_group_input, node_dls_group, sock_dls_reflectivity_map, dls_builder.in_reflectivity_map)
        self.link_socket(node_group_input, node_dls_group, sock_dls_roughness_mult, dls_builder.in_roughness_mult)
        self.link_socket(node_group_input, node_dls_group, sock_dls_l1_roughness, dls_builder.in_l1_roughness)
        self.link_socket(node_group_input, node_dls_group, sock_dls_l1_roughness_map, dls_builder.in_l1_roughness_map)
        self.link_socket(node_group_input, node_dls_group, sock_dls_l2_roughness_mult, dls_builder.in_l2_roughness_mult)
        self.link_socket(node_group_input, node_dls_group, sock_dls_l2_roughness_mult_map, dls_builder.in_l2_roughness_mult_map)
        self.link_socket(node_group_input, node_dls_group, sock_dls_ratio, dls_builder.in_ratio)
        self.link_socket(node_group_input, node_dls_group, sock_dls_ratio_map, dls_builder.in_ratio_map)
        self.link_socket(node_bump_map, node_dls_group, 0, dls_builder.in_normal)

        # Nodes: Makeup Layer
        node_combine_makeup_weight = self.add_node__hsv("Combine Makeup Weight", (29, -39), frame_makeup_layer)
        self.link_socket(node_group_input, node_combine_makeup_weight, sock_makeup_weight, 2)
        self.link_socket(node_group_input, node_combine_makeup_weight, sock_makeup_weight_map, 4)

        node_combine_makeup_base_color = self.add_node__mix(
            "Combine Makeup Base Color", (33, -222), parent=frame_makeup_layer)
        self.link_socket(node_group_input, node_combine_makeup_base_color, sock_makeup_base_color, 6)
        self.link_socket(node_group_input, node_combine_makeup_base_color, sock_makeup_base_color_map, 7)

        node_combine_makeup_roughness_mult = self.add_node__hsv(
            "Combine Makeup Roughness Mult", (32, -449), frame_makeup_layer)
        self.link_socket(node_group_input, node_combine_makeup_roughness_mult, sock_makeup_roughness_mult, 2)
        self.link_socket(node_group_input, node_combine_makeup_roughness_mult, sock_makeup_roughness_mult_map, 4)

        node_combine_makeup_metalic_weight = self.add_node__hsv(
            "Combine Makeup Metalic Weight", (38, -629), frame_makeup_layer)
        self.link_socket(node_group_input, node_combine_makeup_metalic_weight, sock_makeup_metallic_weight, 2)
        self.link_socket(node_group_input, node_combine_makeup_metalic_weight, sock_makeup_metallic_weight_map, 4)

        node_combine_diff_dls_roughness_for_makeup = self.add_node__mix(
            "Combine Diffuse and DLS Roughness Maps for Makeup", (307, -131), parent=frame_makeup_layer)
        self.link_socket(node_combine_roughness, node_combine_diff_dls_roughness_for_makeup, 0, 6)
        self.link_socket(node_group_input, node_combine_diff_dls_roughness_for_makeup, sock_dls_l1_roughness_map,
                         7)

        node_multiply_makeup_base_roughness = self.add_node__mix(
            "Multiply Makeup Base Roughness", (543, -135), parent=frame_makeup_layer)
        self.link_socket(node_combine_diff_dls_roughness_for_makeup, node_multiply_makeup_base_roughness, 2, 6)
        self.link_socket(node_combine_makeup_roughness_mult, node_multiply_makeup_base_roughness, 0, 7)

        node_makeup_normal_interpolation_base_value = self.add_node__normal_map(
            "Makeup Normal Interpolation Base Value", (384, -617), frame_makeup_layer)

        node_interpolate_makeup_normal = self.add_node__mix(
            "Interpolate Makeup Normal", (615, -407), data_type="VECTOR", parent=frame_makeup_layer)
        self.link_socket(node_group_input, node_interpolate_makeup_normal, sock_makeup_reduce_normals, 0)
        self.link_socket(node_bump_map, node_interpolate_makeup_normal, 0, 4)
        self.link_socket(node_makeup_normal_interpolation_base_value, node_interpolate_makeup_normal, 0, 5)

        node_makeup_layer_bsdf = self.add_node__princ_bdsf("Makeup Layer BSDF", (811, -201), frame_makeup_layer)
        self.link_socket(node_combine_makeup_base_color, node_makeup_layer_bsdf, 2, 0)
        self.link_socket(node_combine_makeup_metalic_weight, node_makeup_layer_bsdf, 0, 1)
        self.link_socket(node_multiply_makeup_base_roughness, node_makeup_layer_bsdf, 2, 2)
        self.link_socket(node_interpolate_makeup_normal, node_makeup_layer_bsdf, 1, 5)

        # Nodes: Mix Layers
        node_mix_makeup_shader = self.add_node__mix_shader("Mix Makeup Shader", (1141, -85))
        self.link_socket(node_combine_makeup_weight, node_mix_makeup_shader, 0, 0)
        self.link_socket(node_base_layer_bdsf, node_mix_makeup_shader, 0, 1)
        self.link_socket(node_makeup_layer_bsdf, node_mix_makeup_shader, 0, 2)

        node_mix_dls_shader = self.add_node__mix_shader("Mix DLS Shader", (1348, 52))
        self.link_socket(node_dls_group, node_mix_dls_shader, 0, 0)
        self.link_socket(node_mix_makeup_shader, node_mix_dls_shader, 0, 1)
        self.link_socket(node_dls_group, node_mix_dls_shader, 1, 2)

        # Group Output
        node_group_output = self.add_node__group_output("NodeGroupOutput", (1612, 9))
        self.link_socket(node_mix_dls_shader, node_group_output, 0, sock_out_surface)


class PBRSkinShaderGroupApplier(ShaderGroupApplier):
    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def add_shader_group(self, location: tuple[float, float], channels: dict):
        super().add_shader_group(location, channels)

        builder = PBRSkinShaderGroupBuilder

        if 'Diffuse' in channels:
            self.set_socket(self.shader_group_node, builder.in_diffuse_color, channels['Diffuse']['value'])
            if channels['Diffuse']['image_file'] is not None:
                node_image_texture = self.add_image_texture(channels['Diffuse']['image_file'], False)
                self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_diffuse_color_map)

        if 'Diffuse_Roughness' in channels:
            diffuse_roughness = channels['Diffuse_Roughness']['value']
            if diffuse_roughness != 0:
                self.set_socket(self.shader_group_node, builder.in_roughness_weight, diffuse_roughness)
                if channels['Diffuse_Roughness']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Diffuse_Roughness']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_roughness_weight_map)

        if 'Metallic_Weight' in channels:
            self.set_socket(self.shader_group_node, builder.in_metallic_weight, channels['Metallic_Weight']['value'])
            if channels['Metallic_Weight']['image_file'] is not None:
                node_image_texture = self.add_image_texture(channels['Metallic_Weight']['image_file'], True)
                self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_metallic_weight_map)

        if 'Cutout_Opacity' in channels:
            self.set_socket(self.shader_group_node, builder.in_opacity, channels['Cutout_Opacity']['value'])
            if channels['Cutout_Opacity']['image_file'] is not None:
                node_image_texture = self.add_image_texture(channels['Cutout_Opacity']['image_file'], True)
                self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_opacity_map)

        if 'Dual_Lobe_Specular_Enable' in channels and channels['Dual_Lobe_Specular_Enable']['value']:
            if 'Dual_Lobe_Specular_Weight' in channels:
                self.set_socket(self.shader_group_node, builder.in_dls_weight,
                                channels['Dual_Lobe_Specular_Weight']['value'])
                if channels['Dual_Lobe_Specular_Weight']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Dual_Lobe_Specular_Weight']['image_file'],
                                                                True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_dls_weight_map)

            if 'Dual_Lobe_Specular_Reflectivity' in channels:
                self.set_socket(self.shader_group_node, builder.in_dls_reflectivity,
                                channels['Dual_Lobe_Specular_Reflectivity']['value'])
                if channels['Dual_Lobe_Specular_Reflectivity']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(
                        channels['Dual_Lobe_Specular_Reflectivity']['image_file'], True, 1)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_dls_reflectivity_map)

            if 'Dual_Lobe_Specular_Roughness_Mult' in channels:
                self.set_socket(self.shader_group_node, builder.in_dls_roughness_mult,
                                channels['Dual_Lobe_Specular_Roughness_Mult']['value'])

            if 'Specular_Lobe_1_Roughness' in channels:
                self.set_socket(self.shader_group_node, builder.in_dls_l1_roughness,
                                channels['Specular_Lobe_1_Roughness']['value'])
                if channels['Specular_Lobe_1_Roughness']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Specular_Lobe_1_Roughness']['image_file'],
                                                                True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_dls_l1_roughness_map)

            if 'Specular_Lobe_2_Roughness_Mult' in channels:
                self.set_socket(self.shader_group_node, builder.in_dls_l2_roughness_mult,
                                channels['Specular_Lobe_2_Roughness_Mult']['value'])
                if channels['Specular_Lobe_2_Roughness_Mult']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(
                        channels['Specular_Lobe_2_Roughness_Mult']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0,
                                     builder.in_dls_l2_roughness_mult_map)

            if 'Dual_Lobe_Specular_Ratio' in channels:
                self.set_socket(self.shader_group_node, builder.in_dls_ratio,
                                channels['Dual_Lobe_Specular_Ratio']['value'])
                if channels['Dual_Lobe_Specular_Ratio']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Dual_Lobe_Specular_Ratio']['image_file'],
                                                                True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_dls_ratio_map)

        if 'Sub_Surface_Enable' in channels and channels['Sub_Surface_Enable']['value']:
            if 'Translucency_Weight' in channels:
                self.set_socket(self.shader_group_node, builder.in_sss_weight, channels['Translucency_Weight']['value'])
            if 'SSS_Color' in channels:
                # It's a color, but we need the rgb vector, just omit alpha
                self.set_socket(self.shader_group_node, builder.in_sss_radius, channels['SSS_Color']['value'][:3])
            if 'SSS Direction' in channels:
                # DAZ Value is negative, we need positive
                self.set_socket(self.shader_group_node, builder.in_sss_direction,
                                abs(channels['SSS Direction']['value']))

        if 'Normal_Map' in channels:
            normal_mult = channels['Normal_Map']['value'] * self.properties.normal_factor
            self.set_socket(self.shader_group_node, builder.in_normal_mult, normal_mult)
            if channels['Normal_Map']['image_file'] is not None:
                node_image_texture = self.add_image_texture(channels['Normal_Map']['image_file'], True)
                self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_normal_map)

        if 'Detail_Enable' in channels and channels['Detail_Enable']['value']:
            if 'Detail_Weight' in channels:
                self.set_socket(self.shader_group_node, builder.in_detail_weight, channels['Detail_Weight']['value'])
                if channels['Detail_Weight']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Detail_Weight']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_detail_weight_map)
            if 'Detail_Normal_Map' in channels:
                normal_mult = channels['Detail_Normal_Map']['value'] * self.properties.normal_factor
                self.set_socket(self.shader_group_node, builder.in_normal_mult, normal_mult)
                if channels['Detail_Normal_Map']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Detail_Normal_Map']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_detail_normal_map)

        if 'Bump_Enable' in channels and channels['Bump_Enable']['value']:
            if 'Bump_Strength' in channels:
                self.set_socket(self.shader_group_node, builder.in_bump_strength, channels['Bump_Strength']['value'])
                if channels['Bump_Strength']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Bump_Strength']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_bump_strength_map)

        if 'Top_Coat_Enable' in channels and channels['Top_Coat_Enable']['value']:
            if 'Top_Coat_Weight' in channels:
                self.set_socket(self.shader_group_node, builder.in_top_coat_weight,
                                channels['Top_Coat_Weight']['value'])
                if channels['Top_Coat_Weight']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Top_Coat_Weight']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_top_coat_weight_map)

            if 'Top_Coat_Roughness' in channels:
                self.set_socket(self.shader_group_node, builder.in_top_coat_roughness,
                                channels['Top_Coat_Roughness']['value'])
                if channels['Top_Coat_Roughness']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Top_Coat_Roughness']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_top_coat_roughness_map)

            if 'Top_Coat_Color' in channels:
                self.set_socket(self.shader_group_node, builder.in_top_coat_color, channels['Top_Coat_Color']['value'])
                if channels['Top_Coat_Color']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Top_Coat_Color']['image_file'], False)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_top_coat_color_map)

        if 'Makeup_Enable' in channels and channels['Makeup_Enable']['value']:
            if 'Makeup_Weight' in channels:
                self.set_socket(self.shader_group_node, builder.in_makeup_weight, channels['Makeup_Weight']['value'])
                if channels['Makeup_Weight']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Makeup_Weight']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_makeup_weight_map)

            if 'Makeup_Base_Color' in channels:
                self.set_socket(self.shader_group_node, builder.in_makeup_base_color,
                                channels['Makeup_Base_Color']['value'])
                if channels['Makeup_Base_Color']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Makeup_Base_Color']['image_file'], False)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_makeup_base_color_map)

            if 'Makeup_Roughness_Mult' in channels:
                self.set_socket(self.shader_group_node, builder.in_makeup_roughness_mult,
                                channels['Makeup_Roughness_Mult']['value'])
                if channels['Makeup_Roughness_Mult']['image_file'] is not None:
                    node_image_texture = self.add_image_texture(channels['Makeup_Roughness_Mult']['image_file'], True)
                    self.link_socket(node_image_texture, self.shader_group_node, 0, builder.in_makeup_roughness_mult)
