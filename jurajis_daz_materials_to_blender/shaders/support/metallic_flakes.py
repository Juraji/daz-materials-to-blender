from bpy.types import ShaderNodeTexVoronoi, ShaderNodeValToRGB

from .base import SupportShaderGroupBuilder

__GROUP_NAME__ = "Metallic Flakes"
__MATERIAL_TYPE_ID__ = "metallic_flakes"


class MetallicFlakesShaderGroupBuilder(SupportShaderGroupBuilder):
    in_weight = "Weight"
    in_weight_map = "Weight Map"
    in_color = "Color"
    in_color_map = "Color Map"
    in_roughness = "Roughness"
    in_roughness_map = "Roughness Map"
    in_flake_size = "Flake Size"
    in_flake_strength = "Flake Strength"
    in_flake_density = "Flake Density"
    in_normal = "Normal"

    out_fac = "Fac"
    out_shader = "Shader"

    flake_size_inverson_base = 50

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
        sock_weight = self._float_socket(self.in_weight, 1)
        sock_weight_map = self._color_socket(self.in_weight_map)
        sock_color = self._color_socket(self.in_color)
        sock_color_map = self._color_socket(self.in_color_map)
        sock_roughness = self._float_socket(self.in_roughness)
        sock_roughness_map = self._color_socket(self.in_roughness_map)
        sock_flake_size = self._float_socket(self.in_flake_size, 0.001)
        sock_flake_strength = self._float_socket(self.in_flake_strength, 1)
        sock_flake_density = self._float_socket(self.in_flake_density, 1)
        sock_normal = self._vector_socket(self.in_normal, (0.5, 0.5, 1.0))

        # Output Sockets
        sock_out_fac = self._float_socket(self.out_fac, in_out="OUTPUT")
        sock_out_shader = self._shader_socket(self.out_shader, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-1460.0, 0.0))

        # Nodes: Metallic Flakes
        node_mix_weight = self._add_node__hsv("Mix Weight and Map", (-460.0, 60.0))
        self._link_socket(node_group_input, node_mix_weight, sock_weight, 2)
        self._link_socket(node_group_input, node_mix_weight, sock_weight_map, 4)

        node_mix_color = self._add_node__mix("Mix Color and Map", (-740.0, -180.0))
        self._link_socket(node_group_input, node_mix_color, sock_color, 6)
        self._link_socket(node_group_input, node_mix_color, sock_color_map, 7)

        node_mix_roughness = self._add_node__mix("Mix Roughness and Map", (-740.0, -220.0))
        self._link_socket(node_group_input, node_mix_roughness, sock_roughness, 6)
        self._link_socket(node_group_input, node_mix_roughness, sock_roughness_map, 7)

        node_invert_flake_size = self._add_node__math("Invert Flake Size", (-1200.0, -260.0), "DIVIDE")
        self._set_socket(node_invert_flake_size, 0, self.flake_size_inverson_base)
        self._link_socket(node_group_input, node_invert_flake_size, sock_flake_size, 1)

        voronoi_props = {"distance": 'EUCLIDEAN', "feature": 'F1', "normalize": False, "voronoi_dimensions": '3D'}
        node_voronoi_tex = self._add_node(ShaderNodeTexVoronoi, "Voronoi Texture", (-1000.0, -260.0), props=voronoi_props)
        self._link_socket(node_invert_flake_size, node_voronoi_tex, 0, 2)
        self._set_socket(node_voronoi_tex, 3, 0)
        self._set_socket(node_voronoi_tex, 4, 0)
        self._set_socket(node_voronoi_tex, 5, 1)
        self._set_socket(node_voronoi_tex, 8, 1)

        node_voron_normal_vector_div = self._add_node__mix("Ruin Normals", (-740.0, -260.0), blend_type="DIVIDE", default_factor=0.1)
        self._link_socket(node_group_input, node_voron_normal_vector_div, sock_normal, 6)
        self._link_socket(node_voronoi_tex, node_voron_normal_vector_div, 1, 7)

        node_density_ramp = self._add_node(ShaderNodeValToRGB, "Density Ramp", (-740.0, 20.0))
        self._link_socket(node_voronoi_tex, node_density_ramp, 1,0)

        node_pick_visible_flakes = self._add_node__math("Pick Visible Flakes", (-460.0, -20.0), "LESS_THAN")
        self._link_socket(node_density_ramp, node_pick_visible_flakes, 0, 0)
        self._link_socket(node_group_input, node_pick_visible_flakes, sock_flake_density, 1)

        node_mix_weight_visible_flakes = self._add_node__math("Mix Weight and Visible Flakes", (-260.0, 20.0), "MULTIPLY")
        self._link_socket(node_mix_weight, node_mix_weight_visible_flakes, 0, 0)
        self._link_socket(node_pick_visible_flakes, node_mix_weight_visible_flakes, 0, 1)

        node_princ_bsdf = self._add_node__princ_bdsf("Principled BSDF", (-300.0, -120.0))
        self._link_socket(node_mix_color, node_princ_bsdf, 2, 0)
        self._link_socket(node_group_input, node_princ_bsdf, sock_flake_strength, 1)
        self._link_socket(node_mix_roughness, node_princ_bsdf, 2, 2)
        self._link_socket(node_voron_normal_vector_div, node_princ_bsdf, 2, 5)

        # Group Output
        node_group_output = self._add_node__group_output("NodeGroupOutput", (0, 0))
        self._link_socket(node_mix_weight_visible_flakes, node_group_output, 0, sock_out_fac)
        self._link_socket(node_princ_bsdf, node_group_output, 0, sock_out_shader)
        # @formatter:on

        self.hide_all_nodes(node_group_input,
                            node_princ_bsdf,
                            node_group_output)
