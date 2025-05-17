from .shader_group_converter import ShaderGroupConverter
from ..shaders import IrayUberShaderGroupApplier, PBRSkinShaderGroupApplier, ShaderGroupApplier


class IrayUberToPbrSkinShaderConverter(ShaderGroupConverter):
    from_type = IrayUberShaderGroupApplier
    to_type = PBRSkinShaderGroupApplier
    display_name = "Iray Uber To PBR Skin"

    @classmethod
    def property_mapping(cls) -> list[tuple[str, str]]:
        i = cls.from_type
        o = cls.to_type

        return [
            (i.IN_DIFFUSE, o.IN_DIFFUSE_COLOR),
            (i.IN_DIFFUSE_MAP, o.IN_DIFFUSE_COLOR_MAP),
            (i.IN_DIFFUSE_ROUGHNESS, o.IN_ROUGHNESS),
            (i.IN_DIFFUSE_ROUGHNESS_MAP, o.IN_ROUGHNESS_MAP),
            (i.IN_METALLIC_WEIGHT, o.IN_METALLIC),
            (i.IN_METALLIC_WEIGHT_MAP, o.IN_METALLIC_MAP),
            (i.IN_CUTOUT_OPACITY, o.IN_OPACITY),
            (i.IN_CUTOUT_OPACITY_MAP, o.IN_OPACITY_MAP),
            (i.IN_DUAL_LOBE_SPECULAR_WEIGHT, o.IN_DLS_WEIGHT),
            (i.IN_DUAL_LOBE_SPECULAR_WEIGHT_MAP, o.IN_DLS_WEIGHT_MAP),
            (i.IN_DUAL_LOBE_SPECULAR_REFLECTIVITY, o.IN_DLS_REFLECTIVITY),
            (i.IN_DUAL_LOBE_SPECULAR_REFLECTIVITY_MAP, o.IN_DLS_REFLECTIVITY_MAP),
            (i.IN_SPECULAR_LOBE_1_ROUGHNESS, o.IN_DLS_L1_ROUGHNESS),
            (i.IN_SPECULAR_LOBE_1_ROUGHNESS_MAP, o.IN_DLS_L1_ROUGHNESS_MAP),
            (i.IN_SPECULAR_LOBE_2_ROUGHNESS, o.IN_DLS_L2_ROUGHNESS_MULT),
            (i.IN_SPECULAR_LOBE_2_ROUGHNESS_MAP, o.IN_DLS_L2_ROUGHNESS_MULT_MAP),
            (i.IN_DUAL_LOBE_SPECULAR_RATIO, o.IN_DLS_RATIO),
            (i.IN_DUAL_LOBE_SPECULAR_RATIO_MAP, o.IN_DLS_RATIO_MAP),
            (i.IN_SSS_WEIGHT, o.IN_SSS_WEIGHT),
            (i.IN_SCATTERING_MEASUREMENT_DISTANCE, o.IN_SSS_SCALE),
            (i.IN_SSS_DIRECTION, o.IN_SSS_DIRECTION),
            (i.IN_NORMAL, o.IN_NORMAL_WEIGHT),
            (i.IN_NORMAL_MAP, o.IN_NORMAL_MAP),
            (i.IN_BUMP_STRENGTH, o.IN_BUMP_STRENGTH),
            (i.IN_BUMP_STRENGTH_MAP, o.IN_BUMP_STRENGTH_MAP),
            (i.IN_TOP_COAT_WEIGHT, o.IN_TOP_COAT_WEIGHT),
            (i.IN_TOP_COAT_WEIGHT_MAP, o.IN_TOP_COAT_WEIGHT_MAP),
            (i.IN_TOP_COAT_ROUGHNESS, o.IN_TOP_COAT_ROUGHNESS),
            (i.IN_TOP_COAT_ROUGHNESS_MAP, o.IN_TOP_COAT_ROUGHNESS_MAP),
            (i.IN_TOP_COAT_COLOR, o.IN_TOP_COAT_COLOR),
            (i.IN_TOP_COAT_COLOR_MAP, o.IN_TOP_COAT_COLOR_MAP),
        ]
