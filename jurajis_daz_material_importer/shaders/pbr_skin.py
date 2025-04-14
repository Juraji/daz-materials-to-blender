import os
from datetime import datetime

import bpy
from bpy.types import BlendDataNodeTrees, ShaderNodeTree, Node

from .common.shader_group import MaterialShader
from .dls import DualLobeSpecularMaterialShader


class PBRSkinMaterialShader(MaterialShader):
    group_name = "DAZ PBR Skin"

    def create_node_group(self, node_trees: BlendDataNodeTrees):
        node_group = node_trees.new(type='ShaderNodeTree', name=self.group_name)
        node_group.color_tag = 'TEXTURE'
        node_group.description = f'Created at {datetime.now()}'
        node_group.default_group_node_width = 400

        socket_input_color = self.color_socket_input_generator(node_group)
        socket_input_float = self.float_socket_input_generator(node_group)
        socket_input_vector = self.vector_socket_input_generator(node_group)
        link_socket = self.link_socket_generator(node_group)

        # Panels
        panel_pbr_and_opacity = node_group.interface.new_panel("PBR and Opacity", default_closed=False)
        panel_dls = node_group.interface.new_panel("Dual Lobe Specular", default_closed=True)
        panel_sss = node_group.interface.new_panel("Sub Surface Scattering", default_closed=True)
        panel_normal_and_bump = node_group.interface.new_panel("Normal and Bump", default_closed=True)
        panel_top_coat = node_group.interface.new_panel("Top Coat", default_closed=True)

        # Input Sockets: Diffuse
        sock_diffuse_color_value = socket_input_color('Diffuse Color Value', (1.0, 1.0, 1.0, 1.0),
                                                      panel_pbr_and_opacity)
        sock_diffuse_color_map = socket_input_color('Diffuse Color Map', (1.0, 1.0, 1.0, 1.0), panel_pbr_and_opacity)

        # Input Sockets: Roughness
        sock_roughness_weight = socket_input_float('Roughness Weight', 0.0, panel_pbr_and_opacity)
        sock_roughness_map = socket_input_color('Roughness Map', (0.0, 0.0, 0.0, 1.0), panel_pbr_and_opacity)

        # Input Sockets: Metalic
        sock_metallic_weight_value = socket_input_float('Metallic Weight Value', 0.0, panel_pbr_and_opacity)
        sock_metallic_weight_map = socket_input_color('Metallic Weight Map', (0.0, 0.0, 0.0, 1.0),
                                                      panel_pbr_and_opacity)

        # Input Sockets: Opacity
        sock_opacity_value = socket_input_float('Opacity Value', 1.0, panel_pbr_and_opacity)
        sock_opacity_map = socket_input_color('Opacity Map', (1.0, 1.0, 1.0, 1.0), panel_pbr_and_opacity)

        # Dual Lobe Specular
        sock_dl_specular_weight_value = \
            socket_input_float("Dual Lobe Specular Weight Value", 0.0, panel_dls)
        sock_dl_specular_weight_map = \
            socket_input_color("Dual Lobe Specular Weight Map", (1.0, 1.0, 1.0, 1.0), panel_dls)
        sock_dl_specular_reflectivity_value = \
            socket_input_float("Dual Lobe Specular Reflectivity Value", 0.5, panel_dls)
        sock_dl_specular_reflectivity_map = \
            socket_input_color("Dual Lobe Specular Reflectivity Map", (1.0, 1.0, 1.0, 1.0), panel_dls)
        sock_dl_specular_roughness_mult = \
            socket_input_float("Dual Lobe Specular Roughness Mult", 1.0, panel_dls)
        sock_specular_l1_roughness_value = \
            socket_input_float("Specular Lobe 1 Roughness Value", 0.6, panel_dls)
        sock_specular_l1_roughness_map = \
            socket_input_color("Specular Lobe 1 Roughness Map", (1.0, 1.0, 1.0, 1.0), panel_dls)
        sock_specular_l2_roughness_mult_value = \
            socket_input_float("Specular Lobe 2 Roughness Mult Value", 0.4, panel_dls)
        sock_specular_l2_roughness_mult_map = \
            socket_input_color("Specular Lobe 2 Roughness Mult Map", (1.0, 1.0, 1.0, 1.0), panel_dls)
        sock_dl_specular_ratio_value = \
            socket_input_float("Dual Lobe Specular Ratio Value", 0.15, panel_dls)
        sock_dl_specular_ratio_map = \
            socket_input_color("Dual Lobe Specular Ratio Map", (1.0, 1.0, 1.0, 1.0), panel_dls)

        # Input Sockets: Translucency/SSS
        sock_sss_weight = socket_input_float('SSS Weight', 0.8, panel_sss)
        sock_sss_radius = socket_input_vector('SSS Radius', (1.0, 0.2, 0.1), panel_sss)
        sock_sss_scale = socket_input_float('SSS Scale', 0.004, panel_sss)
        sock_sss_scale.subtype = 'DISTANCE'
        sock_sss_direction = socket_input_float('SSS Direction', 0.8, panel_sss)

        # Input Sockets: Normal
        sock_normal_value = socket_input_float('Normal Value', 1.0, panel_normal_and_bump)
        sock_normal_map = socket_input_color('Normal Map', (0.5, 0.5, 1.0, 1.0), panel_normal_and_bump)

        # Input Sockets: Detail
        sock_detail_weight_value = socket_input_float('Detail Weight Value', 0.0, panel_normal_and_bump)
        sock_detail_weight_map = socket_input_color('Detail Weight Map', (1.0, 1.0, 1.0, 1.0), panel_normal_and_bump)
        sock_detail_normal_map = socket_input_color('Detail Normal Map', (0.5, 0.5, 1.0, 1.0), panel_normal_and_bump)

        # Input Sockets: Bump
        sock_bump_strength_value = socket_input_float('Bump Strength Value', 0.0, panel_normal_and_bump)
        sock_bump_strength_map = socket_input_color('Bump Strength Map', (1.0, 1.0, 1.0, 1.0), panel_normal_and_bump)

        # Input Sockets: Top Coat
        sock_top_coat_weight_value = socket_input_float('Top Coat Weight Value', 0.0, panel_top_coat)
        sock_top_coat_weight_map = socket_input_color('Top Coat Weight Map', (1.0, 1.0, 1.0, 1.0), panel_top_coat)
        sock_top_coat_roughness_value = socket_input_float('Top Coat Roughness Value', 0.7, panel_top_coat)
        sock_top_coat_roughness_map = socket_input_color('Top Coat Roughness Map', (1.0, 1.0, 1.0, 1.0), panel_top_coat)
        sock_top_coat_color_value = socket_input_color('Top Coat Color Value', (1.0, 1.0, 1.0, 1.0), panel_top_coat)
        sock_top_coat_color_map = socket_input_color('Top Coat Color Map', (1.0, 1.0, 1.0, 1.0), panel_top_coat)

        # Output Sockets: Surface
        sock_out_surface = node_group.interface.new_socket(name='Surface', in_out='OUTPUT',
                                                           socket_type='NodeSocketShader')

        # Frames
        frame_pbr_and_opacity = node_group.nodes.new("NodeFrame")
        frame_pbr_and_opacity.label = "PBR and Opacity"
        frame_pbr_and_opacity.name = 'frame_pbr_and_opacity'
        frame_pbr_and_opacity.location = (-210, 601)

        frame_normal_and_bump = node_group.nodes.new("NodeFrame")
        frame_normal_and_bump.label = "Normal, Detail and Bump"
        frame_normal_and_bump.name = 'frame_normal_and_bump'
        frame_normal_and_bump.location = (-188, -302)

        frame_top_coat = node_group.nodes.new("NodeFrame")
        frame_top_coat.label = "Top Coat"
        frame_top_coat.name = 'frame_top_coat'
        frame_top_coat.location = (5, -814)

        # Nodes: Group Input
        node_group_input = node_group.nodes.new('NodeGroupInput')
        node_group_input.name = 'Group Input'
        node_group_input.location = (-1045, -90)

        # Nodes: Diffuse
        node_combine_diffuse_value_and_map = node_group.nodes.new('ShaderNodeMix')
        node_combine_diffuse_value_and_map.label = 'Combine diffuse value and map'
        node_combine_diffuse_value_and_map.name = 'node_combine_diffuse_value_and_map'
        node_combine_diffuse_value_and_map.parent = frame_pbr_and_opacity
        node_combine_diffuse_value_and_map.location = (-158, -39)
        node_combine_diffuse_value_and_map.data_type = 'RGBA'
        node_combine_diffuse_value_and_map.blend_type = 'MULTIPLY'
        node_combine_diffuse_value_and_map.inputs[0].default_value = 1
        link_socket(node_group_input, node_combine_diffuse_value_and_map, sock_diffuse_color_map, 6)
        link_socket(node_group_input, node_combine_diffuse_value_and_map, sock_diffuse_color_value, 7)

        # Nodes: Roughness
        node_combine_roughness_value_and_map = node_group.nodes.new('ShaderNodeHueSaturation')
        node_combine_roughness_value_and_map.label = 'Combine roughness value and map'
        node_combine_roughness_value_and_map.name = 'node_combine_roughness_value_and_map'
        node_combine_roughness_value_and_map.parent = frame_pbr_and_opacity
        node_combine_roughness_value_and_map.location = (28, -39)
        link_socket(node_group_input, node_combine_roughness_value_and_map, sock_roughness_weight, 2)
        link_socket(node_group_input, node_combine_roughness_value_and_map, sock_roughness_map, 4)

        # Nodes: Metallic
        node_combine_metallic_value_and_map = node_group.nodes.new('ShaderNodeHueSaturation')
        node_combine_metallic_value_and_map.label = 'Combine metallic value and map'
        node_combine_metallic_value_and_map.name = 'node_combine_metallic_value_and_map'
        node_combine_metallic_value_and_map.parent = frame_pbr_and_opacity
        node_combine_metallic_value_and_map.location = (240, -39)
        link_socket(node_group_input, node_combine_metallic_value_and_map, sock_metallic_weight_value, 2)
        link_socket(node_group_input, node_combine_metallic_value_and_map, sock_metallic_weight_map, 4)

        # Nodes: Opacity
        node_combine_opacity_value_and_map = node_group.nodes.new('ShaderNodeHueSaturation')
        node_combine_opacity_value_and_map.label = 'Combine opacity value and map'
        node_combine_opacity_value_and_map.name = 'node_combine_opacity_value_and_map'
        node_combine_opacity_value_and_map.parent = frame_pbr_and_opacity
        node_combine_opacity_value_and_map.location = (446, -43)
        link_socket(node_group_input, node_combine_opacity_value_and_map, sock_opacity_value, 2)
        link_socket(node_group_input, node_combine_opacity_value_and_map, sock_opacity_map, 4)

        # Nodes: Normal/Detail/Bump
        node_normal_map = node_group.nodes.new('ShaderNodeNormalMap')
        node_normal_map.label = 'Normal Map'
        node_normal_map.name = 'node_normal_map'
        node_normal_map.parent = frame_normal_and_bump
        node_normal_map.location = (248, -88)
        link_socket(node_group_input, node_normal_map, sock_normal_value, 0)
        link_socket(node_group_input, node_normal_map, sock_normal_map, 1)

        node_combine_detail_weight_value_and_map = node_group.nodes.new('ShaderNodeHueSaturation')
        node_combine_detail_weight_value_and_map.label = 'Combine detail weight value and map'
        node_combine_detail_weight_value_and_map.name = 'node_combine_detail_weight_value_and_map'
        node_combine_detail_weight_value_and_map.parent = frame_normal_and_bump
        node_combine_detail_weight_value_and_map.location = (28, -240)
        link_socket(node_group_input, node_combine_detail_weight_value_and_map, sock_detail_weight_value, 2)
        link_socket(node_group_input, node_combine_detail_weight_value_and_map, sock_detail_weight_map, 4)

        node_detail_normal_map = node_group.nodes.new('ShaderNodeNormalMap')
        node_detail_normal_map.label = 'Detail normal map'
        node_detail_normal_map.name = 'node_detail_normal_map'
        node_detail_normal_map.parent = frame_normal_and_bump
        node_detail_normal_map.location = (247, -266)
        link_socket(node_combine_detail_weight_value_and_map, node_detail_normal_map, 0, 0)
        link_socket(node_group_input, node_detail_normal_map, sock_detail_normal_map, 1)

        node_combine_normal_and_detail_vectors = node_group.nodes.new('ShaderNodeVectorMath')
        node_combine_normal_and_detail_vectors.label = 'Combine normal and detail vectors'
        node_combine_normal_and_detail_vectors.name = 'node_combine_normal_and_detail_vectors'
        node_combine_normal_and_detail_vectors.operation = 'ADD'
        node_combine_normal_and_detail_vectors.parent = frame_normal_and_bump
        node_combine_normal_and_detail_vectors.location = (458, -151)
        link_socket(node_normal_map, node_combine_normal_and_detail_vectors, 0, 0)
        link_socket(node_detail_normal_map, node_combine_normal_and_detail_vectors, 0, 1)

        node_bump_map = node_group.nodes.new('ShaderNodeBump')
        node_bump_map.label = 'Bump map'
        node_bump_map.name = 'node_bump_map'
        node_bump_map.parent = frame_normal_and_bump
        node_bump_map.location = (683, -39)
        link_socket(node_group_input, node_bump_map, sock_bump_strength_value, 0)
        link_socket(node_group_input, node_bump_map, sock_bump_strength_map, 2)
        link_socket(node_combine_normal_and_detail_vectors, node_bump_map, 0, 3)

        # Nodes: Top Coat
        node_combine_top_coat_weight_value_and_map = node_group.nodes.new('ShaderNodeHueSaturation')
        node_combine_top_coat_weight_value_and_map.label = 'Combine top coat weight value and map'
        node_combine_top_coat_weight_value_and_map.name = 'node_combine_top_coat_weight_value_and_map'
        node_combine_top_coat_weight_value_and_map.parent = frame_top_coat
        node_combine_top_coat_weight_value_and_map.location = (36, -44)
        link_socket(node_group_input, node_combine_top_coat_weight_value_and_map, sock_top_coat_weight_value, 2)
        link_socket(node_group_input, node_combine_top_coat_weight_value_and_map, sock_top_coat_weight_map, 4)

        node_combine_top_coat_roughness_value_and_map = node_group.nodes.new('ShaderNodeHueSaturation')
        node_combine_top_coat_roughness_value_and_map.label = 'Combine top coat roughness value and map'
        node_combine_top_coat_roughness_value_and_map.name = 'node_combine_top_coat_roughness_value_and_map'
        node_combine_top_coat_roughness_value_and_map.parent = frame_top_coat
        node_combine_top_coat_roughness_value_and_map.location = (232, -39)
        link_socket(node_group_input, node_combine_top_coat_roughness_value_and_map, sock_top_coat_roughness_value, 2)
        link_socket(node_group_input, node_combine_top_coat_roughness_value_and_map, sock_top_coat_roughness_map, 4)

        node_combine_top_coat_color_value_and_map = node_group.nodes.new('ShaderNodeMix')
        node_combine_top_coat_color_value_and_map.label = 'Combine top coat color value and map'
        node_combine_top_coat_color_value_and_map.name = 'node_combine_top_coat_color_value_and_map'
        node_combine_top_coat_color_value_and_map.parent = frame_top_coat
        node_combine_top_coat_color_value_and_map.location = (31, -240)
        node_combine_top_coat_color_value_and_map.data_type = 'RGBA'
        node_combine_diffuse_value_and_map.blend_type = 'MULTIPLY'
        node_combine_diffuse_value_and_map.inputs[0].default_value = 1
        link_socket(node_group_input, node_combine_top_coat_color_value_and_map, sock_top_coat_color_map, 6)
        link_socket(node_group_input, node_combine_top_coat_color_value_and_map, sock_top_coat_color_value, 7)

        # Nodes: Bdsf Shader
        node_principled_bsdf = node_group.nodes.new('ShaderNodeBsdfPrincipled')
        node_principled_bsdf.label = 'Principled BDSF'
        node_principled_bsdf.name = 'node_principled_bsdf'
        node_principled_bsdf.location = (776, 0)
        node_principled_bsdf.subsurface_method = 'RANDOM_WALK_SKIN'
        link_socket(node_combine_diffuse_value_and_map, node_principled_bsdf, 2, 0)
        link_socket(node_combine_metallic_value_and_map, node_principled_bsdf, 0, 1)
        link_socket(node_combine_roughness_value_and_map, node_principled_bsdf, 0, 2)
        link_socket(node_combine_opacity_value_and_map, node_principled_bsdf, 0, 4)
        link_socket(node_bump_map, node_principled_bsdf, 0, 5)
        link_socket(node_group_input, node_principled_bsdf, sock_sss_weight, 8)
        link_socket(node_group_input, node_principled_bsdf, sock_sss_radius, 9)
        link_socket(node_group_input, node_principled_bsdf, sock_sss_scale, 10)
        link_socket(node_group_input, node_principled_bsdf, sock_sss_direction, 12)
        link_socket(node_combine_top_coat_weight_value_and_map, node_principled_bsdf, 0, 19)
        link_socket(node_combine_top_coat_roughness_value_and_map, node_principled_bsdf, 0, 20)
        link_socket(node_combine_top_coat_color_value_and_map, node_principled_bsdf, 2, 22)
        link_socket(node_bump_map, node_principled_bsdf, 0, 23)

        # Nodes: Dual Lobe Specular
        dls_group = node_group.nodes.new("ShaderNodeGroup")
        dls_group.label = DualLobeSpecularMaterialShader.group_name
        dls_group.name = (f'{self.group_name}_${DualLobeSpecularMaterialShader.group_name}'
                          .replace(' ', '_').lower())
        dls_group.location = (18, 218)
        dls_group.width, dls_group.height = 400.0, 100.0
        dls_group.node_tree = bpy.data.node_groups[DualLobeSpecularMaterialShader.group_name]
        link_socket(node_group_input, dls_group, sock_dl_specular_weight_value, 0)
        link_socket(node_group_input, dls_group, sock_dl_specular_weight_map, 1)
        link_socket(node_group_input, dls_group, sock_dl_specular_reflectivity_value, 2)
        link_socket(node_group_input, dls_group, sock_dl_specular_reflectivity_map, 3)
        link_socket(node_group_input, dls_group, sock_dl_specular_roughness_mult, 4)
        link_socket(node_group_input, dls_group, sock_specular_l1_roughness_value, 5)
        link_socket(node_group_input, dls_group, sock_specular_l1_roughness_map, 6)
        link_socket(node_group_input, dls_group, sock_specular_l2_roughness_mult_value, 7)
        link_socket(node_group_input, dls_group, sock_specular_l2_roughness_mult_map, 8)
        link_socket(node_group_input, dls_group, sock_dl_specular_ratio_value, 9)
        link_socket(node_group_input, dls_group, sock_dl_specular_ratio_map, 10)
        link_socket(node_bump_map, dls_group, 0, 11)

        node_dls_mix_surfaces = node_group.nodes.new("ShaderNodeMixShader")
        node_dls_mix_surfaces.label = "Mix Surfaces"
        node_dls_mix_surfaces.name = "node_dls_mix_surfaces"
        node_dls_mix_surfaces.location = (1064, 161)
        link_socket(dls_group, node_dls_mix_surfaces, 0, 0)
        link_socket(dls_group, node_dls_mix_surfaces, 1, 2)
        link_socket(node_principled_bsdf, node_dls_mix_surfaces, 0, 1)

        # Group Output
        node_group_output = node_group.nodes.new('NodeGroupOutput')
        node_group_output.name = 'Group Output'
        node_group_output.location = (1272, -5)
        node_group_output.is_active_output = True
        link_socket(node_dls_mix_surfaces, node_group_output, 0, sock_out_surface)

    def apply_material(self,
                       node_tree: ShaderNodeTree,
                       node_mapping: Node,
                       node_material_output: Node,
                       channels: dict):
        shader_group = node_tree.nodes.new("ShaderNodeGroup")
        shader_group.label = self.group_name
        shader_group.name = self.group_name
        shader_group.location = (-521.4857788085938, -1.3936055898666382)
        shader_group.width, shader_group.height = 400.0, 100.0
        shader_group.node_tree = bpy.data.node_groups[self.group_name]
        node_tree.links.new(shader_group.outputs[0], node_material_output.inputs[0])

        tex_location_x = -1200

        def tex_location_y_gen():
            location = 400
            while True:
                yield location
                location -= 300

        tex_location_y = tex_location_y_gen()

        def image_texture(path: str, non_color: bool, tile: int) -> Node:
            tex_image = node_tree.nodes.new(type='ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(path)
            # noinspection PyTypeChecker
            tex_image.image.colorspace_settings.name = 'Non-Color' if non_color else 'sRGB'
            tex_image.location = (tex_location_x, next(tex_location_y))
            tex_image.image_user.tile = tile

            img_name = os.path.basename(path)
            if img_name in bpy.data.images:
                tex_image.image = bpy.data.images[img_name]
            else:
                tex_image.image = bpy.data.images.load(img_name)

            node_tree.links.new(node_mapping.outputs[0], tex_image.inputs[0])
            return tex_image

        if 'Diffuse' in channels:
            shader_group.inputs['Diffuse Color Value'].default_value = channels['Diffuse']['value']
            if channels['Diffuse']['image_file'] is not None:
                node_image_texture = image_texture(channels['Diffuse']['image_file'], False, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Diffuse Color Map'])

        if 'Diffuse_Roughness' in channels:
            shader_group.inputs['Roughness Weight'].default_value = channels['Diffuse_Roughness']['value']
            if channels['Diffuse_Roughness']['image_file'] is not None:
                node_image_texture = image_texture(channels['Diffuse_Roughness']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Roughness Map'])

        if 'Metallic_Weight' in channels:
            shader_group.inputs['Metallic Weight Value'].default_value = channels['Metallic_Weight']['value']
            if channels['Metallic_Weight']['image_file'] is not None:
                node_image_texture = image_texture(channels['Metallic_Weight']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Metallic Weight Map'])

        if 'Cutout_Opacity' in channels:
            shader_group.inputs['Opacity Value'].default_value = channels['Cutout_Opacity']['value']
            if channels['Cutout_Opacity']['image_file'] is not None:
                node_image_texture = image_texture(channels['Cutout_Opacity']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Opacity Map'])

        if 'Dual_Lobe_Specular_Enable' in channels and channels['Dual_Lobe_Specular_Enable']['value']:
            if 'Dual_Lobe_Specular_Weight' in channels:
                shader_group.inputs['Dual Lobe Specular Weight Value'].default_value = \
                    channels['Dual_Lobe_Specular_Weight']['value']
                if channels['Dual_Lobe_Specular_Weight']['image_file'] is not None:
                    node_image_texture = image_texture(channels['Dual_Lobe_Specular_Weight']['image_file'], True, 1)
                    node_tree.links.new(node_image_texture.outputs[0],
                                        shader_group.inputs['Dual Lobe Specular Weight Map'])

            if 'Dual_Lobe_Specular_Reflectivity' in channels:
                shader_group.inputs['Dual Lobe Specular Reflectivity Value'].default_value = \
                    channels['Dual_Lobe_Specular_Reflectivity']['value']
                if channels['Dual_Lobe_Specular_Reflectivity']['image_file'] is not None:
                    node_image_texture = image_texture(channels['Dual_Lobe_Specular_Reflectivity']['image_file'], True,
                                                       1)
                    node_tree.links.new(node_image_texture.outputs[0],
                                        shader_group.inputs['Dual Lobe Specular Reflectivity Map'])

            if 'Dual_Lobe_Specular_Roughness_Mult' in channels:
                shader_group.inputs['Dual Lobe Specular Roughness Mult'].default_value = \
                    channels['Dual_Lobe_Specular_Roughness_Mult']['value']

            if 'Specular_Lobe_1_Roughness' in channels:
                shader_group.inputs['Specular Lobe 1 Roughness Value'].default_value = \
                    channels['Specular_Lobe_1_Roughness']['value']
                if channels['Specular_Lobe_1_Roughness']['image_file'] is not None:
                    node_image_texture = image_texture(channels['Specular_Lobe_1_Roughness']['image_file'], True, 1)
                    node_tree.links.new(node_image_texture.outputs[0],
                                        shader_group.inputs['Specular Lobe 1 Roughness Map'])

            if 'Specular_Lobe_2_Roughness_Mult' in channels:
                shader_group.inputs['Specular Lobe 2 Roughness Mult Value'].default_value = \
                    channels['Specular_Lobe_2_Roughness_Mult']['value']
                if channels['Specular_Lobe_2_Roughness_Mult']['image_file'] is not None:
                    node_image_texture = image_texture(channels['Specular_Lobe_2_Roughness_Mult']['image_file'], True,
                                                       1)
                    node_tree.links.new(node_image_texture.outputs[0],
                                        shader_group.inputs['Specular Lobe 2 Roughness Mult Map'])

            if 'Dual_Lobe_Specular_Ratio' in channels:
                shader_group.inputs['Dual Lobe Specular Ratio Value'].default_value = \
                    channels['Dual_Lobe_Specular_Ratio'][
                        'value']
                if channels['Dual_Lobe_Specular_Ratio']['image_file'] is not None:
                    node_image_texture = image_texture(channels['Dual_Lobe_Specular_Ratio']['image_file'], True, 1)
                    node_tree.links.new(node_image_texture.outputs[0],
                                        shader_group.inputs['Dual Lobe Specular Ratio Map'])

        if 'Translucency_Weight' in channels:
            shader_group.inputs['SSS Weight'].default_value = abs(channels['Translucency_Weight']['value'])

        if 'Sub_Surface_Enable' in channels and channels['Sub_Surface_Enable']['value']:
            if 'SSS_Color' in channels:
                # It's a color, but we need the rgb vector, just omit alpha
                shader_group.inputs['SSS Radius'].default_value = channels['SSS_Color']['value'][:3]
            if 'SSS Direction' in channels:
                # DAZ Value is negative, we need positive
                shader_group.inputs['SSS Direction'].default_value = abs(channels['SSS_Direction']['value'])

        if 'Normal_Map' in channels:
            shader_group.inputs['Normal Value'].default_value = (
                    channels['Normal_Map']['value'] * self.properties.normal_factor)
            if channels['Normal_Map']['image_file'] is not None:
                node_image_texture = image_texture(channels['Normal_Map']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Normal Map'])

        if 'Detail_Enable' in channels and channels['Detail_Enable']['value']:
            shader_group.inputs['Detail Weight Value'].default_value = (
                    channels['Detail_Weight']['value'] * self.properties.normal_factor)
            if channels['Detail_Weight']['image_file'] is not None:
                node_image_texture = image_texture(channels['Detail_Weight']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Detail Weight Map'])
            if channels['Detail_Normal_Map']['image_file'] is not None:
                node_image_texture = image_texture(channels['Detail_Normal_Map']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Detail Normal Map'])

        if 'Bump_Enable' in channels and channels['Bump_Enable']['value']:
            shader_group.inputs['Bump Strength Value'].default_value = channels['Bump_Strength']['value']
            if channels['Bump_Strength']['image_file'] is not None:
                node_image_texture = image_texture(channels['Bump_Strength']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Bump Strength Map'])

        if 'Top_Coat_Enable' in channels and channels['Top_Coat_Enable']['value']:
            shader_group.inputs['Top Coat Weight Value'].default_value = channels['Top_Coat_Weight']['value']
            if channels['Top_Coat_Weight']['image_file'] is not None:
                node_image_texture = image_texture(channels['Top_Coat_Weight']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Top Coat Weight Map'])

            shader_group.inputs['Top Coat Roughness Value'].default_value = channels['Top_Coat_Roughness']['value']
            if channels['Top_Coat_Roughness']['image_file'] is not None:
                node_image_texture = image_texture(channels['Top_Coat_Roughness']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Top Coat Roughness Map'])

            shader_group.inputs['Top Coat Color Value'].default_value = channels['Top_Coat_Color']['value']
            if channels['Top_Coat_Color']['image_file'] is not None:
                node_image_texture = image_texture(channels['Top_Coat_Color']['image_file'], True, 1)
                node_tree.links.new(node_image_texture.outputs[0], shader_group.inputs['Top Coat Color Map'])
