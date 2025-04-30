from typing import Type

from .base import ShaderGroupApplier
from .fake_glass import FakeGlassShaderGroupApplier
from .iray_uber import IrayUberShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupApplier
from .pbr_skin import PBRSkinShaderGroupApplier

SHADER_GROUP_APPLIERS: list[Type[ShaderGroupApplier]] = [
    FakeGlassShaderGroupApplier,
    IrayUberShaderGroupApplier,
    IWaveTranslucentFabricShaderGroupApplier,
    PBRSkinShaderGroupApplier,
]
