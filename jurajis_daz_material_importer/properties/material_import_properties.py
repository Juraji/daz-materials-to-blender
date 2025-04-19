from bpy.props import StringProperty, BoolProperty
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
        name="Replace Existing Shader Groups",
        description="Replace shader node groups created by an earlier import.",
        default=True,
    )
