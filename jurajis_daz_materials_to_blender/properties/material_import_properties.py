from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from bpy.types import PropertyGroup


class MaterialImportProperties(PropertyGroup):
    daz_scene_file: StringProperty(
        name="DAZ Scene File",
        description="Path to directory where the files are created",
        subtype="FILE_PATH",
    )

    rename_materials: BoolProperty(
        name="Rename Materials",
        description="""Rename materials to their DAZ surface equivalents.
Note that enabling this will prevent rerunning imports!""",
        default=False,
    )

    rename_objects: BoolProperty(
        name="Rename Objects",
        description="""Rename objects to their DAZ label equivalent.
Note that enabling this will break rerunning imports!""",
        default=False,
    )

    # General Modifiers
    apply_color_corrections: BoolProperty(
        name="Apply Color Correction",
        description="""DAZ Studio uses a curve to determine colors.
You might have noticed that the numbers, shown on color sliders don't match the colors in the color picker.
Enabling this option will apply an aproximated curve to correct color inputs.""",
        default=True,
    )

    bump_strength_multiplier: FloatProperty(
        name="Bump Strength Multiplier",
        description="""Multiplier for the bump strength property.
Bump strength in DAZ is scaled 100x. This option reduces bump strength on import.""",
        default=0.01,
        min=0.001,
        max=1.0,
    )

    dls_weight_multiplier: FloatProperty(
        name="DLS Weight",
        description="""Multiply Dual Lobe Specular weigths by this value.
DLS can be quite strong in DAZ, x0.5 seems to be a good starting point.""",
        default=0.5,
        min=0.0,
        max=2.0,
    )

    # PBR Skin Modifiers
    pbr_skin_normal_multiplier: FloatProperty(
        name="PBR Skin Normal Weight",
        description="""Multiply PBR Skin's Normal weigths by this value.
Some skin textures look better when normals are x2.0.""",
        default=2.0,
        min=0.0,
        max=3.0,
    )

    # Iray Uber Modifiers
    iray_uber_remap_glossy_color_to_roughness: BoolProperty(
        name="Remap Glossy Color to Roughness",
        description="""Remaps Glossy Color to Roughness.
If Glossy Roughness is not set.""",
        default=True,
    )

    iray_uber_replace_glass: BoolProperty(
        name="Use Fake Glass",
        description="""The Iray Uber Shader Group is very expensive for surfaces with 100% refraction.
You can opt to replace these surfaces with a fake glass implementation to save on render cycles.""",
        default=True,
    )

    iray_uber_clamp_emission: FloatProperty(
        name="Iray Uber Clamp Emission",
        description="""Clamp Emission colors.
Some artist use emission to make surfaces pop. However, this looks bad in Cycles. This value clamps emission to 0 when it's color value is below this threshold""",
        default=0.5,
        min=0.0,
        max=1.0
    )

    def has_scene_file_set(self):
        return self.daz_scene_file != "" and self.daz_scene_file.endswith(".duf")
