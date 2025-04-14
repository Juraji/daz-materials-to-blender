from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy.types import PropertyGroup


class MaterialImportProperties(PropertyGroup):
    daz_scene_file: StringProperty(
        name="DAZ Scene File",
        description="Path to directory where the files are created",
        subtype="FILE_PATH",
    )

    rename_materials: BoolProperty(
        name="Rename Materials",
        description="Rename materials to their DAZ surface equivalents. Note that enabling this will prevent rerunning imports!",
        default=False,
    )

    rename_objects: BoolProperty(
        name="Rename Objects",
        description="Rename objects to their DAZ label equivalent. Note that enabling this will prevent rerunning imports!",
        default=False,
    )

    replace_node_groups: BoolProperty(
        name="Replace Shader Groups",
        description="Replace shader node groups created by an earlier import.",
        default=False,
    )

    normal_factor: FloatProperty(
        name="Normal Factor",
        description="Normal mulitplication factor.",
        default=2.0,
    )

    dls_layer_factor: FloatProperty(
        name="DLS Layer Factor",
        description="Dual Lobe Specular layer factor.",
        default=0.7,
    )
