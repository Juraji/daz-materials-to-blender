from .shader_group_applier import ShaderGroupApplier
from .library import MELANIN_DUAL_LOBE_HAIR
from ..utils.dson import DsonChannel


class MelaninDualLobeHairShaderApplier(ShaderGroupApplier):
    ATTRIB__ROOT_TO_TIP_GRADIENT = "blended_dual_lobe_hair_root_to_tip_gradient"

    # Base
    IN_BASE_ROOT_MELANIN = "Base Root Melanin"
    IN_BASE_ROOT_TINT = "Base Root Tint"
    IN_BASE_TIP_MELANIN = "Base Tip Melanin"
    IN_BASE_TIP_TINT = "Base Tip Tint"
    IN_BASE_MELANIN_REDNESS = "Base Melanin Redness"

    # Highlights
    IN_HIGHLIGHTS_WEIGHT = "Highlights Weight"
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
    IN_ROOT_TO_TIP_COORDINATES = "Root to Tip Coordinates"
    IN_ROOT_TO_TIP_BIAS = "Root to Tip Bias"
    IN_ROOT_TO_TIP_GAIN = "Root to Tip Gain"

    OUT_SURFACE = "Surface"

    @staticmethod
    def group_name() -> str:
        return MELANIN_DUAL_LOBE_HAIR

    @staticmethod
    def material_type_id() -> str:
        return "melanin_based_dual_lobe_blended_hair"

    def apply_shader_group(self, channels: dict[str, DsonChannel]):
        raise NotImplementedError(f"Group {self.group_name()} cannot directly be applied via import")
