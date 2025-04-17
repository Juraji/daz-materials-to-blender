from .base import ShaderGroupApplier, ShaderGroupBuilder

from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "DAZ Iray Uber"
__MATERIAL_TYPE_ID__ = "iray_uber"


class IrayUberShaderGroupBuilder(ShaderGroupBuilder):

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def setup_group(self):
        super().setup_group()
        pass  # TODO: Implement builder


class IrayUberShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def add_shader_group(self, channels: dict[str, DsonMaterialChannel]):
        pass # TODO: Implement applier
