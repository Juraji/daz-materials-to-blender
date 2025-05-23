# Helpers
LIB_GROUP_DESCRIPTION = "DO NOT EDIT - DAZ IMPORTER SHADER GROUP"
LIB_FILE_NAME = "library.blend"


def library_path():
    import pathlib
    return pathlib.Path(__file__).parent.resolve() / LIB_FILE_NAME


# Support Groups
ADVANCED_TOP_COAT = "Advanced Top Coat"
ASYMMETRICAL_DISPLACEMENT = "Asymmetrical Displacement"
BLACKBODY_EMISSION = "Blackbody Emission"
DAZ_LUT_CORRECTION = "DAZ LUT Correction"
DUAL_LOBE_SPECULAR = "Dual Lobe Specular"
FAKE_GLASS = "Fake Glass"
METALLIC_FLAKES = "Metallic Flakes"
WEIGHTED_TRANSLUCENCY = "Weighted Translucency"

SUPPORT_SHADER_GROUPS = [
    ADVANCED_TOP_COAT,
    ASYMMETRICAL_DISPLACEMENT,
    BLACKBODY_EMISSION,
    DAZ_LUT_CORRECTION,
    DUAL_LOBE_SPECULAR,
    FAKE_GLASS,
    METALLIC_FLAKES,
    WEIGHTED_TRANSLUCENCY,
]

# Shader groups
IRAY_UBER = "Iray Uber"
IWAVE_TRANSLUCENT_FABRIC = "iWave Translucent Fabric"
MELANIN_DUAL_LOBE_HAIR = "Melanin Based Dual Lobe Blended Hair"
PBR_SKIN = "PBR Skin"

SHADER_GROUPS = [
    IRAY_UBER,
    IWAVE_TRANSLUCENT_FABRIC,
    MELANIN_DUAL_LOBE_HAIR,
    PBR_SKIN,
]
