from bpy.props import CollectionProperty, StringProperty
from bpy.types import AddonPreferences, PropertyGroup, Context


class ContentLibraryItem(PropertyGroup):
    path: StringProperty(
        name="Library Path",
        description="Path to a content library",
        subtype="DIR_PATH",
    )


class MaterialImportPreferences(AddonPreferences):
    bl_idname = "bl_ext.user_default.jurajis_daz_materials_to_blender"

    content_libraries: CollectionProperty(
        name="Content Libraries",
        description="Your DAZ Content Libraries",
        type=ContentLibraryItem,
    )

    # noinspection PyUnusedLocal
    def draw(self, context: Context):
        layout = self.layout
        layout.label(text="DAZ Library locations")
        box = layout.box()
        col = box.column()

        for i, item in enumerate(self.content_libraries):
            row = col.row()
            row.prop(item, "path", text=f"Path {i + 1}")
            remove_op = row.operator("daz_import.prefs_remove_library_path", text="", icon="X")
            remove_op.index = i

        row = col.row(align=True)
        row.operator("daz_import.prefs_win_detect_daz_libraries")
        row.operator("daz_import.prefs_add_library_path")

    def content_libraries_as_paths(self):
        from pathlib import Path
        from bpy.path import abspath
        return [Path(abspath(p.path)) for p in self.content_libraries]
