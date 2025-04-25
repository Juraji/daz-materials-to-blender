from bpy.types import ShaderNodeLightPath, ShaderNodeFresnel, ShaderNodeBsdfAnisotropic, ShaderNodeBsdfTransparent

from .base import SupportShaderGroupBuilder, ShaderGroupApplier

__GROUP_NAME__ = "Fake Glass"
__MATERIAL_TYPE_ID__ = "fake_glass"

from jurajis_daz_material_importer.utils.dson import DsonMaterialChannel


class FakeGlassShaderGroupBuilder(SupportShaderGroupBuilder):
    in_normal = "Normal"
    in_normal_map = "Normal Map"

    out_surface = "Surface"

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
        sock_normal = self._float_socket(self.in_normal, 1)
        sock_normal_map = self._color_socket(self.in_normal_map, (0.5, 0.5, 1.0, 1.0))

        # Output Sockets
        sock_out_surface = self._shader_socket(self.out_surface, in_out="OUTPUT")

        # Nodes: Group Input
        node_group_input = self._add_node__group_input("Group Input", (-1160, 0.0))

        # Nodes: Glass
        node_normal_map = self._add_node__normal_map("Normal", (-920, -80.0))
        self._link_socket(node_group_input, node_normal_map, sock_normal, 0)
        self._link_socket(node_group_input, node_normal_map, sock_normal_map, 1)

        node_light_path = self._add_node(ShaderNodeLightPath, "Light Path", (-920, 290.0))

        node_fresnel = self._add_node(ShaderNodeFresnel, "Fresnel", (-680, 70.0))
        self._set_socket(node_fresnel, 0, 40.0)
        self._link_socket(node_normal_map, node_fresnel, 0, 1)

        node_glossy = self._add_node(ShaderNodeBsdfAnisotropic, "Glossy BSDF", (-680, -70.0), props={"distribution": "GGX"})
        self._set_socket(node_glossy, 1, 0)
        self._link_socket(node_normal_map, node_glossy, 0, 4)

        node_transparent = self._add_node(ShaderNodeBsdfTransparent, "Transparent", (-680, -290.0))

        node_add_rays1 = self._add_node__math("Add Rays 1", (-680, 290.0))
        self._link_socket(node_light_path, node_add_rays1, 1, 0)
        self._link_socket(node_light_path, node_add_rays1, 2, 1)

        node_add_rays2 = self._add_node__math("Add Rays 2", (-420, 230.0))
        self._link_socket(node_add_rays1, node_add_rays2, 0, 0)
        self._link_socket(node_light_path, node_add_rays2, 3, 1)

        node_mix_shaders1 = self._add_node__mix_shader("Mix Shaders 1", (-420, 30.0))
        self._link_socket(node_fresnel, node_mix_shaders1, 0, 0)
        self._link_socket(node_glossy, node_mix_shaders1, 0, 1)
        self._link_socket(node_transparent, node_mix_shaders1, 0, 2)

        node_mix_shaders2 = self._add_node__mix_shader("Mix Shaders 2", (-200, 30.0))
        self._link_socket(node_add_rays2, node_mix_shaders2, 0, 0)
        self._link_socket(node_mix_shaders1, node_mix_shaders2, 0, 1)
        self._link_socket(node_transparent, node_mix_shaders2, 0, 2)

        # Group Output
        node_group_output = self._add_node__group_output("Group Output", (0, 0))
        self._link_socket(node_mix_shaders2, node_group_output, 0, sock_out_surface)
        # @formatter:on


class FakeGlassShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        builder = FakeGlassShaderGroupBuilder
        self._channel_to_sockets("normal_map", builder.in_normal, builder.in_normal_map)
