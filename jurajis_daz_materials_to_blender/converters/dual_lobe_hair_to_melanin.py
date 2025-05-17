from bpy.types import ShaderNodeTree, ShaderNodeGroup

from .shader_group_converter import ShaderGroupConverter
from ..shaders import BlendedDualLobeHairShaderApplier
from ..shaders.melanin_dual_lobe_hair import MelaninDualLobeHairShaderApplier
from ..utils.node_trees import get_color_socket_value, get_float_socket_value, set_socket_value


class DualLobeHairToMelaninShaderConverter(ShaderGroupConverter):
    from_type = BlendedDualLobeHairShaderApplier
    to_type = MelaninDualLobeHairShaderApplier
    display_name = "Blended Dual Lobe Hair To Melanin Based"

    @classmethod
    def property_mapping(cls) -> list[tuple[str, str]]:
        i = cls.from_type
        o = cls.to_type

        return [
            (i.IN_HAIR_ROOT_COLOR_MAP, o.IN_BASE_ROOT_TINT),
            (i.IN_HAIR_TIP_COLOR_MAP, o.IN_BASE_TIP_TINT),

            (i.IN_HIGHLIGHT_WEIGHT, o.IN_HIGHLIGHTS_WEIGHT),
            (i.IN_HIGHLIGHT_ROOT_COLOR_MAP, o.IN_HIGHLIGHTS_ROOT_TINT),
            (i.IN_TIP_HIGHLIGHT_COLOR_MAP, o.IN_HIGHLIGHTS_TIP_TINT),

            (i.IN_ROUGHNESS, o.IN_ROUGHNESS),
            (i.IN_GLOSSY_LAYER_WEIGHT, o.IN_GLOSSY_COAT),

            (i.IN_ROOT_TO_TIP_GEOMETRY_DATA, o.IN_ROOT_TO_TIP_COORDINATES),
            (i.IN_ROOT_TO_TIP_BIAS, o.IN_ROOT_TO_TIP_BIAS),
            (i.IN_ROOT_TO_TIP_GAIN, o.IN_ROOT_TO_TIP_GAIN),
        ]

    # noinspection DuplicatedCode
    @classmethod
    def convert_material(cls,
                         mapping: list[tuple[str, str]],
                         node_tree: ShaderNodeTree,
                         org_group: ShaderNodeGroup,
                         new_group: ShaderNodeGroup):
        super().convert_material(mapping, node_tree, org_group, new_group)
        i = cls.from_type
        o = cls.to_type

        root_color_value = get_color_socket_value(org_group, i.IN_HAIR_ROOT_COLOR)
        tip_color_value = get_color_socket_value(org_group, i.IN_HAIR_TIP_COLOR)

        root_melanin, root_redness = cls._color_to_melanin(root_color_value)
        tip_melanin, tip_redness = cls._color_to_melanin(tip_color_value)
        avg_redness = (root_redness + tip_redness) / 2

        set_socket_value(new_group, o.IN_BASE_ROOT_MELANIN, root_melanin)
        set_socket_value(new_group, o.IN_BASE_TIP_MELANIN, tip_melanin)
        set_socket_value(new_group, o.IN_BASE_MELANIN_REDNESS, avg_redness)

        highlight_weight = get_float_socket_value(org_group, i.IN_HIGHLIGHT_WEIGHT)
        if highlight_weight > 0:  # Skip if no highlights are used
            highlight_root_color_value = get_color_socket_value(org_group, i.IN_HIGHLIGHT_ROOT_COLOR)
            highlight_tip_color_value = get_color_socket_value(org_group, i.IN_TIP_HIGHLIGHT_COLOR)

            root_melanin, root_redness = cls._color_to_melanin(highlight_root_color_value)
            tip_melanin, tip_redness = cls._color_to_melanin(highlight_tip_color_value)
            avg_redness = (root_redness + tip_redness) / 2

            set_socket_value(new_group, o.IN_HIGHLIGHTS_ROOT_MELANIN, root_melanin)
            set_socket_value(new_group, o.IN_HIGHLIGHTS_TIP_MELANIN, tip_melanin)
            set_socket_value(new_group, o.IN_HIGHLIGHTS_MELANIN_REDNESS, avg_redness)

    @classmethod
    def _color_to_melanin(cls, rgba: tuple[float, float, float, float]) -> tuple[float, float]:
        r, g, b, _ = rgba
        eps = 1e-6
        falloff = 0.15

        # 1) Compute linear luminance (Rec. 709)
        luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b)  ** falloff

        # 2) Melanin ≈ how far below white you are
        melanin = 1.0 - luminance
        melanin = max(0.0, min(1.0, melanin))

        # 3) Redness: how much red stands out *relative* to your melanin amount
        #    (if melanin is near zero, redness → 0)
        red_diff = r - (g + b) * 0.5
        redness = red_diff / (melanin + eps)
        redness = max(0.0, min(1.0, redness))

        return melanin, redness
