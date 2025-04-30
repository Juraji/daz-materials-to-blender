from .base import ShaderGroupApplier
from .library import FAKE_GLASS
from ..utils.dson import DsonMaterialChannel


class FakeGlassShaderGroupApplier(ShaderGroupApplier):
    IN_NORMAL = "Normal"
    IN_NORMAL_MAP = "Normal Map"

    OUT_SURFACE = "Surface"

    @staticmethod
    def group_name() -> str:
        return FAKE_GLASS

    @staticmethod
    def material_type_id() -> str:
        return "fake_glass"

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        self._channel_to_sockets("normal_map", self.IN_NORMAL, self.IN_NORMAL_MAP)
