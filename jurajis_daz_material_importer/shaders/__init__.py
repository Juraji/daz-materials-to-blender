from typing import Type

from .iray_uber import IrayUberShaderGroupBuilder, IrayUberShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupBuilder, IWaveTranslucentFabricShaderGroupApplier
from .pbr_skin import PBRSkinShaderGroupBuilder, PBRSkinShaderGroupApplier
from .support import ShaderGroupBuilder, ShaderGroupApplier, AsymmetricalDisplacementShaderGroupBuilder, \
    DualLobeSpecularShaderGroupBuilder, BlackbodyEmissionShaderGroupBuilder, MetallicFlakesShaderGroupBuilder, \
    WeightedTranslucencyShaderGroupBuilder, FakeGlassShaderGroupBuilder, FakeGlassShaderGroupApplier, \
    GROUP_DESCRIPTION_PREFIX, AdvancedTopCoatShaderGroupBuilder

SHADER_GROUP_BUILDERS: list[Type[ShaderGroupBuilder]] = [
    # Helper Groups
    AdvancedTopCoatShaderGroupBuilder,
    AsymmetricalDisplacementShaderGroupBuilder,
    BlackbodyEmissionShaderGroupBuilder,
    DualLobeSpecularShaderGroupBuilder,
    FakeGlassShaderGroupBuilder,
    MetallicFlakesShaderGroupBuilder,
    WeightedTranslucencyShaderGroupBuilder,

    # Shaders
    PBRSkinShaderGroupBuilder,
    IrayUberShaderGroupBuilder,
    IWaveTranslucentFabricShaderGroupBuilder,
]

SHADER_GROUP_APPLIERS: list[Type[ShaderGroupApplier]] = [
    PBRSkinShaderGroupApplier,
    IrayUberShaderGroupApplier,
    IWaveTranslucentFabricShaderGroupApplier,
    FakeGlassShaderGroupApplier,
]
