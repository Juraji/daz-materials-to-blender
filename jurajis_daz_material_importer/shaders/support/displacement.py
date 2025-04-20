from .base import SupportShaderGroupBuilder

__GROUP_NAME__ = "Asymmetrical Displacement"
__MATERIAL_TYPE_ID__ = "displacement"


class AsymmetricalDisplacementShaderGroupBuilder(SupportShaderGroupBuilder):
    in_normal = "Normal"
    in_strength = "Strength"
    in_strength_map = "Strength Map"
    in_max_displacement = "Max Displacement"
    in_min_displacement = "Min Displacement"

    out_displacement = "Displacement"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def setup_group(self):
        super().setup_group()

        # Input Sockets
        sock_strength = self._float_socket(self.in_strength, 1)
        sock_strength_map = self._color_socket(self.in_strength_map)
        sock_min_displacement = self._float_socket(self.in_min_displacement)
        sock_max_displacement = self._float_socket(self.in_max_displacement)
        sock_normal = self._vector_socket(self.in_normal)

        # Output Sockets
        sock_out_displacement = self._vector_socket(self.out_displacement, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input('Group Input', (-764, 12))

        # Nodes: Asymmetrical Displacement
        node_adj_strength_min = self._add_node__math("Min Adjusted Strength", (-187, 119), "SUBTRACT")
        self._link_socket(node_group_input, node_adj_strength_min, sock_strength_map, 0)
        self._link_socket(node_group_input, node_adj_strength_min, sock_min_displacement, 1)

        node_norm_min_max = self._add_node__math("Normalized Min/Max", (-326, -84), "SUBTRACT")
        self._link_socket(node_group_input, node_norm_min_max, sock_max_displacement, 0)
        self._link_socket(node_group_input, node_norm_min_max, sock_min_displacement, 1)

        node_strength_div_norm = self._add_node__math("Strength / Normalized", (72, 118), "DIVIDE")
        self._link_socket(node_adj_strength_min, node_strength_div_norm, 0, 0)
        self._link_socket(node_norm_min_max, node_strength_div_norm, 0, 1)

        node_abs_min = self._add_node__math("Abs Min", (-66, -84), "MULTIPLY")
        self._link_socket(node_group_input, node_abs_min, sock_min_displacement, 0)
        self._set_socket(node_abs_min, 1, -1.0)

        node_norm_div_abs_min = self._add_node__math("Normalized / Abs Min", (193, -81), "DIVIDE")
        self._link_socket(node_norm_min_max, node_norm_div_abs_min, 0, 0)
        self._link_socket(node_abs_min, node_norm_div_abs_min, 0, 1)

        node_displacement = self._add_node("ShaderNodeDisplacement", "Displacement", (419, 39),
                                           props={"space": "OBJECT"})
        self._link_socket(node_strength_div_norm, node_displacement, 0, 0)
        self._link_socket(node_norm_div_abs_min, node_displacement, 0, 1)
        self._link_socket(node_group_input, node_displacement, sock_strength, 2)
        self._link_socket(node_group_input, node_displacement, sock_normal, 3)

        # Group Output
        node_group_output = self._add_node__group_output('Group Output', (609, 0))
        self._link_socket(node_displacement, node_group_output, 0, sock_out_displacement)
