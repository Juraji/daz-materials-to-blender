from .base import ShaderGroupApplier, ShaderGroupBuilder

from ..utils.dson import DsonMaterialChannel

__GROUP_NAME__ = "iWave Translucent Fabric"
__MATERIAL_TYPE_ID__ = "translucent_fabric"


class IWaveTranslucentFabricShaderGroupBuilder(ShaderGroupBuilder):

    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def setup_group(self):
        super().setup_group()
        # TODO: Implement builder


class IWaveTranslucentFabricShaderGroupApplier(ShaderGroupApplier):
    @staticmethod
    def group_name() -> str:
        return __GROUP_NAME__

    @staticmethod
    def material_type_id() -> str:
        return __MATERIAL_TYPE_ID__

    def add_shader_group(self, location: tuple[float, float], channels: dict[str, DsonMaterialChannel]):
        pass  # TODO: Implement applier
