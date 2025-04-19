from .base import SupportShaderGroupBuilder

__GROUP_NAME__ = "Weighted Translucency"
__MATERIAL_TYPE_ID__ = "w_translucency"

class WeightedTranslucencyShaderGroupBuilder(SupportShaderGroupBuilder):
    in_translucency_weight = "Translucency Weight"
    in_translucency_weight_map = "Translucency Weight Map"
    in_translucency_color = "Translucency Color"
    in_translucency_color_map = "Translucency Color Map"
    in_invert_transmission_normal = "Invert Transmission Normal"
    in_normal = "Normal"

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
        
        # @formatter:off
        # Input Sockets
        sock_weight = self._float_socket(self.in_translucency_weight, 1)
        sock_weight_map = self._color_socket(self.in_translucency_weight_map)
        sock_color = self._color_socket(self.in_translucency_color)
        sock_color_map = self._color_socket(self.in_translucency_color_map)
        sock_invert_transmission_normal = self._bool_socket(self.in_invert_transmission_normal, False)
        sock_normal = self._vector_socket(self.in_normal, (0.5, 0.5, 1.0))

        sock_out_fac = self._float_socket(self.out_fac, in_out="OUTPUT")
        sock_out_shader = self._shader_socket(self.out_shader, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-972, 0))

        # Nodes: Translucency
        node_mix_weight_map = self._add_node__mix("Mix Weight Map", (-156, 237))
        self._link_socket(node_group_input, node_mix_weight_map, sock_weight, 6)
        self._link_socket(node_group_input, node_mix_weight_map, sock_weight_map, 7)

        node_mix_color_map = self._add_node__mix("Mix Color Map", (-153, -23))
        self._link_socket(node_group_input, node_mix_color_map, sock_color, 6)
        self._link_socket(node_group_input, node_mix_color_map, sock_color_map, 7)

        node_mult_invert2 = self._add_node__math("Invert * 2",  (-672, -280))
        self._set_socket(node_mult_invert2, 0, 2.0)
        self._link_socket(node_group_input, node_mult_invert2, sock_invert_transmission_normal, 1)

        node_flip_factor = self._add_node__math("Flip invert factor", (-412, -280))
        self._set_socket(node_flip_factor, 0, 1.0)
        self._link_socket(node_mult_invert2, node_flip_factor, 0, 1)

        node_flip_normal = self._add_node__math_vector("Flip normal", (-152, -297), "MULTIPLY")
        self._link_socket(node_flip_factor, node_flip_normal, 0, 0)
        self._link_socket(node_group_input, node_flip_normal, sock_normal, 1)

        node_trans_bsdf = self._add_node("ShaderNodeBsdfTranslucent", "Translucent BSDF", (230, 8))
        self._link_socket(node_mix_color_map, node_trans_bsdf, 2, 0)
        self._link_socket(node_flip_normal, node_trans_bsdf, 0, 1)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (533, 0))
        self._link_socket(node_mix_weight_map, node_group_output, 2, sock_out_fac)
        self._link_socket(node_trans_bsdf, node_group_output, 0, sock_out_shader)
        # @formatter:on