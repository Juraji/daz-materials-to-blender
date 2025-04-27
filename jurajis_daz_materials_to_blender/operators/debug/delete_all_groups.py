import bpy
from bpy.types import Operator

from ..base import OperatorReportMixin
from ...shaders import GROUP_DESCRIPTION_PREFIX


class DebugDeleteAllGroupsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.debug_delete_all_groups"
    bl_label = "Delete All Groups"
    bl_description = """Delete all groups created by this plugin.
Note that this does not delete or revert materials. It unlinks the groups upon deletion.
Note 2 that this looks at the group descriptions, as the name is free to change. Let's hope you haven't touched those :D."""

    def execute(self, context):
        node_groups = bpy.data.node_groups

        for node_group in node_groups.values():
            if node_group.description.startswith(GROUP_DESCRIPTION_PREFIX):
                node_groups.remove(node_group)

        return {'FINISHED'}
