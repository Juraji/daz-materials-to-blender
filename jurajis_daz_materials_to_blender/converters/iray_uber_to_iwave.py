from typing import Type

from .shader_group_converter import ShaderGroupConverter
from ..shaders import ShaderGroupApplier, IrayUberShaderGroupApplier, IWaveTranslucentFabricShaderGroupApplier


class IrayUberToIWaveFabricShaderConverter(ShaderGroupConverter):
    @staticmethod
    def from_type() -> Type[ShaderGroupApplier]:
        return IrayUberShaderGroupApplier

    @staticmethod
    def to_type() -> Type[ShaderGroupApplier]:
        return IWaveTranslucentFabricShaderGroupApplier

    @staticmethod
    def display_name() -> str:
        return "Iray Uber To IWave Translucent Fabric"

    @staticmethod
    def property_mapping() -> list[tuple[str, str]]:
        iray = IrayUberShaderGroupApplier
        iwave = IWaveTranslucentFabricShaderGroupApplier

        return [
            (iray.IN_DIFFUSE, iwave.IN_DIFFUSE),
            (iray.IN_DIFFUSE_MAP, iwave.IN_DIFFUSE_MAP),

            (iray.IN_NORMAL, iwave.IN_BASE_NORMAL),
            (iray.IN_NORMAL_MAP, iwave.IN_BASE_NORMAL_MAP),
            (iray.IN_BUMP_STRENGTH, iwave.IN_BASE_BUMP),
            (iray.IN_BUMP_STRENGTH_MAP, iwave.IN_BASE_BUMP_MAP),

            (iray.IN_DIFFUSE_OVERLAY_WEIGHT, iwave.IN_FIBER_LAYER_WEIGHT),
            (iray.IN_DIFFUSE_OVERLAY_WEIGHT_MAP, iwave.IN_FIBER_LAYER_WEIGHT_MAP),
            (iray.IN_DIFFUSE_OVERLAY_COLOR, iwave.IN_FIBER_LAYER_COLOR),
            (iray.IN_DIFFUSE_OVERLAY_COLOR_MAP, iwave.IN_FIBER_LAYER_COLOR_MAP),
            (iray.IN_DIFFUSE_OVERLAY_ROUGHNESS, iwave.IN_FIBER_LAYER_ROUGHNESS),
            (iray.IN_DIFFUSE_OVERLAY_ROUGHNESS_MAP, iwave.IN_FIBER_LAYER_ROUGHNESS_MAP),

            (iray.IN_CUTOUT_OPACITY, iwave.IN_CUTOUT_OPACITY),
            (iray.IN_CUTOUT_OPACITY_MAP, iwave.IN_CUTOUT_OPACITY_MAP),
            (iray.IN_DISPLACEMENT_STRENGTH, iwave.IN_DISPLACEMENT_STRENGTH),
            (iray.IN_DISPLACEMENT_STRENGTH_MAP, iwave.IN_DISPLACEMENT_STRENGTH_MAP),
            (iray.IN_MINIMUM_DISPLACEMENT, iwave.IN_MINIMUM_DISPLACEMENT),
            (iray.IN_MAXIMUM_DISPLACEMENT, iwave.IN_MAXIMUM_DISPLACEMENT),

            (iray.IN_GLOSSY_WEIGHT, iwave.IN_GLOSSY_LAYERED_WEIGHT),
            (iray.IN_GLOSSY_WEIGHT_MAP, iwave.IN_GLOSSY_LAYERED_WEIGHT_MAP),
            (iray.IN_GLOSSY_COLOR, iwave.IN_GLOSSY_COLOR),
            (iray.IN_GLOSSY_COLOR_MAP, iwave.IN_GLOSSY_COLOR_MAP),
            (iray.IN_GLOSSY_REFLECTIVITY, iwave.IN_GLOSSY_REFLECTIVITY),
            (iray.IN_GLOSSY_REFLECTIVITY_MAP, iwave.IN_GLOSSY_REFLECTIVITY_MAP),
            (iray.IN_GLOSSY_ROUGHNESS, iwave.IN_GLOSSY_ROUGHNESS),
            (iray.IN_GLOSSY_ROUGHNESS_MAP, iwave.IN_GLOSSY_ROUGHNESS_MAP),

            (iray.IN_DIFFUSE, iwave.IN_GRADIENT_LAYER_GRAZING_COLOR),
            (iray.IN_DIFFUSE_MAP, iwave.IN_GRADIENT_LAYER_GRAZING_COLOR_MAP),
            (iray.IN_DIFFUSE, iwave.IN_GRADIENT_LAYER_NORMAL_TINT),
            (iray.IN_DIFFUSE_MAP, iwave.IN_GRADIENT_LAYER_NORMAL_TINT_MAP),

            (iray.IN_METALLIC_FLAKES_WEIGHT, iwave.IN_METALLIC_FLAKES_WEIGHT),
            (iray.IN_METALLIC_FLAKES_WEIGHT_MAP, iwave.IN_METALLIC_FLAKES_WEIGHT_MAP),
            (iray.IN_METALLIC_FLAKES_COLOR, iwave.IN_METALLIC_FLAKES_COLOR),
            (iray.IN_METALLIC_FLAKES_COLOR_MAP, iwave.IN_METALLIC_FLAKES_COLOR_MAP),
            (iray.IN_METALLIC_FLAKES_ROUGHNESS, iwave.IN_METALLIC_FLAKES_ROUGHNESS),
            (iray.IN_METALLIC_FLAKES_ROUGHNESS_MAP, iwave.IN_METALLIC_FLAKES_ROUGHNESS_MAP),
            (iray.IN_METALLIC_FLAKES_SIZE, iwave.IN_METALLIC_FLAKES_SIZE),
            (iray.IN_METALLIC_FLAKES_STRENGTH, iwave.IN_METALLIC_FLAKES_STRENGTH),
            (iray.IN_METALLIC_FLAKES_DENSITY, iwave.IN_METALLIC_FLAKES_DENSITY),

            (iray.IN_TOP_COAT_WEIGHT, iwave.IN_TOP_COAT_WEIGHT),
            (iray.IN_TOP_COAT_WEIGHT_MAP, iwave.IN_TOP_COAT_WEIGHT_MAP),
            (iray.IN_TOP_COAT_COLOR, iwave.IN_TOP_COAT_COLOR),
            (iray.IN_TOP_COAT_COLOR_MAP, iwave.IN_TOP_COAT_COLOR_MAP),
            (iray.IN_TOP_COAT_ROUGHNESS, iwave.IN_TOP_COAT_ROUGHNESS),
            (iray.IN_TOP_COAT_ROUGHNESS_MAP, iwave.IN_TOP_COAT_ROUGHNESS_MAP),

            (iray.IN_THIN_FILM_WEIGHT, iwave.IN_THIN_FILM_WEIGHT),
            (iray.IN_THIN_FILM_ROTATIONS, iwave.IN_THIN_FILM_ROTATIONS),
            (iray.IN_THIN_FILM_THICKNESS, iwave.IN_THIN_FILM_THICKNESS),
            (iray.IN_THIN_FILM_THICKNESS_MAP, iwave.IN_THIN_FILM_THICKNESS_MAP),
            (iray.IN_THIN_FILM_IOR, iwave.IN_THIN_FILM_IOR),
            (iray.IN_THIN_FILM_IOR_MAP, iwave.IN_THIN_FILM_IOR_MAP),
        ]
