import random

import bpy
from bpy.props import IntProperty, FloatProperty
from bpy.types import Operator, Context, Object
from mathutils import Vector, Matrix, Euler

from ..base import OperatorReportMixin


class SeparateGenesis8EyesOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.separate_genesis_8_eyes"
    bl_label = "Separate Genesis 8 Eyes"
    bl_options = {'REGISTER', 'BLOCKING', 'UNDO'}

    mat_pupils: IntProperty(
        name="Pupils Material Index",
        default=10
    )
    mat_eye_moisture: IntProperty(
        name="Eye Moisture Material Index",
        default=11
    )
    mat_cornea: IntProperty(
        name="Cornea Material Index",
        default=13
    )
    mat_irises: IntProperty(
        name="Irises Material Index",
        default=14
    )
    mat_sclera: IntProperty(
        name="Sclera Material Index",
        default=15
    )
    separation_cluster_sample_size: IntProperty(
        name="Separation Cluster Sample Size",
        default=1000
    )
    separation_cluster_min_dist: FloatProperty(
        name="Separation Cluster Min Distance",
        default=0.01,
        subtype='DISTANCE'
    )

    @classmethod
    def poll(cls, context: Context):
        obj = context.active_object
        return context.mode == 'OBJECT' and obj and obj.type == 'MESH' and obj.data.name.startswith("Genesis8")

    def execute(self, context: Context):
        genesis_obj = context.active_object

        # Separate eyes from genesis figure (makes the vert count far smaller to jump into and out of edit mode)
        all_mats = {self.mat_pupils, self.mat_eye_moisture, self.mat_cornea, self.mat_irises, self.mat_sclera}
        eyes_vertices = self.find_vertices_by_materials(genesis_obj, all_mats)
        self.report_info(f"Found {len(eyes_vertices)} vertices for {genesis_obj.name}'s eyes!")

        right_eye_obj = self.separate_mesh_by_vertices(context, genesis_obj, eyes_vertices)
        right_eye_obj.name = f"{genesis_obj.name}.Eyes.Right"

        # Split left eye from right (by cluster bisection)
        left_eye_vertices, _ = self.bisect_vertex_clusters(
            right_eye_obj, self.separation_cluster_sample_size, self.separation_cluster_min_dist)
        left_eye_obj = self.separate_mesh_by_vertices(context, right_eye_obj, left_eye_vertices)
        left_eye_obj.name = f"{genesis_obj.name}.Eyes.Left"

        # Fix left eye
        self.align_origin_to_eye(context, left_eye_obj)
        self.set_parent_with_transforms(left_eye_obj, genesis_obj)

        # Fix right eye
        self.align_origin_to_eye(context, right_eye_obj)
        self.set_parent_with_transforms(right_eye_obj, genesis_obj)

        # Reset cursor position to identity
        context.scene.cursor.location = Vector()

        self.report_info(
            f"Successfully separated {genesis_obj.name}'s eyes into {right_eye_obj.name} and {left_eye_obj.name}!")
        return {"FINISHED"}

    def align_origin_to_eye(self, context: Context, eye_obj: Object):
        with context.temp_override(
                selected_editable_objects=[eye_obj],
                active_object=eye_obj):
            com_vertices = self.find_vertices_by_materials(eye_obj, {self.mat_sclera})
            com = self.find_center_of_mass(eye_obj, com_vertices)
            context.scene.cursor.location = eye_obj.matrix_world @ com
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            direction_vertices = self.find_vertices_by_materials(eye_obj, {self.mat_cornea})
            normal_vec = self.find_average_vertex_normal(eye_obj, direction_vertices)
            eye_rot = normal_vec.to_track_quat('Z', 'Y')

            loc, rot, scale = eye_obj.matrix_world.decompose()
            eye_obj.matrix_world = Matrix.LocRotScale(loc, eye_rot @ rot, scale)

            eye_obj.data.transform(eye_rot.to_matrix().inverted().to_4x4())
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
    def bisect_vertex_clusters(obj: Object, sample_size: int, min_dist: float) -> tuple[list[int], list[int]]:
        mesh = obj.data
        vert_coords = [v.co for v in mesh.vertices]
        n = len(mesh.vertices)

        if n < 2:
            raise Exception(f"Need at least 2 vertices for {obj.name} to separate into clusters!")

        # Find the two farthest points using a random sample for performance
        sample_size = min(n, sample_size)
        sample_indices = random.sample(range(n), sample_size)
        max_dist: float = -1

        idx1, idx2 = 0, 1
        for i in range(sample_size):
            for j in range(i + 1, sample_size):
                ii = sample_indices[i]
                ij = sample_indices[j]
                dist = (vert_coords[ii] - vert_coords[ij]).length
                if dist > max_dist:
                    max_dist = dist
                    idx1, idx2 = ii, ij

        if max_dist < min_dist:
            return [0], []

        # Swap extreme coords if 1 > 2, making this method predictable
        if vert_coords[idx1] > vert_coords[idx2]:
            idx1, idx2 = idx2, idx1

        # Classify each vertex based on proximity to the two farthest points
        cluster_left, cluster_right = [], []
        for i in range(n):
            dist_to_idx1 = (vert_coords[i] - vert_coords[idx1]).length
            dist_to_idx2 = (vert_coords[i] - vert_coords[idx2]).length
            if dist_to_idx1 < dist_to_idx2:
                cluster_left.append(i)
            else:
                cluster_right.append(i)

        print(f"Found clusters with sizes {len(cluster_left)} and {len(cluster_right)} with max distance {max_dist}")
        return cluster_left, cluster_right

    @staticmethod
    def find_center_of_mass(obj: Object, vertex_indices: list[int]) -> Vector:
        center = Vector()
        for i in vertex_indices:
            center += obj.data.vertices[i].co
        center /= len(vertex_indices)
        return center

    @staticmethod
    def find_average_vertex_normal(obj: Object, vertex_indices) -> Vector:
        vector = Vector()
        for i in vertex_indices:
            vector += obj.data.vertices[i].normal
        return vector.normalized()

    @staticmethod
    def set_parent_with_transforms(obj: Object, parent: Object):
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
