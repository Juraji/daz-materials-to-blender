from collections import defaultdict
from pathlib import Path
from typing import Type

import bpy
from bpy.types import Operator, Object

from .operator_report_mixin import OperatorReportMixin
from ..properties import MaterialImportProperties
from ..shaders import ShaderGroupApplier, SHADER_GROUP_BUILDERS, SHADER_GROUP_APPLIERS
from ..utils.dson import DazDsonMaterialReader, DsonMaterial, DsonSceneNode


class ImportMaterialsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.import_all_materials"
    bl_label = "Import All Materials"
    bl_description = "Import Materials from DAZ"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    @classmethod
    def poll(cls, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        return props.daz_scene_file != "" and props.daz_scene_file.endswith(".duf")

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties

        # Read and convert DAZ scene
        daz_save_file = Path(props.daz_scene_file)
        if not daz_save_file.exists():
            self.report_error(f"File {daz_save_file} does not exist")
            return {"CANCELLED"}

        dson_reader = DazDsonMaterialReader()
        dson_scene_nodes = dson_reader.read_materials(daz_save_file)
        dson_id_conversion_table = self._create_dson_id_conversion_table(dson_scene_nodes)
        self.report_info(f"Found {len(dson_scene_nodes)} objects in {daz_save_file}!")

        def convert_id(nid: str) -> str:
            if nid in dson_id_conversion_table:
                return dson_id_conversion_table[nid]
            else:
                return nid

        self._create_missing_shader_groups(dson_scene_nodes)

        # Apply materials
        for mat_def in dson_scene_nodes:
            dson_id = mat_def.id
            dson_label: str = mat_def.label
            dson_parent_id = mat_def.parent_id
            dson_materials = mat_def.materials
            b_obj_name = convert_id(dson_id)

            b_object = bpy.data.objects.get(b_obj_name)
            if b_object is None and not dson_parent_id is None:
                node_parent_name = convert_id(dson_parent_id)
                b_object = bpy.data.objects.get(node_parent_name)
            if b_object is None:
                self.report_warning(f"Object {b_obj_name} ({dson_label}) not found!")
                continue

            self._apply_material_to_object(b_object, dson_materials, props)

            if props.rename_objects and b_obj_name != dson_label:
                b_object.name = dson_label

        self.report_info("Materials import finished!")
        return {"FINISHED"}

    def _apply_material_to_object(self,
                                  b_object: Object,
                                  node_materials: list[DsonMaterial],
                                  props: MaterialImportProperties):
        for mat_def in node_materials:
            mat_name = mat_def.material_name
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
                return

            material.use_nodes = True
            node_tree = material.node_tree

            # Setup defaults
            node_tree.nodes.clear()

            applier = applier_cls(props, node_tree)
            applier.apply_shader_group(channels)
            applier.align_image_nodes()

            if props.rename_materials:
                material.name = f'{b_object.name}_{mat_name}'

    @staticmethod
    def _create_missing_shader_groups(nodes: list[DsonSceneNode]):
        used_mat_types = {mat_def.type_id for node in nodes for mat_def in node.materials}

        for builder in (b for b in SHADER_GROUP_BUILDERS if b.material_type_id() in used_mat_types):
            # noinspection PyUnresolvedReferences
            bpy.ops.daz_import.create_shader_group(group_name=builder.group_name(), silent=True)

    @staticmethod
    def _find_applier_by_type_id(mat_type_id: str) -> Type[ShaderGroupApplier] | None:
        for applier in SHADER_GROUP_APPLIERS:
            if applier.material_type_id() == mat_type_id:
                return applier
        return None

    @staticmethod
    def _create_dson_id_conversion_table(nodes: list[DsonSceneNode]) -> dict[str, str]:
        """
        :param nodes: The result from read_materials
        :return: A dict of DAZ node id to expected node name in Blender.
        """
        conversion_table = {}
        suffix_groups = defaultdict(list)

        # Collect node IDs with suffixes
        for node in nodes:
            base, *suffix = node.id.rsplit('-', 1)
            if suffix and suffix[0].isdigit():
                suffix_groups[base].append(node.id)

        # Assign new names based on suffix groups
        for base, variants in suffix_groups.items():
            for i, variant in enumerate(sorted(variants)):
                conversion_table[variant] = f"{base}.{i + 1:03d}"

        return conversion_table
