from datetime import datetime

from bpy.types import BlendDataNodeTrees

from ...properties import MaterialImportProperties
from .sockets import color_socket_input_generator, float_socket_input_generator, \
    vector_socket_input_generator, link_socket_generator

GROUP_NAME = "Dual Lobe Specular"


def create_node_group(node_trees: BlendDataNodeTrees, props: MaterialImportProperties):
    node_group = node_trees.new(type='ShaderNodeTree', name=GROUP_NAME)
    node_group.color_tag = 'TEXTURE'
    node_group.description = f'Created by DAZ Material Importer at {datetime.now()}'
    node_group.default_group_node_width = 400

    socket_input_color = color_socket_input_generator(node_group)
    socket_input_float = float_socket_input_generator(node_group)
    socket_input_vector = vector_socket_input_generator(node_group)
    link_socket = link_socket_generator(node_group)

    # Input Sockets
    sock_dl_specular_weight_value = socket_input_float("Weight Value", 0)
    sock_dl_specular_weight_map = socket_input_color("Weight Map", (1, 1, 1, 1))
    sock_dl_specular_reflectivity_value = socket_input_float("Reflectivity Value", 0)
    sock_dl_specular_reflectivity_map = socket_input_color("Reflectivity Map", (1, 1, 1, 1))
    sock_dl_specular_roughness_mult = socket_input_float("Roughness Mult", 1)
    sock_specular_l1_roughness_value = socket_input_float("Lobe 1 Roughness Value", 0)
    sock_specular_l1_roughness_map = socket_input_color("Lobe 1 Roughness Map", (1, 1, 1, 1))
    sock_specular_l2_roughness_mult_value = socket_input_float("Lobe 2 Roughness Mult Value", 0)
    sock_specular_l2_roughness_mult_map = socket_input_color("Lobe 2 Roughness Mult Map", (1, 1, 1, 1))
    sock_dl_specular_ratio_value = socket_input_float("Ratio Value", 0)
    sock_dl_specular_ratio_map = socket_input_color("Ratio Map", (1, 1, 1, 1))
    sock_normal = socket_input_vector("Normal", (0, 0, 1))

    # Output Sockets
    sock_out_fac = node_group.interface.new_socket(name='Fac', in_out='OUTPUT', socket_type='NodeSocketFloat')
    sock_out_specular = node_group.interface.new_socket(name='Specular', in_out='OUTPUT', socket_type='NodeSocketShader')

    # Nodes: Group Input
    node_group_input = node_group.nodes.new('NodeGroupInput')
    node_group_input.name = 'Group Input'
    node_group_input.location = (-1159, -78)

    # Nodes: Dual Lobe Specular
    node_combine_dl_specular_weight = node_group.nodes.new('ShaderNodeHueSaturation')
    node_combine_dl_specular_weight.label = 'Combine Dual Lobe Specular Weight'
    node_combine_dl_specular_weight.name = 'node_combine_dl_specular_weight'
    node_combine_dl_specular_weight.location = (-522, 174)
    link_socket(node_group_input, node_combine_dl_specular_weight, sock_dl_specular_weight_value, 2)
    link_socket(node_group_input, node_combine_dl_specular_weight, sock_dl_specular_weight_map, 4)

    node_combine_dl_specular_reflectivity = node_group.nodes.new('ShaderNodeHueSaturation')
    node_combine_dl_specular_reflectivity.label = 'Combine Dual Lobe Specular Reflectivity'
    node_combine_dl_specular_reflectivity.name = 'node_combine_dl_specular_reflectivity'
    node_combine_dl_specular_reflectivity.location = (-518, -8)
    link_socket(node_group_input, node_combine_dl_specular_reflectivity, sock_dl_specular_reflectivity_value, 2)
    link_socket(node_group_input, node_combine_dl_specular_reflectivity, sock_dl_specular_reflectivity_map, 4)

    node_combine_specular_l1_roughness = node_group.nodes.new('ShaderNodeHueSaturation')
    node_combine_specular_l1_roughness.label = 'Combine Specular Lobe 1 Roughness'
    node_combine_specular_l1_roughness.name = 'node_combine_specular_l1_roughness'
    node_combine_specular_l1_roughness.location = (-514, -189)
    link_socket(node_group_input, node_combine_specular_l1_roughness, sock_specular_l1_roughness_value, 2)
    link_socket(node_group_input, node_combine_specular_l1_roughness, sock_specular_l1_roughness_map, 4)

    node_combine_specular_l2_roughness_mult = node_group.nodes.new('ShaderNodeHueSaturation')
    node_combine_specular_l2_roughness_mult.label = 'Combine Specular Lobe 2 Roughness'
    node_combine_specular_l2_roughness_mult.name = 'node_combine_specular_l2_roughness_mult'
    node_combine_specular_l2_roughness_mult.location = (-516, -373)
    link_socket(node_group_input, node_combine_specular_l2_roughness_mult, sock_specular_l2_roughness_mult_value, 2)
    link_socket(node_group_input, node_combine_specular_l2_roughness_mult, sock_specular_l2_roughness_mult_map, 4)

    node_combine_dl_specular_ratio = node_group.nodes.new('ShaderNodeHueSaturation')
    node_combine_dl_specular_ratio.label = 'Combine Dual Lobe Specular Ratio'
    node_combine_dl_specular_ratio.name = 'node_combine_dl_specular_ratio'
    node_combine_dl_specular_ratio.location = (-520, -564)
    link_socket(node_group_input, node_combine_dl_specular_ratio, sock_dl_specular_ratio_value, 2)
    link_socket(node_group_input, node_combine_dl_specular_ratio, sock_dl_specular_ratio_map, 4)

    node_dls_l1_multiply = node_group.nodes.new("ShaderNodeMix")
    node_dls_l1_multiply.label = "Lobe 1 Multiply"
    node_dls_l1_multiply.name = "node_dls_l1_multiply"
    node_dls_l1_multiply.location = (-188, 69)
    node_dls_l1_multiply.data_type = 'RGBA'
    node_dls_l1_multiply.blend_type = 'MULTIPLY'
    node_dls_l1_multiply.inputs[0].default_value = 1
    link_socket(node_combine_specular_l1_roughness, node_dls_l1_multiply, 0, 6)
    link_socket(node_group_input, node_dls_l1_multiply, sock_dl_specular_roughness_mult, 7)

    node_dls_l2_multiply = node_group.nodes.new("ShaderNodeMix")
    node_dls_l2_multiply.label = "Lobe 2 Multiply"
    node_dls_l2_multiply.name = "node_dls_l2_multiply"
    node_dls_l2_multiply.location = (-172, -255)
    node_dls_l2_multiply.data_type = 'RGBA'
    node_dls_l2_multiply.blend_type = 'MULTIPLY'
    node_dls_l2_multiply.inputs[0].default_value = 1
    link_socket(node_combine_specular_l1_roughness, node_dls_l2_multiply, 0, 6)
    link_socket(node_combine_specular_l2_roughness_mult, node_dls_l2_multiply, 0, 7)

    node_dls_l1_glossy = node_group.nodes.new("ShaderNodeBsdfGlossy")
    node_dls_l1_glossy.label = "Lobe 1 Glossy"
    node_dls_l1_glossy.name = "node_dls_l1_glossy"
    node_dls_l1_glossy.location = (43, 162)
    node_dls_l1_glossy.distribution = 'MULTI_GGX'
    link_socket(node_combine_dl_specular_reflectivity, node_dls_l1_glossy, 0, 0)
    link_socket(node_dls_l1_multiply, node_dls_l1_glossy, 2, 1)
    link_socket(node_group_input, node_dls_l1_glossy, sock_normal, 4)

    node_dls_l2_glossy = node_group.nodes.new("ShaderNodeBsdfGlossy")
    node_dls_l2_glossy.label = "Lobe 2 Glossy"
    node_dls_l2_glossy.name = "node_dls_l2_glossy"
    node_dls_l2_glossy.location = (51, -154)
    node_dls_l2_glossy.distribution = 'MULTI_GGX'
    link_socket(node_combine_dl_specular_reflectivity, node_dls_l2_glossy, 0, 0)
    link_socket(node_dls_l2_multiply, node_dls_l2_glossy, 2, 1)
    link_socket(node_group_input, node_dls_l2_glossy, sock_normal, 4)

    node_dls_layer_weight = node_group.nodes.new("ShaderNodeLayerWeight")
    node_dls_layer_weight.label = "Layer Weight"
    node_dls_layer_weight.name = "node_dls_layer_weight"
    node_dls_layer_weight.location = (53, -419)
    node_dls_layer_weight.inputs[0].default_value = props.dls_layer_factor
    link_socket(node_group_input, node_dls_layer_weight, sock_normal, 1)

    node_dls_mix_glossies = node_group.nodes.new("ShaderNodeMixShader")
    node_dls_mix_glossies.label = "Mix Glossies"
    node_dls_mix_glossies.name = "node_dls_mix_glossies"
    node_dls_mix_glossies.location = (340, 10)
    link_socket(node_combine_dl_specular_ratio, node_dls_mix_glossies, 0, 0)
    link_socket(node_dls_l1_glossy, node_dls_mix_glossies, 0, 1)
    link_socket(node_dls_l2_glossy, node_dls_mix_glossies, 0, 2)

    node_dls_layer_weight_factor = node_group.nodes.new("ShaderNodeMath")
    node_dls_layer_weight_factor.label = "DLS Layer Weight Factor"
    node_dls_layer_weight_factor.name = "node_dls_layer_weight_factor"
    node_dls_layer_weight_factor.location = (309, -228)
    node_dls_layer_weight_factor.operation = 'MULTIPLY'
    link_socket(node_combine_dl_specular_weight, node_dls_layer_weight_factor, 0, 0)
    link_socket(node_dls_layer_weight, node_dls_layer_weight_factor, 0, 1)

    node_group_output = node_group.nodes.new('NodeGroupOutput')
    node_group_output.name = 'Group Output'
    node_group_output.location = (680, 0)
    node_group_output.is_active_output = True
    link_socket(node_dls_layer_weight_factor, node_group_output, 0, sock_out_fac)
    link_socket(node_dls_mix_glossies, node_group_output, 0, sock_out_specular)
