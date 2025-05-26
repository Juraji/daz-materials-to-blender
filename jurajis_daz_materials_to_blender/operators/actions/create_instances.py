import math

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator, Context, Collection, Object as BObject
from mathutils import Vector, Euler, Matrix

from ..base import OperatorReportMixin
from ...properties import MaterialImportProperties, props_from_ctx
from ...utils.dson import DsonCacheManager, DsonLoadException, DsonObject, DsonTransforms
from ...utils.math import tuple_prod, tuple_zip_sum


class CreateInstancesOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.create_instances"
    bl_label = "Create Instances"
    bl_description = "Create instances of all instanced objects in DAZ."
    bl_options = {"REGISTER", "BLOCKING", "UNDO"}

    use_cached_scene_data: BoolProperty(
        name="Use cached scene data",
        default=False,
    )

    instances_collection_name: StringProperty(
        name="Collection name",
        default="Instances",
    )

    @classmethod
    def poll(cls, context: Context):
        props: MaterialImportProperties = props_from_ctx(context)
        return props.has_scene_file_set() and len(context.scene.objects) > 0

    def execute(self, context: Context):
        props: MaterialImportProperties = props_from_ctx(context)
        instance_collection = self._get_instance_collection(context, self.instances_collection_name)

        try:
            dson_data = DsonCacheManager.get_or_load(context)
        except DsonLoadException as e:
            self.report_error(e.message)
            return {"CANCELLED"}

        for dson_scene_node in dson_data.objects:
            b_object_name = dson_data.to_blender_name(dson_scene_node.id)
            b_object = bpy.data.objects.get(b_object_name)
            if b_object is None:
                continue

            self._restore_object_transformations(props, b_object, dson_scene_node)

            for dson_instance in dson_scene_node.instances:
                b_instance = b_object.copy()
                b_instance.data = b_object.data
                b_instance.name = dson_instance.label
                b_instance.matrix_world = self._daz_matrix_from(props, dson_instance)
                instance_collection.objects.link(b_instance)

        self.report_info(f"Created {len(instance_collection.objects)} instances!")
        return {"FINISHED"}

    @staticmethod
    def _get_instance_collection(context: Context, collection_nane: str) -> Collection:
        collections = bpy.data.collections

        if collection_nane not in collections:
            render_targets = collections.new(collection_nane)
            context.scene.collection.children.link(render_targets)
            return render_targets
        else:
            return collections[collection_nane]

    @classmethod
    def _restore_object_transformations(cls,
                                        props: MaterialImportProperties,
                                        b_object: BObject,
                                        dson_scene_node: DsonObject):
        current_world_matrix = b_object.matrix_world.copy()
        if current_world_matrix.translation != Vector((0, 0, 0)):
            return

        daz_matrix = cls._daz_matrix_from(props, dson_scene_node)

        b_object.matrix_world = daz_matrix
        bpy.context.view_layer.update()

        delta = daz_matrix.inverted() @ current_world_matrix
        b_object.data.transform(delta)
        bpy.context.view_layer.update()

    @staticmethod
    def _daz_matrix_from(props: MaterialImportProperties,
                         transforms: DsonTransforms) -> Matrix:
        # Location
        loc = tuple_zip_sum(transforms.translation, transforms.origin)  # combine origin and translation
        loc = tuple_prod(loc, props.exported_scale_float())  # Scale by exported scale
        loc = Vector((loc[0], -loc[2], loc[1]))  # XZY vector and invert Y axis
        # Rotation
        rot = (
            math.radians(transforms.rotation[0]),
            math.radians(transforms.rotation[2]),
            math.radians(transforms.rotation[1]),
        )  # Convert deg to rad and convert to XZY
        rot = Euler(rot)
        # Scale
        scale = transforms.scale  # Use base scale to prevent overscaling
        scale = Vector((scale[0], scale[2], scale[1]))  # XZY vector

        # noinspection PyTypeChecker
        return Matrix.LocRotScale(loc, rot, scale)
