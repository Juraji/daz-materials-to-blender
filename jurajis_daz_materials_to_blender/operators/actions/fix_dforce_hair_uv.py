from bpy.types import Operator, Object, ShaderNodeUVMap
from bpy.props import StringProperty, FloatProperty

from ..base import OperatorReportMixin
from ...utils.poll import mode_is_object, object_is_mesh
from ...utils.uv import HairUVProcessor


class FixDforceHairUVOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.fix_dforce_hair_uv"
    bl_label = "Fix Dforce Hair UV"
    bl_description = "Try to fix the UV alignment of Dforce generated PS/PR hairs."
    bl_options = {"REGISTER", "BLOCKING", "UNDO"}

    fixed_uv_name: StringProperty(
        name="Fixed UV Name",
        default="FixedHairUV"
    )

    uv_strand_spacing: FloatProperty(
        name="UV Strand Spacing",
        default=0.01
    )

    @classmethod
    def poll(cls, context):
        return mode_is_object(context) and object_is_mesh(context)

    def execute(self, context):
        b_object: Object = context.active_object
        processor = HairUVProcessor(b_object, self.fixed_uv_name, self.uv_strand_spacing)

        if not processor.uv_exists():
            processor.regenerate_uv()
        else:
            self.report_warning(f"A UV Map with the name \"{self.fixed_uv_name}\" already exists. Delete it first.")
            return {"CANCELLED"}

        for material_slot in b_object.material_slots:
            if not material_slot.material.use_nodes:
                continue  # Not a node tree!
            for node in material_slot.material.node_tree.nodes:
                if isinstance(node, ShaderNodeUVMap):
                    node.uv_map = self.fixed_uv_name

        self.report_info("New UV generated!")
        return {"FINISHED"}
