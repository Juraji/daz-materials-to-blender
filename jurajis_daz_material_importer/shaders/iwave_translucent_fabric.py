from .material_shader import ShaderGroupApplier, ShaderGroupBuilder

__GROUP_NAME__ = "iWave Translucent Fabric"


class IWaveTranslucentFabricShaderGroupBuilder(ShaderGroupBuilder):

    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def setup_group(self):
        pass  # TODO: Implement builder


class IWaveTranslucentFabricShaderGroupApplier(ShaderGroupApplier):
    @classmethod
    def group_name(cls) -> str:
        return __GROUP_NAME__

    def add_shader_group(self, location: tuple[float, float], channels: dict):
        pass  # TODO: Implement applier
