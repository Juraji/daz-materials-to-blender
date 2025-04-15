from .material_shader import ShaderGroupBuilder

__GROUP_NAME__ = "Dual Lobe Specular"


class DualLobeSpecularShaderGroupBuilder(ShaderGroupBuilder):
    in_weight = 'Weight'
    in_weight_map = 'Weight Map'
    in_reflectivity = 'Reflectivity'
    in_reflectivity_map = 'Reflectivity Map'
    in_roughness_mult = 'Roughness Mult'
    in_l1_roughness = 'Lobe 1 Roughness'
    in_l1_roughness_map = 'Lobe 1 Roughness Map'
    in_l2_roughness_mult = 'Lobe 2 Roughness'
    in_l2_roughness_mult_map = 'Lobe 2 Roughness Map'
    in_ratio = 'Ratio'
    in_ratio_map = 'Ratio Map'
    in_normal = 'Normal'

    @staticmethod
    def group_name() -> str: return __GROUP_NAME__

    def setup_group(self):
        super().setup_group()

        # Input sockets
        sock_weight = self.float_socket(self.in_weight)
        sock_weight_map = self.color_socket(self.in_weight_map)
        sock_reflectivity = self.float_socket(self.in_reflectivity)
        sock_reflectivity_map = self.color_socket(self.in_reflectivity_map)
        sock_roughness_mult = self.float_socket(self.in_roughness_mult)
        sock_l1_roughness = self.float_socket(self.in_l1_roughness)
        sock_l1_roughness_map = self.color_socket(self.in_l1_roughness_map)
        sock_l2_roughness_mult = self.float_socket(self.in_l2_roughness_mult)
        sock_l2_roughness_mult_map = self.color_socket(self.in_l2_roughness_mult_map)
        sock_ratio = self.float_socket(self.in_ratio)
        sock_ratio_map = self.color_socket(self.in_ratio_map)
        sock_normal = self.vector_socket(self.in_normal)

        # Output Sockets
        sock_out_fac = self.float_socket('Fac', in_out='OUTPUT')
        sock_out_specular = self.shader_socket('Specular', in_out='OUTPUT')

        # Nodes: Group Input
        node_group_input = self.add_node__group_input('Group Input', (-1159, -78))

        # Nodes: Dual Lobe Specular
        node_combine_weight = self.add_node__hsv('Combine Specular Weight', (-522, 174))
        self.link_socket(node_group_input, node_combine_weight, sock_weight, 2)
        self.link_socket(node_group_input, node_combine_weight, sock_weight_map, 4)

        node_combine_reflectivity = self.add_node__hsv('Combine Specular Reflectivity', (-518, -8))
        self.link_socket(node_group_input, node_combine_reflectivity, sock_reflectivity, 2)
        self.link_socket(node_group_input, node_combine_reflectivity, sock_reflectivity_map, 4)

        node_combine_l1_roughness = self.add_node__hsv('Combine Lobe 1 Roughness', (-514, -189))
        self.link_socket(node_group_input, node_combine_l1_roughness, sock_l1_roughness, 2)
        self.link_socket(node_group_input, node_combine_l1_roughness, sock_l1_roughness_map, 4)

        node_combine_l2_roughness_mult = self.add_node__hsv('Combine Specular Lobe 2 Roughness', (-516, -373))
        self.link_socket(node_group_input, node_combine_l2_roughness_mult, sock_l2_roughness_mult, 2)
        self.link_socket(node_group_input, node_combine_l2_roughness_mult, sock_l2_roughness_mult_map, 4)

        node_combine_ratio = self.add_node__hsv('Combine Dual Lobe Specular Ratio', (-520, -564))
        self.link_socket(node_group_input, node_combine_ratio, sock_ratio, 2)
        self.link_socket(node_group_input, node_combine_ratio, sock_ratio_map, 4)

        node_l1_multiply = self.add_node__mix("Lobe 1 Multiply", (-188, 69))
        self.link_socket(node_combine_l1_roughness, node_l1_multiply, 0, 6)
        self.link_socket(node_group_input, node_l1_multiply, sock_roughness_mult, 7)

        node_l2_multiply = self.add_node__mix("Lobe 2 Multiply", (-172, -255))
        self.link_socket(node_combine_l1_roughness, node_l2_multiply, 0, 6)
        self.link_socket(node_combine_l2_roughness_mult, node_l2_multiply, 0, 7)

        node_l1_glossy = self.add_node("ShaderNodeBsdfGlossy", "Lobe 1 Glossy", (43, 162))
        node_l1_glossy.distribution = 'MULTI_GGX'
        self.link_socket(node_combine_reflectivity, node_l1_glossy, 0, 0)
        self.link_socket(node_l1_multiply, node_l1_glossy, 2, 1)
        self.link_socket(node_group_input, node_l1_glossy, sock_normal, 4)

        node_l2_glossy = self.add_node("ShaderNodeBsdfGlossy", "Lobe 2 Glossy", (51, -154))
        node_l2_glossy.distribution = 'MULTI_GGX'
        self.link_socket(node_combine_reflectivity, node_l2_glossy, 0, 0)
        self.link_socket(node_l2_multiply, node_l2_glossy, 2, 1)
        self.link_socket(node_group_input, node_l2_glossy, sock_normal, 4)

        node_layer_weight = self.add_node(
            "ShaderNodeLayerWeight", "Layer Weight", (53, -419))
        self.set_socket(node_layer_weight, 0, self.properties.dls_layer_factor)
        self.link_socket(node_group_input, node_layer_weight, sock_normal, 1)

        node_mix_glossies = self.add_node__mix_shader("Mix Glossies", (340, 10))
        self.link_socket(node_combine_ratio, node_mix_glossies, 0, 0)
        self.link_socket(node_l1_glossy, node_mix_glossies, 0, 1)
        self.link_socket(node_l2_glossy, node_mix_glossies, 0, 2)

        node_layer_weight_factor = self.add_node("ShaderNodeMath", "Layer Weight Factor", (309, -228))
        node_layer_weight_factor.operation = 'MULTIPLY'
        self.link_socket(node_combine_weight, node_layer_weight_factor, 0, 0)
        self.link_socket(node_layer_weight, node_layer_weight_factor, 0, 1)

        # Group Output
        node_group_output = self.add_node__group_output('Group Output', (680, 0))
        self.link_socket(node_layer_weight_factor, node_group_output, 0, sock_out_fac)
        self.link_socket(node_mix_glossies, node_group_output, 0, sock_out_specular)
