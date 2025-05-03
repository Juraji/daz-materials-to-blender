from bpy.types import ShaderNodeMapping, ShaderNodeUVMap, ShaderNodeOutputMaterial, ShaderNodeBsdfPrincipled

from ..utils.dson import DsonChannel
from .base import ShaderGroupApplier


class FallbackShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return "Unknown Material Fallback"

    @staticmethod
    def material_type_id() -> str:
        return "fallback"

    def apply_shader_group(self, channels: dict[str, DsonChannel]):
        self._channels: dict[str, DsonChannel] = {}

        # Setup base nodes
        self._uv_map = self._add_node(ShaderNodeUVMap, "UV Map",
                                      self.uv_map_location,
                                      props={"from_instancer": False, "uv_map": "UVMap"})
        self._mapping = self._add_node(ShaderNodeMapping, "Mapping",
                                       self.mapping_location,
                                       props={"vector_type": "POINT", "hide": True})
        self._material_ouput = self._add_node(ShaderNodeOutputMaterial, "Material Output",
                                              self.material_output_location,
                                              props={"is_active_output": True, "target": "ALL"})
        self._link_socket(self._uv_map, self._mapping, 0, 0)

        # Just add all images
        for _, ch in self._channels.items():
            if ch.has_image():
                self._add_image_texture(ch.image_file, False)

        # As a default white BSDF
        principled_bsdf = self._add_node(ShaderNodeBsdfPrincipled, "Principled BSDF", self.node_group_location)
        self._set_socket(principled_bsdf, 0, (1.0, 1.0, 1.0, 1.0))

        self._link_socket(principled_bsdf, self._material_ouput, 0, 0)
