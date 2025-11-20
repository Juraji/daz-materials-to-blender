import random

import bpy
from bpy.props import IntProperty, FloatProperty
from bpy.types import Operator, Context, Object
from mathutils import Vector, Matrix

from ..base import OperatorReportMixin


class SeparateGenesis9EyesOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.separate_genesis_9_eyes"
    bl_label = "Separate Genesis 9 Eyes"
    bl_options = {'REGISTER', 'BLOCKING', 'UNDO'}

    mat_eye_moisture_left: IntProperty(
        name="Eye Moisture Left Material Index",
        default=0
    )
    mat_eye_moisture_right: IntProperty(
        name="Eye Moisture Right Material Index",
        default=1
    )
    eye_left_uv_x: FloatProperty(
        name="Eye Left UV X Position",
        default=0.75
    )
    eye_left_uv_y: FloatProperty(
        name="Eye Left UV Y Position",
        default=0.25
    )
    mat_eye_left: IntProperty(
        name="Eye Left Material Index",
        default=2
    )
    mat_eye_right: IntProperty(
        name="Eye Right Material Index",
        default=3
    )
    eye_right_uv_x: FloatProperty(
        name="Eye Right UV X Position",
        default=0.25
    )
    eye_right_uv_y: FloatProperty(
        name="Eye Right UV Y Position",
        default=0.25
    )

    @classmethod
    def poll(cls, context: Context):
        obj = context.active_object
        return context.mode == 'OBJECT' and obj and obj.type == 'MESH' and obj.data.name.startswith("Genesis9Eyes")

    def execute(self, context: Context):
        genesis_eyes_obj = context.active_object

        left_eye_vertices = self.find_vertices_by_materials(genesis_eyes_obj,
                                                            {self.mat_eye_moisture_left, self.mat_eye_left})
        left_eye_obj = self.separate_mesh_by_vertices(context, genesis_eyes_obj, left_eye_vertices)
        left_eye_obj.name = f"{genesis_eyes_obj.name}.Left"

        right_eye_obj = genesis_eyes_obj
        right_eye_obj.name = f"{genesis_eyes_obj.name}.Right"

        self.align_origin_to_eye(context, left_eye_obj,
                                 self.mat_eye_moisture_left, self.eye_left_uv_x, self.eye_left_uv_y)
        self.align_origin_to_eye(context, right_eye_obj,
                                 self.mat_eye_moisture_right, self.eye_right_uv_x, self.eye_right_uv_y)

        self.report_info(
            f"Successfully separated {genesis_eyes_obj.name}'s eyes into {right_eye_obj.name} and {left_eye_obj.name}!")
        return {"FINISHED"}

    def align_origin_to_eye(self, context: Context, eye_obj: Object,
                            eye_mat_idx: int, eye_uv_x: float, eye_uv_y: float):
        with context.temp_override(
                selected_editable_objects=[eye_obj],
                active_object=eye_obj):
            # Set origin to center of mass
            com_vertices = self.find_vertices_by_materials(eye_obj, {eye_mat_idx})
            com = self.find_center_of_mass(eye_obj, com_vertices)
            context.scene.cursor.location = eye_obj.matrix_world @ com
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            context.scene.cursor.location = Vector()

            # Calculate the rotation quaternion in object space
            normal_vec = self.find_eye_direction_via_uv(eye_obj, eye_uv_x, eye_uv_y)

            # Calculate the rotation to align the object's local Z-axis with the normal
            z_to_normal_rot = Vector((0, 0, 1)).rotation_difference(normal_vec)

            # Apply the rotation to the object's local axes
            loc, rot, scale = eye_obj.matrix_world.decompose()
            new_rot = rot @ z_to_normal_rot
            eye_obj.matrix_world = Matrix.LocRotScale(loc, new_rot, scale)

            # Compensate the mesh rotation
            eye_obj.data.transform(z_to_normal_rot.inverted().to_matrix().to_4x4())
            eye_obj.data.update()

    @staticmethod
    def find_vertices_by_materials(obj: Object, mat_indices: set[int]) -> list[int]:
        mesh = obj.data
        vert_indices: set[int] = set()

        for poly in mesh.polygons:
            if poly.material_index in mat_indices:
                for loop in poly.loop_indices:
                    vert_idx = mesh.loops[loop].vertex_index
                    vert_indices.add(vert_idx)

        return list(vert_indices)

    @staticmethod
    def separate_mesh_by_vertices(context: Context, source_obj: Object,
                                  vertex_indices: list[int]) -> Object:
        mesh = source_obj.data

        # Update selected vertices of interest
        for v in mesh.vertices:
            v.select = False
        for i in vertex_indices:
            mesh.vertices[i].select = True

        with context.temp_override(
                selected_editable_objects=[source_obj],
                active_object=source_obj):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.object.mode_set(mode='OBJECT')

        # The new object is the last selected object
        return context.selected_objects[-1]

    @staticmethod
    def find_center_of_mass(obj: Object, vertex_indices: list[int]) -> Vector:
        center = Vector()
        for i in vertex_indices:
            center += obj.data.vertices[i].co
        center /= len(vertex_indices)
        return center

    @staticmethod
    def find_eye_direction_via_uv(obj: Object, uv_center_x: float, uv_center_y: float,
                                  threshold: float = 0.001) -> Vector:
        mesh = obj.data
        if not mesh.uv_layers.active:
            raise Exception(f"Object with name '{obj.name}' has no active UV layers")

        uv_data = mesh.uv_layers.active.data
        thresh_sqr = threshold ** 2
        closest_dist = float('inf')
        closest_vert_normal = None

        for poly in mesh.polygons:
            loop_start = poly.loop_start
            for i in range(poly.loop_total):
                loop_idx = loop_start + i
                uv = uv_data[loop_idx].uv
                dist_sqr = (uv.x - uv_center_x) ** 2 + (uv.y - uv_center_y) ** 2
                if dist_sqr < thresh_sqr and dist_sqr < closest_dist:
                    closest_dist = dist_sqr
                    vert_idx = mesh.loops[loop_idx].vertex_index
                    vert = mesh.vertices[vert_idx]
                    closest_vert_normal = vert.normal

        if not closest_vert_normal:
            raise Exception(f"Could not find vertex near coordinate {uv_center_x},{uv_center_y} for object {obj.name}")

        return closest_vert_normal

    @staticmethod
    def find_average_vertex_normal(obj: Object, vertex_indices) -> Vector:
        vector = Vector()
        for i in vertex_indices:
            vector += obj.data.vertices[i].normal
        vector /= len(vertex_indices)
        return vector.normalized()

    @staticmethod
    def set_parent_with_transforms(obj: Object, parent: Object):
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
