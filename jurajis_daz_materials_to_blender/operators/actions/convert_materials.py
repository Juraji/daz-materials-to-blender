import bpy
from bpy.props import StringProperty, BoolProperty, CollectionProperty, EnumProperty
from bpy.types import Operator, PropertyGroup

from .import_object_materials import MATERIAL_TYPE_ID_PROP
from ..base import OperatorReportMixin
from ...converters import SHADER_GROUP_CONVERTERS_ENUM_OPTS, converter_by_cls_name


class MaterialItem(PropertyGroup):
    name: StringProperty()
    select: BoolProperty(name="Select", default=False)


class ConvertMaterialsOperator(OperatorReportMixin, Operator):
    bl_idname = "daz_import.select_materials_to_convert"
    bl_label = "Convert Materials"
    bl_options = {'REGISTER', 'UNDO'}

    materials_to_convert: CollectionProperty(type=MaterialItem)
    conversion_type: EnumProperty(
        name="Conversion Type",
        items=SHADER_GROUP_CONVERTERS_ENUM_OPTS
    )
    keep_original_group: BoolProperty(name="Keep Original Group", default=False)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and len(obj.material_slots) > 0

    def invoke(self, context, event):
        wm = context.window_manager
        obj = context.active_object

        # Clear previous items
        self.materials_to_convert.clear()

        if obj and obj.type == 'MESH':
            seen = set()
            for slot in obj.material_slots:
                if slot.material and slot.material.name not in seen:
                    item = self.materials_to_convert.add()
                    item.name = slot.material.name
                    seen.add(item.name)

        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        conversion_type = converter_by_cls_name(self.conversion_type)

        layout.prop(self, "conversion_type")
        layout.prop(self, "keep_original_group")

        layout.label(text=f"Select materials to convert for '{obj.name}':")
        for item in self.materials_to_convert:
            mat = bpy.data.materials.get(item.name)
            if (mat and MATERIAL_TYPE_ID_PROP in mat
                    and mat[MATERIAL_TYPE_ID_PROP] == conversion_type.from_type.material_type_id()):
                row = layout.row()
                row.prop(item, "select", text=item.name)

    def execute(self, context):
        selected_materials_names = self.materials_to_convert
        selected_materials = [
            bpy.data.materials[mat_item.name]
            for mat_item in selected_materials_names
            if mat_item.select
        ]

        converter_cls = converter_by_cls_name(self.conversion_type)
        converter = converter_cls()

        # noinspection PyUnresolvedReferences
        bpy.ops.daz_import.import_shader_group(silent=True, group_name=converter_cls.to_type.group_name())

        converter.convert_materials(selected_materials, self.keep_original_group)

        for mat in selected_materials:
            mat[MATERIAL_TYPE_ID_PROP] = converter_cls.to_type.material_type_id()

        return {"FINISHED"}
