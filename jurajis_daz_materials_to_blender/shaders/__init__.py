from typing import Type

from .iray_uber import IrayUberShaderGroupApplier
from .iray_uber_as_fake_glass import IrayUberAsFakeGlassShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupApplier
from .melanin_dual_lobe_hair import MelaninDualLobeHairShaderApplier
from .pbr_skin import PBRSkinShaderGroupApplier
from .shader_group_applier import ShaderGroupApplier

SHADER_GROUP_APPLIERS: list[Type[ShaderGroupApplier]] = [
    IWaveTranslucentFabricShaderGroupApplier,
    IrayUberAsFakeGlassShaderGroupApplier,
    IrayUberShaderGroupApplier,
    MelaninDualLobeHairShaderApplier,
    PBRSkinShaderGroupApplier,
]
