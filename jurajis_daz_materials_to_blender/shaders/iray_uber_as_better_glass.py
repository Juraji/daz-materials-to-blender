from . import ShaderGroupApplier
from .library import BETTER_GLASS
from ..utils.dson import DsonMaterialChannel


class IrayUberAsBetterGlassShaderGroupApplier(ShaderGroupApplier):
    IN_COLOR = "Color"
    IN_COLOR_MAP = "Color Map"
    IN_ROUGHNESS = "Roughness"
    IN_ROUGHNESS_MAP = "Roughness Map"
    IN_IOR = "IOR"
    IN_TRANSMISSION = "Transmission"
    IN_SHADOW_CONTRAST = "Shadow Contrast"

    IN_VECTOR = "Vector"
    IN_NORMAL = "Normal"
    IN_NORMAL_MAP = "Normal Map"
    IN_BUMP = "Bump"
    IN_BUMP_MAP = "Bump Map"

    IN_WAVE_PATTERN_ANGLE = "Wave Pattern Angle"
    IN_WAVE_PATTERN_SCALE = "Wave Pattern Scale"
    IN_WAVE_PATTERN_BUMP = "Wave Pattern Bump"

    @staticmethod
    def group_name() -> str:
        return BETTER_GLASS

    @staticmethod
    def material_type_id() -> str:
        return "better_glass"

    def apply_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        super().apply_shader_group(channels)

        self._link_socket(self._mapping, self._shader_group, 0, self.IN_VECTOR)

        if self._channel_enabled("diffuse_roughness"):
            self._channel_to_sockets("diffuse_roughness", self.IN_ROUGHNESS, self.IN_ROUGHNESS_MAP)
        elif self._channel_enabled("glossy_roughness"):
            self._channel_to_sockets("glossy_roughness", self.IN_ROUGHNESS, self.IN_ROUGHNESS_MAP)
        elif self._channel_enabled("glossy_color"):
            self._channel_to_sockets("glossy_color", self.IN_ROUGHNESS, self.IN_ROUGHNESS_MAP)

        self._channel_to_sockets("bump_strength", self.IN_BUMP, self.IN_BUMP_MAP)
        self._channel_to_sockets("normal_map", self.IN_NORMAL, self.IN_NORMAL_MAP)

        if self._channel_enabled("bump_strength"):
            self._set_socket(self._shader_group, self.IN_BUMP, self._properties.bump_strength_multiplier, "MULTIPLY")

        self._channel_to_sockets("refraction_index", self.IN_IOR, None)



