from bpy.types import BlendDataNodeTrees, ShaderNodeFresnel, ShaderNodeLayerWeight, ShaderNodeValToRGB, \
    ShaderNodeBsdfAnisotropic

from .base import SupportShaderGroupBuilder
from ...properties import MaterialImportProperties

__GROUP_NAME__ = "Advanced Top Coat"
__MATERIAL_TYPE_ID__ = "adv_top_coat"


class AdvancedTopCoatShaderGroupBuilder(SupportShaderGroupBuilder):
    """
    Glossy Top Coat Layer with IOR based fresnel and thin film aproximation.

    How thin fil is done:
    Let d = film thickness, n = IOR, Θ = view angle, R = Iridescent rotations
    Refraction: δ = (4πd.n.sin(Θ))/λ
    Our approx.: sin((d/2000).Θ.n.R) which rotates the color along a spectrum
    """

    in_top_coat_weight = "Top Coat Weight"
    in_top_coat_weight_map = "Top Coat Weight Map"
    in_top_coat_color = "Top Coat Color"
    in_top_coat_color_map = "Top Coat Color Map"
    in_top_coat_roughness = "Top Coat Roughness"
    in_top_coat_roughness_map = "Top Coat Roughness Map"
    in_top_coat_reflectivity = "Top Coat Reflectivity"
    in_top_coat_reflectivity_map = "Top Coat Reflectivity Map"
    in_top_coat_normal = "Top Coat Normal"
    in_top_coat_normal_map = "Top Coat Normal Map"
    in_top_coat_bump = "Top Coat Bump"
    in_top_coat_bump_map = "Top Coat Bump Map"
    in_top_coat_bump_vector = "Top Coat Bump Vector"
    in_top_coat_anisotropy = "Top Coat Anisotropy"
    in_top_coat_anisotropy_map = "Top Coat Anisotropy Map"
    in_top_coat_rotations = "Top Coat Rotations"
    in_top_coat_rotations_map = "Top Coat Rotations Map"

    in_thin_film_weight = "Thin Film Weight"
    in_thin_film_rotations = "Thin Film Iridescent Rotations"
    in_thin_film_thickness = "Thin Film Thickness"
    in_thin_film_thickness_map = "Thin Film Thickness Map"
    in_thin_film_ior = "Thin Film Ior"
    in_thin_film_ior_map = "Thin Film Ior Map"

    out_fac = "Fac"
    out_shader = "Shader"

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def __init__(self, properties: MaterialImportProperties, node_trees: BlendDataNodeTrees):
        super().__init__(properties, node_trees)

    def setup_group(self):
        super().setup_group()

        # Input Sockets
        panel_top_coat = self._add_panel("Top Coat", False)
        panel_thin_film = self._add_panel("Thin Film", False)

        # Sockets: Top Coat
        sock_top_coat_weight = self._float_socket(self.in_top_coat_weight, parent=panel_top_coat)
        sock_top_coat_weight_map = self._color_socket(self.in_top_coat_weight_map, parent=panel_top_coat)
        sock_top_coat_color = self._color_socket(self.in_top_coat_color, parent=panel_top_coat)
        sock_top_coat_color_map = self._color_socket(self.in_top_coat_color_map, parent=panel_top_coat)
        sock_top_coat_roughness = self._float_socket(self.in_top_coat_roughness, parent=panel_top_coat)
        sock_top_coat_roughness_map = self._color_socket(self.in_top_coat_roughness_map, parent=panel_top_coat)
        sock_top_coat_reflectivity = self._float_socket(self.in_top_coat_reflectivity, parent=panel_top_coat)
        sock_top_coat_reflectivity_map = self._color_socket(self.in_top_coat_reflectivity_map, (0.5, 0.5, 1.0, 1.0), parent=panel_top_coat)
        sock_top_coat_normal = self._float_socket(self.in_top_coat_normal, 0, parent=panel_top_coat)
        sock_top_coat_normal_map = self._color_socket(self.in_top_coat_normal_map, (0.5, 0.5, 1.0, 1.0), parent=panel_top_coat)
        sock_top_coat_bump = self._float_socket(self.in_top_coat_bump, 0, parent=panel_top_coat)
        sock_top_coat_bump_map = self._color_socket(self.in_top_coat_bump_map, parent=panel_top_coat)
        sock_top_coat_normal_and_bump_vector = self._vector_socket(self.in_top_coat_bump_vector,
                                                                   (0.5, 0.5, 1.0), parent=panel_top_coat)
        sock_top_coat_anisotropy = self._float_socket(self.in_top_coat_anisotropy, parent=panel_top_coat)
        sock_top_coat_anisotropy_map = self._color_socket(self.in_top_coat_anisotropy_map, parent=panel_top_coat)
        sock_top_coat_rotations = self._float_socket(self.in_top_coat_rotations, parent=panel_top_coat)
        sock_top_coat_rotations_map = self._color_socket(self.in_top_coat_rotations_map, parent=panel_top_coat)

        # Sockets: Thin Film
        sock_thin_film_weight = self._float_socket(self.in_thin_film_weight, parent=panel_thin_film)
        sock_thin_film_rotations = self._float_socket(self.in_thin_film_rotations, 30, parent=panel_thin_film)
        sock_thin_film_thickness = self._float_socket(self.in_thin_film_thickness, parent=panel_thin_film)
        sock_thin_film_thickness_map = self._color_socket(self.in_thin_film_thickness_map, parent=panel_thin_film)
        sock_thin_film_ior = self._float_socket(self.in_thin_film_ior, 1.5, parent=panel_thin_film)
        sock_thin_film_ior_map = self._color_socket(self.in_thin_film_ior_map, parent=panel_thin_film)

        # Output Sockets
        sock_out_fac = self._float_socket(self.out_fac, in_out="OUTPUT")
        sock_out_shader = self._shader_socket(self.out_shader, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input('Group Input', (-1360.0, 0.0))

        # Nodes: Top Coat Calculations
        node_mix_tc_color = self._add_node__mix("Mix TC Color", (-1080.0, -180.0))
        self._link_socket(node_group_input, node_mix_tc_color, sock_top_coat_color, 6)
        self._link_socket(node_group_input, node_mix_tc_color, sock_top_coat_color_map, 7)

        node_mix_tc_reflectivity = self._add_node__hsv("Mix TC Reflectivity", (-1080.0, -220))
        self._link_socket(node_group_input, node_mix_tc_reflectivity, sock_top_coat_reflectivity, 2)
        self._link_socket(node_group_input, node_mix_tc_reflectivity, sock_top_coat_reflectivity_map, 4)

        node_mix_tc_roughness = self._add_node__hsv("Mix TC Roughness", (-1080.0, -260))
        self._link_socket(node_group_input, node_mix_tc_roughness, sock_top_coat_roughness, 2)
        self._link_socket(node_group_input, node_mix_tc_roughness, sock_top_coat_roughness_map, 4)

        node_mix_tc_anisotropy = self._add_node__hsv("Mix TC Anisotropy", (-1080.0, -300))
        self._link_socket(node_group_input, node_mix_tc_anisotropy, sock_top_coat_anisotropy, 2)
        self._link_socket(node_group_input, node_mix_tc_anisotropy, sock_top_coat_anisotropy_map, 4)

        node_mix_tc_rotations = self._add_node__hsv("Mix TC Rotations", (-1080.0, -340))
        self._link_socket(node_group_input, node_mix_tc_rotations, sock_top_coat_rotations, 2)
        self._link_socket(node_group_input, node_mix_tc_rotations, sock_top_coat_rotations_map, 4)

        node_mix_tc_weight = self._add_node__hsv("Mix TC Weight", (-1080.0, -380))
        self._link_socket(node_group_input, node_mix_tc_weight, sock_top_coat_weight, 2)
        self._link_socket(node_group_input, node_mix_tc_weight, sock_top_coat_weight_map, 4)

        node_tc_normal_map = self._add_node__normal_map("TC Normal Map", (-1080.0, -420))
        self._link_socket(node_group_input, node_tc_normal_map, sock_top_coat_normal, 0)
        self._link_socket(node_group_input, node_tc_normal_map, sock_top_coat_normal_map, 1)

        node_tc_bump = self._add_node__bump("TC Bump", (-1080.0, -460))
        self._link_socket(node_group_input, node_tc_bump, sock_top_coat_bump, 0)
        self._link_socket(node_group_input, node_tc_bump, sock_top_coat_bump_map, 2)
        self._link_socket(node_tc_normal_map, node_tc_bump, 0, 3)

        node_mix_tc_bump_vector = self._add_node__math_vector("Mix TC Bump Vector", (-1080.0, -500))
        self._link_socket(node_tc_bump, node_mix_tc_bump_vector, 0, 0)
        self._link_socket(node_group_input, node_mix_tc_bump_vector, sock_top_coat_normal_and_bump_vector, 1)

        node_tc_ior = self._add_node__math("TC IOR", (-660.0, -420.0))
        self._set_socket(node_tc_ior, 0, 1.0)
        self._link_socket(node_mix_tc_reflectivity, node_tc_ior, 0, 1)

        node_tc_fresnel = self._add_node(ShaderNodeFresnel, "TC Fresnel", (-460.0, -420.0))
        self._link_socket(node_tc_ior, node_tc_fresnel, 0, 0)
        self._link_socket(node_mix_tc_bump_vector, node_tc_fresnel, 0, 1)

        # Nodes: Thin Film Calculations
        node_mix_tf_thickness = self._add_node__hsv("Mix TF Thickness", (-1080.0, -20.0))
        self._link_socket(node_group_input, node_mix_tf_thickness, sock_thin_film_thickness, 2)
        self._link_socket(node_group_input, node_mix_tf_thickness, sock_thin_film_thickness_map, 4)

        node_tf_layer_weight = self._add_node(ShaderNodeLayerWeight, "TF Layer Weight", (-1080.0, -60.0))
        self._link_socket(node_mix_tc_bump_vector, node_tf_layer_weight, 0, 1)

        node_mix_tf_ior = self._add_node__hsv("Mix TF IOR", (-1080.0, -100.0))
        self._link_socket(node_group_input, node_mix_tf_ior, sock_thin_film_ior, 2)
        self._link_socket(node_group_input, node_mix_tf_ior, sock_thin_film_ior_map, 4)

        node_tf_calc_step1 = self._add_node__math("TF Refraction nm > d", (-800.0, 20.0), "DIVIDE")
        self._link_socket(node_mix_tf_thickness, node_tf_calc_step1, 0, 0)
        self._set_socket(node_tf_calc_step1, 1, 2000.0)

        node_tf_calc_step2 = self._add_node__math("TF Refraction Θ·d", (-800.0, -20.0), "MULTIPLY")
        self._link_socket(node_tf_calc_step1, node_tf_calc_step2, 0, 0)
        self._link_socket(node_tf_layer_weight, node_tf_calc_step2, 1, 1)

        node_tf_calc_step3 = self._add_node__math("TF Refraction Θd·n", (-800.0, -60.0), "MULTIPLY")
        self._link_socket(node_tf_calc_step2, node_tf_calc_step3, 0, 0)
        self._link_socket(node_mix_tf_ior, node_tf_calc_step3, 0, 1)

        node_tf_calc_step4 = self._add_node__math("TF Refraction Θdn·R", (-800.0, -100.0), "MULTIPLY")
        self._link_socket(node_tf_calc_step3, node_tf_calc_step4, 0, 0)
        self._link_socket(node_group_input, node_tf_calc_step4, sock_thin_film_rotations, 1)

        node_tf_calc_step5 = self._add_node__math("TF Refraction sin(ΘdnR)", (-800.0, -140.0), "SINE")
        self._link_socket(node_tf_calc_step4, node_tf_calc_step5, 0, 0)

        node_tf_spectrum = self._add_node(ShaderNodeValToRGB, "TF Refreaction Spectrum", (-800.0, -180.0))
        self._setup_spectrum_in(node_tf_spectrum)
        self._link_socket(node_tf_calc_step5, node_tf_spectrum, 0, 0)

        # Nodes: Combine TC and TF
        node_mix_tc_tf_color = self._add_node__mix("Mix TC and TF", (-460.0, -200.0), blend_type="MIX")
        self._link_socket(node_group_input, node_mix_tc_tf_color, sock_thin_film_weight, 0)
        self._link_socket(node_mix_tc_color, node_mix_tc_tf_color, 2, 6)
        self._link_socket(node_tf_spectrum, node_mix_tc_tf_color, 0, 7)

        # Nodes: BSDF and Fac
        node_bsdf = self._add_node(ShaderNodeBsdfAnisotropic, "TC Glossy BSDF", (-260.0, -240.0))
        self._link_socket(node_mix_tc_tf_color, node_bsdf, 2, 0)
        self._link_socket(node_mix_tc_roughness, node_bsdf, 0, 1)
        self._link_socket(node_mix_tc_anisotropy, node_bsdf, 0, 2)
        self._link_socket(node_mix_tc_rotations, node_bsdf, 0, 3)
        self._link_socket(node_mix_tc_bump_vector, node_bsdf, 0, 4)

        node_fac = self._add_node__math("Top Coat Fac", (-260.0, -280.0), "MULTIPLY")
        self._link_socket(node_mix_tc_weight, node_fac, 0, 0)
        self._link_socket(node_tc_fresnel, node_fac, 0, 1)

        # Group Output
        node_group_output = self._add_node__group_output('Group Output', (0, 0))
        self._link_socket(node_bsdf, node_group_output, 0, sock_out_shader)
        self._link_socket(node_fac, node_group_output, 0, sock_out_fac)

        self.hide_all_nodes(node_group_input, node_group_output)

    @staticmethod
    def _setup_spectrum_in(node: ShaderNodeValToRGB):
        ramp = node.color_ramp
        # Clear any existing elements first, keeping the first one to avoid index errors
        while len(ramp.elements) > 1:
            ramp.elements.remove(ramp.elements[-1])

        spectrum_points = [
            (0.0, (0.0, 0.0, 1.0, 1.0)),  # Blue
            (0.333, (0.0, 1.0, 0.0, 1.0)),  # Green
            (0.667, (1.0, 0.0, 0.0, 1.0)),  # Red
            (1.0, (0.0, 0.0, 1.0, 1.0)),  # Blue again
        ]

        for i, (pos, color) in enumerate(spectrum_points):
            if i == 0:
                elem = ramp.elements[0]
            else:
                elem = ramp.elements.new(pos)
            elem.position = pos
            elem.color = color
            elem.alpha = 1.0
