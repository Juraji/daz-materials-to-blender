from .base import SupportShaderGroupBuilder

__GROUP_NAME__ = "Weighted Transmission"
__MATERIAL_TYPE_ID__ = "w_transmission"


class WeightedTransmissonShaderGroupBuilder(SupportShaderGroupBuilder):
    in_transmitted_measurement_distance = "Transmitted Measurement Distance"
    in_transmitted_color = "Transmitted Color"
    in_transmitted_color_map = "Transmitted Color Map"

    out_weight = "Weight"
    out_volume = "Volume"

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
        sock_transmitted_measurement_distance = self._float_socket(self.in_transmitted_measurement_distance, 0.1)
        sock_transmitted_color = self._color_socket(self.in_transmitted_color)
        sock_transmitted_color_map = self._color_socket(self.in_transmitted_color_map)

        # Output Sockets
        sock_out_weight = self._float_socket(self.out_weight, in_out="OUTPUT")
        sock_out_volume = self._shader_socket(self.out_volume, in_out="OUTPUT")

        # Frames
        frame_weight = self.add_frame("Weight by Color Luminance", (0,0))

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-972, 0))

        # Nodes: Transmission
        mix_color_and_map = self._add_node__mix("Mix Color and Map", (-678, -87))
        self._link_socket(node_group_input, mix_color_and_map, sock_transmitted_color, 6)
        self._link_socket(node_group_input, mix_color_and_map, sock_transmitted_color_map, 7)

        node_luminance_mod = self._add_node("ShaderNodeRGB", "Apparent Luminance", (-679, 199), parent=frame_weight)
        self._set_socket(node_luminance_mod, 0, (0.2125, 0.7152, 0.0722, 1.0), "OUTPUT")

        node_norm_luminance = self._add_node__mix("Normalize Apparent Luminance", (-419, 228), parent=frame_weight)
        self._link_socket(mix_color_and_map, node_norm_luminance, 2, 6)
        self._link_socket(node_luminance_mod, node_norm_luminance, 0, 7)

        node_separate_luminance = self._add_node("ShaderNodeSeparateColor", "Separate Luminance", (-159, 171), parent=frame_weight)
        self._link_socket(node_norm_luminance, node_separate_luminance, 2, 0)

        node_lum_add_r_g = self._add_node__math("Luminance R+G", (360, 175), parent=frame_weight)
        self._link_socket(node_separate_luminance, node_lum_add_r_g, 0, 0)
        self._link_socket(node_separate_luminance, node_lum_add_r_g, 1, 1)

        node_lum_add_y_b = self._add_node__math("Luminance Y+B", (100, 175), parent=frame_weight)
        self._link_socket(node_lum_add_r_g, node_lum_add_y_b, 0, 0)
        self._link_socket(node_separate_luminance, node_lum_add_y_b, 2, 1)

        node_limit_min_dist = self._add_node__math("Limit Transmitted Distance", (-156, -139), "MAXIMUM")
        self._link_socket(node_group_input, node_limit_min_dist, sock_transmitted_measurement_distance, 0)
        self._set_socket(node_limit_min_dist, 1, 0.0001)

        node_vol_absorption = self._add_node("ShaderNodeVolumeAbsorption", "Volume Absorption", (103, -175))
        self._link_socket(mix_color_and_map, node_vol_absorption, 2, 0)
        self._link_socket(node_limit_min_dist, node_vol_absorption, 0, 1)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0, 0))
        self._link_socket(node_lum_add_y_b, node_group_output, 0, sock_out_weight)
        self._link_socket(node_vol_absorption, node_group_output, 0, sock_out_volume)
        # @formatter:on
