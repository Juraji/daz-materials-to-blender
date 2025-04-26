from bpy.types import ShaderNodeBlackbody, ShaderNodeEmission, ShaderNodeClamp

from .base import ShaderGroupBuilder, SupportShaderGroupBuilder

__GROUP_NAME__ = "Blackbody Emission"
__MATERIAL_TYPE_ID__ = "blackbody_emission"


class BlackbodyEmissionShaderGroupBuilder(SupportShaderGroupBuilder):
    in_color = "Color"
    in_color_map = "Color Map"
    in_temperature = "Temperature (K)"
    in_luminance = "Luminance"
    in_luminance_map = "Luminance Map"

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
        sock_color = self._color_socket(self.in_color)
        sock_color_map = self._color_socket(self.in_color_map)
        sock_temperature = self._float_socket(self.in_temperature, 6500, props={"subtype": 'COLOR_TEMPERATURE', "min_value": 800, "max_value": 12000})
        sock_luminance = self._float_socket(self.in_luminance, 10)
        sock_luminance_map = self._color_socket(self.in_luminance_map)

        # Output Sockets
        sock_out_fac = self._float_socket(self.out_fac, in_out="OUTPUT")
        sock_out_shader = self._shader_socket(self.out_shader, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-920.0, 0.0))

        # Nodes: Emission
        node_mix_luminance = self._add_node__hsv("Mix Luminance and Map", (-660.0, -120.0))
        self._link_socket(node_group_input, node_mix_luminance, sock_luminance, 2)
        self._link_socket(node_group_input, node_mix_luminance, sock_luminance_map, 4)

        node_mix_color = self._add_node__mix("Mix Color and Map", (-660.0, -40.0))
        self._link_socket(node_group_input, node_mix_color, sock_color, 6)
        self._link_socket(node_group_input, node_mix_color, sock_color_map, 7)

        node_blackbody = self._add_node(ShaderNodeBlackbody, "Blackbody", (-660.0, -80.0))
        self._link_socket(node_group_input, node_blackbody, sock_temperature, 0)

        node_mix_color_temp = self._add_node__mix("Mix Color and Temp", (-420.0, -60.0))
        self._link_socket(node_mix_color, node_mix_color_temp, 2, 6)
        self._link_socket(node_blackbody, node_mix_color_temp, 0, 7)

        node_clamp_fac = self._add_node(ShaderNodeClamp, "Clamp Factor", (-200.0, -40.0))
        self._link_socket(node_mix_luminance, node_clamp_fac, 0, 0)
        self._set_socket(node_clamp_fac,1, 0)
        self._set_socket(node_clamp_fac,2, 1)

        node_emission_shader = self._add_node(ShaderNodeEmission, "Emission Shader", (-200.0, -80.0))
        self._link_socket(node_mix_color_temp, node_emission_shader, 0, 0)
        self._link_socket(node_mix_luminance, node_emission_shader, 0, 1)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0.0, 0.0))
        self._link_socket(node_clamp_fac, node_group_output, 0, sock_out_fac)
        self._link_socket(node_emission_shader, node_group_output, 0, sock_out_shader)
        # @formatter:on

        self.hide_all_nodes(node_group_input, node_group_output)
