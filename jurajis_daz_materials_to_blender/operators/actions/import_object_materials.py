from typing import Type

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator, Context, Object as BObject

from ..base import OperatorReportMixin
from ...properties import MaterialImportProperties, props_from_ctx
from ...shaders import SHADER_GROUP_APPLIERS, ShaderGroupApplier
from ...shaders.fallback import FallbackShaderGroupApplier
from ...utils.dson import DsonChannels, DsonCacheManager, DsonLoadException
from ...utils.poll import selected_objects_all_is_mesh
from ...utils.slugify import slugify

MATERIAL_TYPE_ID_PROP = "__DAZ_IMPORT_SHADER_TYPE_ID__"


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

        try:
            dson_data = DsonCacheManager.get_or_load(context)
        except DsonLoadException as e:
            self.report_error(e.message)
            return {"CANCELLED"}

        for b_object in b_objects:
            dson_id = dson_data.to_dson_id(b_object.name)
            node_mat_channels: list[DsonChannels] = \
                next((node.materials for node in dson_data.objects if node.id == dson_id), [])

            if not node_mat_channels:
                self.report_warning(f"Could not find materials for object {b_object.name}. (dson id: {dson_id})")
                continue

            node_mat_channel_names = [c.name for c in node_mat_channels]
            direct_children_mat_channels = [
                material
                for node in dson_data.objects if node.parent_id == dson_id
                for material in node.materials if material.name not in node_mat_channel_names
            ]

            mat_channels = [*node_mat_channels, *direct_children_mat_channels]

            self._import_missing_groups(mat_channels)
            self._apply_materials(b_object, mat_channels, props)
            self.report_info(f"Applied materials for object {b_object.name}")

        return {"FINISHED"}

    def _apply_materials(self,
                         b_object: BObject,
                         dson_materials: list[DsonChannels],
                         props: MaterialImportProperties):
        for mat_def in dson_materials:
            mat_name = mat_def.name
            mat_type_id = mat_def.type_id
            channels = mat_def.channels

            material = self._find_material_by_name(b_object, mat_name)
            if not material:
                continue

            applier_cls = self._find_applier_by_type_id(mat_type_id)
            if not applier_cls:
                self.report_warning("No shader group available for material type "
                                    f"\"{mat_type_id}\" for {b_object.name}[{mat_name}].")
                applier_cls = FallbackShaderGroupApplier  # Fallback

            material.use_nodes = True
            node_tree = material.node_tree

            # Setup defaults
            node_tree.nodes.clear()

            applier = applier_cls(props, b_object, node_tree)
            applier.apply_shader_group(channels)
            material[MATERIAL_TYPE_ID_PROP] = mat_type_id

    @staticmethod
    def _find_material_by_name(b_object, mat_name):
        # Material name exactly equals
        if mat_name in b_object.data.materials:
            return b_object.data.materials[mat_name]

        # Slugified material name exactly equals
        mat_name_slug = slugify(mat_name, lower_case=False)
        if mat_name_slug in b_object.data.materials:
            return b_object.data.materials[mat_name_slug]

        # Starts with
        for mat in b_object.data.materials.values():
            if mat.name.startswith(mat_name):
                return mat
            mat_slug = slugify(mat.name, lower_case=False)
            if mat_slug.startswith(mat_name_slug):
                return mat

        return None

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
