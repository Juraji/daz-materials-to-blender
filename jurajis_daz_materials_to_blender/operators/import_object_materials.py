from pathlib import Path
from typing import Type

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator, Context, Object as BObject

from .base import OperatorReportMixin
from ..properties import MaterialImportProperties, props_from_ctx
from ..shaders import SHADER_GROUP_APPLIERS, ShaderGroupApplier
from ..shaders.fallback import FallbackShaderGroupApplier
from ..utils.dson import DsonObject, DsonChannels
from ..utils.dson_scene_data import DsonSceneData, DsonFileNotFoundException
from ..utils.poll import selected_objects_all_is_mesh


class ImportObjectMaterialsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.import_object_materials"
    bl_label = "Import Object Materials"
    bl_description = "Import Materials from DAZ for the selected object."
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    use_cached_scene_data: BoolProperty(
        name="Use cached scene data",
        default=False,
    )

    @classmethod
    def poll(cls, context: Context):
        props: MaterialImportProperties = props_from_ctx(context)
        return props.has_scene_file_set() and selected_objects_all_is_mesh(context)

    def execute(self, context):
        props: MaterialImportProperties = props_from_ctx(context)
        b_objects = context.selected_objects

        if self.use_cached_scene_data and DsonSceneData.has_scene_data():
            dson_scene_nodes, dson_id_conversion_table = DsonSceneData.get_scene_data()
        else:
            try:
                daz_save_file = Path(bpy.path.abspath(props.daz_scene_file))
                dson_scene_nodes, dson_id_conversion_table = DsonSceneData.load_scene_data(daz_save_file)
                self.report_info(f"Found {len(dson_scene_nodes)} objects in {daz_save_file}!")
            except DsonFileNotFoundException as e:
                self.report_error(e.message)
                return {"CANCELLED"}


        for b_object in b_objects:
            dson_id = dson_id_conversion_table.to_dson(b_object.name)
            dson_node_mat = next((node.materials for node in dson_scene_nodes if node.id == dson_id), None)

            if not dson_node_mat:
                self.report_warning(f"Could not find materials object {b_object.name}")
                continue

            dson_direct_children_mats = [
                materials
                for node in dson_scene_nodes if node.parent_id == dson_id
                for materials in node.materials
            ]

            dson_materials = [*dson_node_mat, *dson_direct_children_mats]

            self._import_missing_groups(dson_materials)
            self._apply_materials(b_object, dson_materials, props)

        return {"FINISHED"}

    def _apply_materials(self,
                         b_object: BObject,
                         dson_materials: list[DsonChannels],
                         props: MaterialImportProperties):
        for mat_def in dson_materials:
            mat_name = mat_def.name
            mat_type_id = mat_def.type_id
            channels = mat_def.channels

            if mat_name in b_object.data.materials:
                material = b_object.data.materials[mat_name]
            else:
                material = next((m for m in b_object.data.materials if m.name.startswith(mat_name)), None)

            if not material:
                continue

            applier_cls = self._find_applier_by_type_id(mat_type_id)
            if not applier_cls:
                self.report_error("No shader group available for material type "
                                  f"\"{mat_type_id}\" for {b_object.name}[{mat_name}].")
                applier_cls = FallbackShaderGroupApplier  # Fallback

            material.use_nodes = True
            node_tree = material.node_tree

            # Setup defaults
            node_tree.nodes.clear()

            applier = applier_cls(props, b_object, node_tree)
            applier.apply_shader_group(channels)

            if props.rename_materials:
                material.name = f'{b_object.name}_{mat_name}'

    @staticmethod
    def _import_missing_groups(materials: list[DsonChannels]):
        used_mat_types = {mat_def.type_id for mat_def in materials}
        used_builders = [b for b in SHADER_GROUP_APPLIERS if b.material_type_id() in used_mat_types]

        for builder in used_builders:
            # noinspection PyUnresolvedReferences
            bpy.ops.daz_import.import_shader_group(group_name=builder.group_name(), silent=True)

    @staticmethod
    def _find_applier_by_type_id(mat_type_id: str) -> Type[ShaderGroupApplier] | None:
        for applier in SHADER_GROUP_APPLIERS:
            if applier.material_type_id() == mat_type_id:
                return applier
        return None
