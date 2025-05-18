from typing import Type

from .iray_uber_to_iwave import IrayUberToIWaveFabricShaderConverter
from .iray_uber_to_pbr_skin import IrayUberToPbrSkinShaderConverter
from .shader_group_converter import ShaderGroupConverter

SHADER_GROUP_CONVERTERS: list[Type[ShaderGroupConverter]] = [
    IrayUberToPbrSkinShaderConverter,
    IrayUberToIWaveFabricShaderConverter,
]

SHADER_GROUP_CONVERTERS_ENUM_OPTS = [
    (c.__name__, c.display_name, "", i) for i, c in enumerate(SHADER_GROUP_CONVERTERS)
]

def converter_by_cls_name(cls: str) -> Type[ShaderGroupConverter]:
    return next(c for c in SHADER_GROUP_CONVERTERS if c.__name__ == cls)