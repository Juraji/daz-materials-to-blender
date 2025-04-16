from .base import ShaderGroupApplier, ShaderGroupBuilder

__GROUP_NAME__ = "DAZ Iray Uber"

from ..utils.dson import DsonMaterialChannel


class IrayUberShaderGroupBuilder(ShaderGroupBuilder):

    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def setup_group(self):
        super().setup_group()
        pass  # TODO: Implement builder


class IrayUberShaderGroupApplier(ShaderGroupApplier):
    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def add_shader_group(self, location: tuple[float, float], channels: dict[str, DsonMaterialChannel]):
        pass  # TODO: Implement applier
