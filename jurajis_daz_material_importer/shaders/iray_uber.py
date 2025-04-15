from .material_shader import ShaderGroupApplier, ShaderGroupBuilder

__GROUP_NAME__ = "DAZ Iray Uber"


class IrayUberShaderGroupBuilder(ShaderGroupBuilder):

    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def setup_group(self):
        pass  # TODO: Implement builder


class IrayUberShaderGroupApplier(ShaderGroupApplier):
    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def add_shader_group(self, location: tuple[float, float], channels: dict):
        pass  # TODO: Implement applier
