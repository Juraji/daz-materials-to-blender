from .library import MELANIN_DUAL_LOBE_HAIR
from .shader_group_applier import ShaderGroupApplier
from ..utils.blended_hair_uv_processor import BlendedHairUVProcessor
from ..utils.dson import DsonChannel


class MelaninDualLobeHairShaderApplier(ShaderGroupApplier):
    FIXED_UV_NAME = "FixedHairUV"
    UV_STRAND_SPACING = 0.01

    # Base
    IN_BASE_ROOT_MELANIN = "Base Root Melanin"
    IN_BASE_ROOT_TINT = "Base Root Tint"
    IN_BASE_TIP_MELANIN = "Base Tip Melanin"
    IN_BASE_TIP_TINT = "Base Tip Tint"
    IN_BASE_MELANIN_REDNESS = "Base Melanin Redness"

    # Highlights
    IN_HIGHLIGHTS_WEIGHT = "Highlights Weight"
    IN_HIGHLIGHTS_SEPARATION = "Highlights Separation"
    IN_HIGHLIGHTS_ROOT_MELANIN = "Highlights Root Melanin"
    IN_HIGHLIGHTS_ROOT_TINT = "Highlights Root Tint"
    IN_HIGHLIGHTS_TIP_MELANIN = "Highlights Tip Melanin"
    IN_HIGHLIGHTS_TIP_TINT = "Highlights Tip Tint"
    IN_HIGHLIGHTS_MELANIN_REDNESS = "Highlights Melanin Redness"

    # Reflection
    IN_ROUGHNESS = "Roughness"
    IN_RADIAL_ROUGHNESS = "Radial Roughness"
    IN_GLOSSY_COAT = "Glossy Coat"
    IN_IOR = "IOR"

    # Geometry
    IN_VECTOR = "Vector"
    IN_ROOT_TO_TIP_BIAS = "Root to Tip Bias"
    IN_ROOT_TO_TIP_GAIN = "Root to Tip Gain"

    OUT_SURFACE = "Surface"

    @staticmethod
    def group_name() -> str:
        return MELANIN_DUAL_LOBE_HAIR

    @staticmethod
    def material_type_id() -> str:
        return "blended_dual_lobe_hair"

    def apply_shader_group(self, channels: dict[str, DsonChannel]):
        super().apply_shader_group(channels)

        processor = BlendedHairUVProcessor(self._b_object, self.FIXED_UV_NAME, self.UV_STRAND_SPACING)
        if not processor.uv_exists():
            processor.regenerate_uv()

        self._uv_map.uv_map = self.FIXED_UV_NAME

        # Base Melanin
        root_transmission_color = self._channel_value("root_transmission_color",
                                                      transform=lambda c: self._correct_color(c.as_rgba()))
        tip_transmission_color = self._channel_value("root_transmission_color",
                                                     transform=lambda c: self._correct_color(c.as_rgba()))

        root_melanin, root_redness = self._color_to_melanin(root_transmission_color)
        tip_melanin, tip_redness = self._color_to_melanin(tip_transmission_color)
        avg_redness = (root_redness + tip_redness) / 2

        self._channel_to_sockets("hair_root_color", self.IN_BASE_ROOT_TINT, None)
        self._channel_to_sockets("hair_tip_color", self.IN_BASE_TIP_TINT, None)
        self._set_socket(self._shader_group, self.IN_BASE_ROOT_MELANIN, root_melanin)
        self._set_socket(self._shader_group, self.IN_BASE_TIP_MELANIN, root_melanin)
        self._set_socket(self._shader_group, self.IN_BASE_MELANIN_REDNESS, avg_redness)

        # Highlight Melanin
        if self._channel_enabled("highlight_weight"):
            highlight_root_color = self._channel_value("highlight_root_color",
                                                       transform=lambda c: self._correct_color(c.as_rgba()))
            tip_highlight_color = self._channel_value("tip_highlight_color",
                                                      transform=lambda c: self._correct_color(c.as_rgba()))
            root_melanin, root_redness = self._color_to_melanin(highlight_root_color)
            tip_melanin, tip_redness = self._color_to_melanin(tip_highlight_color)
            avg_redness = (root_redness + tip_redness) / 2

            self._channel_to_sockets("highlight_weight", self.IN_HIGHLIGHTS_WEIGHT, None)
            self._channel_to_sockets("separation", self.IN_HIGHLIGHTS_SEPARATION, None)
            self._set_socket(self._shader_group, self.IN_HIGHLIGHTS_ROOT_MELANIN, root_melanin)
            self._set_socket(self._shader_group, self.IN_HIGHLIGHTS_TIP_MELANIN, tip_melanin)
            self._set_socket(self._shader_group, self.IN_HIGHLIGHTS_MELANIN_REDNESS, avg_redness)

        # Reflection
        self._channel_to_sockets("glossy_layer_weight", self.IN_GLOSSY_COAT, None)
        self._channel_to_sockets("base_roughness", self.IN_ROUGHNESS, None)

        # Geometry
        self._link_socket(self._mapping, self._shader_group, 0, self.IN_VECTOR)
        self._channel_to_sockets("root_to_tip_bias", self.IN_ROOT_TO_TIP_BIAS, None)
        self._channel_to_sockets("root_to_tip_gain", self.IN_ROOT_TO_TIP_GAIN, None)

    @classmethod
    def _color_to_melanin(cls, rgba: tuple[float, float, float, float]) -> tuple[float, float]:
        r, g, b, _ = rgba
        eps = 1e-6
        falloff = 0.15

        # 1) Compute linear luminance (Rec. 709)
        luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) ** falloff

        # 2) Melanin ≈ how far below white you are
        melanin = 1.0 - luminance
        melanin = max(0.0, min(1.0, melanin))

        # 3) Redness: how much red stands out *relative* to your melanin amount
        #    (if melanin is near zero, redness → 0)
        red_diff = r - (g + b) * 0.5
        redness = red_diff / (melanin + eps)
        redness = max(0.0, min(1.0, redness))

        return melanin, redness
