import re

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Context

from ..base import OperatorReportMixin
from ...shaders.library import library_path, LIB_GROUP_DESCRIPTION


class ImportShaderGroupOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.import_shader_group"
    bl_label = "Import Shader Group"
    bl_description = "Imports the Shader Group identified by group_name from the internal library."
    bl_options = {"REGISTER", "UNDO"}

    group_name: StringProperty(
        name="Group Name",
        description="The name of the shader group to import.",
    )

    def execute(self, context: Context):
        library = str(library_path())

        if self.group_name in bpy.data.node_groups:
            self.report_warning(f"A Shader Group with name \"{self.group_name}\" already exists!")
            return {"CANCELLED"}

        with bpy.data.libraries.load(filepath=library, link=False) as (data_from, data_to):
            if not self.group_name in data_from.node_groups:
                self.report_warning(f"No Shader Group with name \"{self.group_name}\" exists in the library!")
                return {"CANCELLED"}

            data_to.node_groups.append(self.group_name)

        self._dedupe_groups()

        self.report_info(f"Successfully imported shader group \"{self.group_name}\".")
        return {'FINISHED'}

    @staticmethod
    def _dedupe_groups():
        originals = {}
        duplicates = []

        for group in bpy.data.node_groups:
            if group.description != LIB_GROUP_DESCRIPTION:
                continue

            base_name = re.sub(r'\.\d{3}$', '', group.name)
            if base_name not in originals:
                originals[base_name] = group
            else:
                duplicates.append((base_name, group))

        for base_name, dup in duplicates:
            original = originals[base_name]
            for user in bpy.data.node_groups:
                for node in user.nodes:
                    if node.type == "GROUP" and node.node_tree == dup:
                        node.node_tree = original

            if not dup.users:
                bpy.data.node_groups.remove(dup)

