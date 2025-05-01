from typing import Type

from .base import ShaderGroupApplier
from .blended_dual_lobe_hair import BlendedDualLobeHairShaderApplier
from .iray_uber_as_fake_glass import IrayUberAsFakeGlassShaderGroupApplier
from .iray_uber import IrayUberShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupApplier
from .pbr_skin import PBRSkinShaderGroupApplier

SHADER_GROUP_APPLIERS: list[Type[ShaderGroupApplier]] = [
    BlendedDualLobeHairShaderApplier,
    IrayUberAsFakeGlassShaderGroupApplier,
    IrayUberShaderGroupApplier,
    IWaveTranslucentFabricShaderGroupApplier,
    PBRSkinShaderGroupApplier,
]
