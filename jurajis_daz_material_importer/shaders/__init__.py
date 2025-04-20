from typing import Type

from .iray_uber import IrayUberPBRMRShaderGroupBuilder, IrayUberPBRMRShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupBuilder, IWaveTranslucentFabricShaderGroupApplier
from .pbr_skin import PBRSkinShaderGroupBuilder, PBRSkinShaderGroupApplier
from .support.base import ShaderGroupBuilder, ShaderGroupApplier
from .support.displacement import AsymmetricalDisplacementShaderGroupBuilder
from .support.dls import DualLobeSpecularShaderGroupBuilder
from .support.emission import BlackbodyEmissionShaderGroupBuilder
from .support.metallic_flakes import MetallicFlakesShaderGroupBuilder
from .support.translucency import WeightedTranslucencyShaderGroupBuilder

SHADER_GROUP_BUILDERS: list[Type[ShaderGroupBuilder]] = [
    # Helper Groups
    AsymmetricalDisplacementShaderGroupBuilder,
    BlackbodyEmissionShaderGroupBuilder,
    DualLobeSpecularShaderGroupBuilder,
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
]