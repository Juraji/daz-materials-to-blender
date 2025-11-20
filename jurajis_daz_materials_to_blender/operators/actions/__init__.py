from .import_all_materials import ImportAllMaterialsOperator
from .import_object_materials import ImportObjectMaterialsOperator
from .import_shader_group import ImportShaderGroupOperator
from .create_instances import CreateInstancesOperator
from .convert_materials import ConvertMaterialsOperator, MaterialItem
from .separate_genesis8_eyes import SeparateGenesis8EyesOperator
from .separate_genesis9_eyes import SeparateGenesis9EyesOperator
from .clear_custom_split_normals import ClearCustomSplitNormalsOperator


__CLASSES__ = [
    ImportAllMaterialsOperator,
    ImportObjectMaterialsOperator,
    ImportShaderGroupOperator,
    CreateInstancesOperator,
    MaterialItem,
    ConvertMaterialsOperator,
    SeparateGenesis8EyesOperator,
    SeparateGenesis9EyesOperator,
    ClearCustomSplitNormalsOperator,
]

def register():
    from bpy.utils import register_class

    for cls in __CLASSES__:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(__CLASSES__):
        unregister_class(cls)
