from typing import Type

from .support.base import ShaderGroupBuilder, ShaderGroupApplier
from .iray_uber import IrayUberPBRMRShaderGroupBuilder, IrayUberPBRMRShaderGroupApplier
from .iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupBuilder, IWaveTranslucentFabricShaderGroupApplier
from .pbr_skin import PBRSkinShaderGroupBuilder, PBRSkinShaderGroupApplier
from .support.displacement import AsymmetricalDisplacementShaderGroupBuilder
from .support.dls import DualLobeSpecularShaderGroupBuilder
from .support.translucency import WeightedTranslucencyShaderGroupBuilder
from .support.transmission import WeightedTransmissonShaderGroupBuilder

SHADER_GROUP_BUILDERS: list[Type[ShaderGroupBuilder]] = [
    # Helper Groups
    DualLobeSpecularShaderGroupBuilder,
    AsymmetricalDisplacementShaderGroupBuilder,
    WeightedTranslucencyShaderGroupBuilder,
    WeightedTransmissonShaderGroupBuilder,

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
