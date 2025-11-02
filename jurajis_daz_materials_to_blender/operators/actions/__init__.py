from .import_all_materials import ImportAllMaterialsOperator
from .import_object_materials import ImportObjectMaterialsOperator
from .import_shader_group import ImportShaderGroupOperator
from .create_instances import CreateInstancesOperator
from .convert_materials import ConvertMaterialsOperator, MaterialItem
from .separate_genesis8_eyes import SeparateGenesis8EyesOperator
from .separate_genesis9_eyes import SeparateGenesis9EyesOperator


def register():
    from bpy.utils import register_class

    register_class(ImportAllMaterialsOperator)
    register_class(ImportObjectMaterialsOperator)
    register_class(ImportShaderGroupOperator)
    register_class(CreateInstancesOperator)
    register_class(MaterialItem)
    register_class(ConvertMaterialsOperator)
    register_class(SeparateGenesis8EyesOperator)
    register_class(SeparateGenesis9EyesOperator)


def unregister():
    from bpy.utils import unregister_class

    unregister_class(ImportAllMaterialsOperator)
    unregister_class(ImportObjectMaterialsOperator)
    unregister_class(ImportShaderGroupOperator)
    unregister_class(CreateInstancesOperator)
    unregister_class(MaterialItem)
    unregister_class(ConvertMaterialsOperator)
    unregister_class(SeparateGenesis9EyesOperator)
