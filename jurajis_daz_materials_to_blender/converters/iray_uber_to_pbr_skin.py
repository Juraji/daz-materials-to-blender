from typing import Type

from .shader_group_converter import ShaderGroupConverter
from ..shaders import IrayUberShaderGroupApplier, PBRSkinShaderGroupApplier, ShaderGroupApplier


class IrayUberToPbrSkinShaderConverter(ShaderGroupConverter):
    @staticmethod
    def from_type() -> Type[ShaderGroupApplier]:
        return IrayUberShaderGroupApplier

    @staticmethod
    def to_type() -> Type[ShaderGroupApplier]:
        return PBRSkinShaderGroupApplier

    @staticmethod
    def display_name() -> str:
        return "Iray Uber To PBR Skin"

    @staticmethod
    def property_mapping() -> list[tuple[str, str]]:
        iray = IrayUberShaderGroupApplier
        pbr = PBRSkinShaderGroupApplier

        return [
            (iray.IN_DIFFUSE, pbr.IN_DIFFUSE_COLOR),
            (iray.IN_DIFFUSE_MAP, pbr.IN_DIFFUSE_COLOR_MAP),
            (iray.IN_DIFFUSE_ROUGHNESS, pbr.IN_ROUGHNESS),
            (iray.IN_DIFFUSE_ROUGHNESS_MAP, pbr.IN_ROUGHNESS_MAP),
            (iray.IN_METALLIC_WEIGHT, pbr.IN_METALLIC),
            (iray.IN_METALLIC_WEIGHT_MAP, pbr.IN_METALLIC_MAP),
            (iray.IN_CUTOUT_OPACITY, pbr.IN_OPACITY),
            (iray.IN_CUTOUT_OPACITY_MAP, pbr.IN_OPACITY_MAP),
            (iray.IN_DUAL_LOBE_SPECULAR_WEIGHT, pbr.IN_DLS_WEIGHT),
            (iray.IN_DUAL_LOBE_SPECULAR_WEIGHT_MAP, pbr.IN_DLS_WEIGHT_MAP),
            (iray.IN_DUAL_LOBE_SPECULAR_REFLECTIVITY, pbr.IN_DLS_REFLECTIVITY),
            (iray.IN_DUAL_LOBE_SPECULAR_REFLECTIVITY_MAP, pbr.IN_DLS_REFLECTIVITY_MAP),
            (iray.IN_SPECULAR_LOBE_1_ROUGHNESS, pbr.IN_DLS_L1_ROUGHNESS),
            (iray.IN_SPECULAR_LOBE_1_ROUGHNESS_MAP, pbr.IN_DLS_L1_ROUGHNESS_MAP),
            (iray.IN_SPECULAR_LOBE_2_ROUGHNESS, pbr.IN_DLS_L2_ROUGHNESS_MULT),
            (iray.IN_SPECULAR_LOBE_2_ROUGHNESS_MAP, pbr.IN_DLS_L2_ROUGHNESS_MULT_MAP),
            (iray.IN_DUAL_LOBE_SPECULAR_RATIO, pbr.IN_DLS_RATIO),
            (iray.IN_DUAL_LOBE_SPECULAR_RATIO_MAP, pbr.IN_DLS_RATIO_MAP),
            (iray.IN_SSS_WEIGHT, pbr.IN_SSS_WEIGHT),
            (iray.IN_SCATTERING_MEASUREMENT_DISTANCE, pbr.IN_SSS_SCALE),
            (iray.IN_SSS_DIRECTION, pbr.IN_SSS_DIRECTION),
            (iray.IN_NORMAL, pbr.IN_NORMAL_WEIGHT),
            (iray.IN_NORMAL_MAP, pbr.IN_NORMAL_MAP),
            (iray.IN_BUMP_STRENGTH, pbr.IN_BUMP_STRENGTH),
            (iray.IN_BUMP_STRENGTH_MAP, pbr.IN_BUMP_STRENGTH_MAP),
            (iray.IN_TOP_COAT_WEIGHT, pbr.IN_TOP_COAT_WEIGHT),
            (iray.IN_TOP_COAT_WEIGHT_MAP, pbr.IN_TOP_COAT_WEIGHT_MAP),
            (iray.IN_TOP_COAT_ROUGHNESS, pbr.IN_TOP_COAT_ROUGHNESS),
            (iray.IN_TOP_COAT_ROUGHNESS_MAP, pbr.IN_TOP_COAT_ROUGHNESS_MAP),
            (iray.IN_TOP_COAT_COLOR, pbr.IN_TOP_COAT_COLOR),
            (iray.IN_TOP_COAT_COLOR_MAP, pbr.IN_TOP_COAT_COLOR_MAP),
        ]
