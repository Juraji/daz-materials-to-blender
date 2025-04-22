from typing import Type

from .iray_uber import IrayUberPBRMRShaderGroupBuilder, IrayUberPBRMRShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupBuilder, IWaveTranslucentFabricShaderGroupApplier
from .pbr_skin import PBRSkinShaderGroupBuilder, PBRSkinShaderGroupApplier
from .support import ShaderGroupBuilder, ShaderGroupApplier, AsymmetricalDisplacementShaderGroupBuilder, \
    DualLobeSpecularShaderGroupBuilder, BlackbodyEmissionShaderGroupBuilder, MetallicFlakesShaderGroupBuilder, \
    WeightedTranslucencyShaderGroupBuilder, FakeGlassShaderGroupBuilder, FakeGlassShaderGroupApplier

SHADER_GROUP_BUILDERS: list[Type[ShaderGroupBuilder]] = [
    # Helper Groups
    AsymmetricalDisplacementShaderGroupBuilder,
    BlackbodyEmissionShaderGroupBuilder,
    DualLobeSpecularShaderGroupBuilder,
    FakeGlassShaderGroupBuilder,
    MetallicFlakesShaderGroupBuilder,
    WeightedTranslucencyShaderGroupBuilder,

    # Shaders
    PBRSkinShaderGroupBuilder,
    IrayUberPBRMRShaderGroupBuilder,
    IWaveTranslucentFabricShaderGroupBuilder,
]

SHADER_GROUP_APPLIERS: list[Type[ShaderGroupApplier]] = [
    PBRSkinShaderGroupApplier,
    IrayUberPBRMRShaderGroupApplier,
    IWaveTranslucentFabricShaderGroupApplier,
    FakeGlassShaderGroupApplier,
]
