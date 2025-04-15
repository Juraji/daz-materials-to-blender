from pathlib import Path
from typing import Type

import bpy
from bpy.types import Operator, Object

from ..shaders.material_shader import ShaderGroupApplier
from ..utils.dson import DazDsonMaterialReader
from ..utils.utilities import translate_node_id_to_blender_name
from ..properties import MaterialImportProperties


class ImportMaterialsOperator(Operator):
    bl_idname = "daz_import.import_all_materials"
    bl_label = "Import All Materials"
    bl_description = "Import Materials from DAZ"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    @classmethod
    def poll(cls, context):
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties
        return props.daz_scene_file != "" and props.daz_scene_file.endswith(".duf")

    def execute(self, context):
        props: MaterialImportProperties = context.scene.daz_import__material_import_properties

        # Run shader group import op
        create_groups_result = bpy.ops.daz_import.create_shader_groups()
        if create_groups_result != {"FINISHED"}:
            self.report({"ERROR"}, "Failed to create shader groups.")
            return {"CANCELLED"}

        # Read and convert DAZ scene
        daz_save_file = Path(props.daz_scene_file)
        if not daz_save_file.exists():
            self.report_error(f"File {daz_save_file} does not exist")
            return {"CANCELLED"}

        reader = DazDsonMaterialReader()
        mats_per_object = reader.read_materials(daz_save_file)
        self.report_info(f"Found {len(mats_per_object)} objects in {daz_save_file}!")

        for node_id, mat_def in mats_per_object.items():
            node_label: str = mat_def['label']
            node_parent_id = mat_def['parent_id']
            node_materials: dict = mat_def['materials']
            b_obj_name = translate_node_id_to_blender_name(node_id)

            b_object = bpy.data.objects.get(b_obj_name)
            if b_object is None and not node_parent_id is None:
                node_parent_name = translate_node_id_to_blender_name(node_parent_id)
                b_object = bpy.data.objects.get(node_parent_name)
            if b_object is None:
                self.report_warning(f"Object {node_id} ({node_label}) not found!")
                continue

            self.report_info(f"Importing Materials for {node_id}...")
            self.apply_material_to_object(b_object, node_materials, props)

            if props.rename_objects and b_obj_name != node_label:
                b_object.name = node_label

        self.report_info("Materials import finished!")
        return {"FINISHED"}

    def report_info(self, message: str):
        self.report({"INFO"}, f"DAZ Material Import: {message}")

    def report_warning(self, message: str):
        self.report({"WARNING"}, f"DAZ Material Import: {message}")

    def report_error(self, message: str):
        self.report({"ERROR"}, f"DAZ Material Import: {message}")

    def apply_material_to_object(self, b_object: Object, node_materials: dict, props: MaterialImportProperties):
        for mat_name, mat_def in node_materials.items():
            mat_type = mat_def['type']
            channels = mat_def['channels']

            material = None
            if mat_name in b_object.data.materials:
                material = b_object.data.materials[mat_name]
            else:
                for mat in b_object.data.materials:
                    if mat.name.startswith(mat_name):
                        material = mat
                        break

            if material is None:
                continue

            material.use_nodes = True
            node_tree = material.node_tree

            # Setup defaults
            node_tree.nodes.clear()

            node_material_output = node_tree.nodes.new("ShaderNodeOutputMaterial")
            node_material_output.name = "Material Output"
            node_material_output.is_active_output = True
            node_material_output.target = 'ALL'
            node_material_output.location = (125, 0)

            node_mapping = node_tree.nodes.new("ShaderNodeMapping")
            node_mapping.name = "Mapping"
            node_mapping.vector_type = 'POINT'
            node_mapping.location = (-1230, 0)

            # node UV Map
            node_uv_map = node_tree.nodes.new("ShaderNodeUVMap")
            node_uv_map.name = "UV Map"
            node_uv_map.from_instancer = False
            node_uv_map.uv_map = "UVMap"
            node_uv_map.location = (-1505, 0)
            node_tree.links.new(node_uv_map.outputs[0], node_mapping.inputs[0])

            material_shader_cls: Type[ShaderGroupApplier] | None = None
            if mat_type == 'pbrskin':
                from ..shaders.pbr_skin import PBRSkinShaderGroupApplier
                material_shader_cls = PBRSkinShaderGroupApplier
            elif mat_type == 'iray_uber':
                from ..shaders.iray_uber import IrayUberShaderGroupApplier
                material_shader_cls = IrayUberShaderGroupApplier
            elif mat_type == 'translucent_fabric':
                from ..shaders.iwave_translucent_fabric import IWaveTranslucentFabricShaderGroupApplier
                material_shader_cls = IWaveTranslucentFabricShaderGroupApplier

            if material_shader_cls is None:
                self.report_error(f"Unknown Material Type {mat_type} for {b_object.name}[{mat_name}].")
                return

            material_shader: ShaderGroupApplier = material_shader_cls(props, node_tree, node_mapping, node_material_output)
            material_shader.add_shader_group((-415, 0), channels)
            material_shader.align_image_nodes(-915, 0)

            if props.rename_materials:
                material.name = f'{b_object.name}_{mat_name}'
