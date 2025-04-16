from typing import Type

from .base import ShaderGroupBuilder, ShaderGroupApplier

# Shaders
from .dls import DualLobeSpecularShaderGroupBuilder
from .pbr_skin import PBRSkinShaderGroupBuilder, PBRSkinShaderGroupApplier
from .iray_uber import IrayUberShaderGroupBuilder, IrayUberShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupBuilder, IWaveTranslucentFabricShaderGroupApplier

SHADER_GROUP_BUILDERS: list[Type[ShaderGroupBuilder]] = [
    DualLobeSpecularShaderGroupBuilder,
    PBRSkinShaderGroupBuilder,
    IrayUberShaderGroupBuilder,
    IWaveTranslucentFabricShaderGroupBuilder,
]

SHADER_GROUP_APPLIERS: list[Type[ShaderGroupApplier]] = [
    PBRSkinShaderGroupApplier,
    IrayUberShaderGroupApplier,
    IWaveTranslucentFabricShaderGroupApplier,
]
