from .shader_group_applier import ShaderGroupApplier
from .library import FAKE_GLASS
from ..utils.dson import DsonChannel


class IrayUberAsFakeGlassShaderGroupApplier(ShaderGroupApplier):
    IN_NORMAL = "Normal"
    IN_NORMAL_MAP = "Normal Map"
    IN_BUMP = "Bump"
    IN_BUMP_MAP = "Bump Map"

    OUT_SURFACE = "Surface"

    @staticmethod
    def group_name() -> str:
        return FAKE_GLASS

    @staticmethod
    def material_type_id() -> str:
        return "fake_glass"

    def apply_shader_group(self, channels: dict[str, DsonChannel]):
        super().apply_shader_group(channels)

        self._channel_to_sockets("bump_strength", self.IN_BUMP, self.IN_BUMP_MAP)
        self._channel_to_sockets("normal_map", self.IN_NORMAL, self.IN_NORMAL_MAP)

        # @formatter:off
        if self._channel_enabled("bump_strength"):
            self._set_socket(self._shader_group, self.IN_BUMP, self._properties.bump_strength_multiplier, "MULTIPLY")
        # @formatter:on
