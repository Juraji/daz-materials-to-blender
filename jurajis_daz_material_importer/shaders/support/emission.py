from .base import ShaderGroupBuilder, SupportShaderGroupBuilder

__GROUP_NAME__ = "Blackbody Emission"
__MATERIAL_TYPE_ID__ = "blackbody_emission"


class BlackbodyEmissionShaderGroupBuilder(SupportShaderGroupBuilder):
    in_color = "Color"
    in_color_map = "Color Map"
    in_temperature = "Temperature (K)"
    in_luminance = "Luminance"
    in_luminance_map = "Luminance Map"

    out_weight = "Weight"
    out_color = "Color"

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
        sock_color = self._color_socket(self.in_color)
        sock_color_map = self._color_socket(self.in_color_map)
        sock_temperature = self._float_socket(self.in_temperature, 6500, props={"subtype": 'COLOR_TEMPERATURE', "min_value": 800, "max_value": 12000})
        sock_luminance = self._float_socket(self.in_luminance, 10)
        sock_luminance_map = self._color_socket(self.in_luminance_map)

        # Output Sockets
        sock_out_weight = self._float_socket(self.out_weight, in_out="OUTPUT")
        sock_out_color = self._color_socket(self.out_color, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (310, 0))

        # Nodes: Emission
        node_mix_luminance = self._add_node__hsv("Mix Luminance and Map", (-120, 209))
        self._link_socket(node_group_input, node_mix_luminance, sock_luminance, 2)
        self._link_socket(node_group_input, node_mix_luminance, sock_luminance_map, 4)

        node_mix_color = self._add_node__mix("Mix Color and Map", (-111, 30))
        self._link_socket(node_group_input, node_mix_color, sock_color, 6)
        self._link_socket(node_group_input, node_mix_color, sock_color_map, 7)

        node_blackbody = self._add_node("ShaderNodeBlackbody", "Blackbody", (-111, -209))
        self._link_socket(node_group_input, node_blackbody, sock_temperature, 0)

        node_mix_color_temp = self._add_node__mix("Mix Color and Temp", (120, -10))
        self._link_socket(node_mix_color, node_mix_color_temp, 2, 6)
        self._link_socket(node_blackbody, node_mix_color_temp, 0, 7)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (310.0, 0.0))
        self._link_socket(node_mix_luminance, node_group_output, 0, sock_out_weight)
        self._link_socket(node_mix_color_temp, node_group_output, 2, sock_out_color)
        # @formatter:on
