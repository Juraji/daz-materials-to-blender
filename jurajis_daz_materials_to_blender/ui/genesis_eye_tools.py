from bpy.types import Panel

from ..operators.actions import SeparateGenesis8EyesOperator, SeparateGenesis9EyesOperator


class GenesisEyeToolsPanel3D(Panel):
    bl_category = "Juraji's Tools"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_context = "objectmode"
    bl_label = "Genesis Eyes"
    bl_idname = "VIEW3D_PT_daz_extract_genesis_eyes"

    def draw(self, context):
        layout = self.layout
        layout.operator(SeparateGenesis8EyesOperator.bl_idname)
        layout.operator(SeparateGenesis9EyesOperator.bl_idname)
