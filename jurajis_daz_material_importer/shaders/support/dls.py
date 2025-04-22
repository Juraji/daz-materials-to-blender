from .base import ShaderGroupBuilder

__GROUP_NAME__ = "Dual Lobe Specular"
__MATERIAL_TYPE_ID__ = "dls"


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
    dls_layer_weight = 0.7

    out_fac = "Fac"
    out_shader = "Shader"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def setup_group(self):
        super().setup_group()

        # Input sockets
        sock_weight = self._float_socket(self.in_weight, 0.35)
        sock_weight_map = self._color_socket(self.in_weight_map)
        sock_reflectivity = self._float_socket(self.in_reflectivity, 0.25)
        sock_reflectivity_map = self._color_socket(self.in_reflectivity_map)
        sock_roughness_mult = self._float_socket(self.in_roughness_mult, 1)
        sock_l1_roughness = self._float_socket(self.in_l1_roughness, 0.7)
        sock_l1_roughness_map = self._color_socket(self.in_l1_roughness_map)
        sock_l2_roughness_mult = self._float_socket(self.in_l2_roughness_mult, 0.45)
        sock_l2_roughness_mult_map = self._color_socket(self.in_l2_roughness_mult_map)
        sock_ratio = self._float_socket(self.in_ratio ,0.15)
        sock_ratio_map = self._color_socket(self.in_ratio_map)
        sock_normal = self._vector_socket(self.in_normal)

        # Output Sockets
        sock_out_fac = self._float_socket(self.out_fac, in_out='OUTPUT')
        sock_out_specular = self._shader_socket(self.out_shader, in_out='OUTPUT')

        # Nodes: Group Input
        node_group_input = self._add_node__group_input('Group Input', (-1159, -78))

        # Nodes: Dual Lobe Specular
        node_combine_weight = self._add_node__hsv('Combine Specular Weight', (-522, 174))
        self._link_socket(node_group_input, node_combine_weight, sock_weight, 2)
        self._link_socket(node_group_input, node_combine_weight, sock_weight_map, 4)

        node_combine_reflectivity = self._add_node__hsv('Combine Specular Reflectivity', (-518, -8))
        self._link_socket(node_group_input, node_combine_reflectivity, sock_reflectivity, 2)
        self._link_socket(node_group_input, node_combine_reflectivity, sock_reflectivity_map, 4)

        node_combine_l1_roughness = self._add_node__hsv('Combine Lobe 1 Roughness', (-514, -189))
        self._link_socket(node_group_input, node_combine_l1_roughness, sock_l1_roughness, 2)
        self._link_socket(node_group_input, node_combine_l1_roughness, sock_l1_roughness_map, 4)

        node_combine_l2_roughness_mult = self._add_node__hsv('Combine Specular Lobe 2 Roughness', (-516, -373))
        self._link_socket(node_group_input, node_combine_l2_roughness_mult, sock_l2_roughness_mult, 2)
        self._link_socket(node_group_input, node_combine_l2_roughness_mult, sock_l2_roughness_mult_map, 4)

        node_combine_ratio = self._add_node__hsv('Combine Dual Lobe Specular Ratio', (-520, -564))
        self._link_socket(node_group_input, node_combine_ratio, sock_ratio, 2)
        self._link_socket(node_group_input, node_combine_ratio, sock_ratio_map, 4)

        node_l1_multiply = self._add_node__mix("Lobe 1 Multiply", (-188, 69))
        self._link_socket(node_combine_l1_roughness, node_l1_multiply, 0, 6)
        self._link_socket(node_group_input, node_l1_multiply, sock_roughness_mult, 7)

        node_l2_multiply = self._add_node__mix("Lobe 2 Multiply", (-172, -255))
        self._link_socket(node_combine_l1_roughness, node_l2_multiply, 0, 6)
        self._link_socket(node_combine_l2_roughness_mult, node_l2_multiply, 0, 7)

        node_l1_glossy = self._add_node("ShaderNodeBsdfGlossy", "Lobe 1 Glossy", (43, 162))
        node_l1_glossy.distribution = 'MULTI_GGX'
        self._link_socket(node_combine_reflectivity, node_l1_glossy, 0, 0)
        self._link_socket(node_l1_multiply, node_l1_glossy, 2, 1)
        self._link_socket(node_group_input, node_l1_glossy, sock_normal, 4)

        node_l2_glossy = self._add_node("ShaderNodeBsdfGlossy", "Lobe 2 Glossy", (51, -154))
        node_l2_glossy.distribution = 'MULTI_GGX'
        self._link_socket(node_combine_reflectivity, node_l2_glossy, 0, 0)
        self._link_socket(node_l2_multiply, node_l2_glossy, 2, 1)
        self._link_socket(node_group_input, node_l2_glossy, sock_normal, 4)

        node_layer_weight = self._add_node("ShaderNodeLayerWeight", "Layer Weight", (53, -419))
        self._set_socket(node_layer_weight, 0, self.dls_layer_weight)
        self._link_socket(node_group_input, node_layer_weight, sock_normal, 1)

        node_mix_glossies = self._add_node__mix_shader("Mix Glossies", (340, 10))
        self._link_socket(node_combine_ratio, node_mix_glossies, 0, 0)
        self._link_socket(node_l1_glossy, node_mix_glossies, 0, 1)
        self._link_socket(node_l2_glossy, node_mix_glossies, 0, 2)

        node_layer_weight_factor = self._add_node("ShaderNodeMath", "Layer Weight Factor", (309, -228))
        node_layer_weight_factor.operation = 'MULTIPLY'
        self._link_socket(node_combine_weight, node_layer_weight_factor, 0, 0)
        self._link_socket(node_layer_weight, node_layer_weight_factor, 0, 1)

        # Group Output
        node_group_output = self._add_node__group_output('Group Output', (680, 0))
        self._link_socket(node_layer_weight_factor, node_group_output, 0, sock_out_fac)
        self._link_socket(node_mix_glossies, node_group_output, 0, sock_out_specular)
