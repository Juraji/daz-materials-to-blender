from typing import cast

import bpy
from bpy.types import ShaderNodeRGBCurve

if __name__ == "__main__":
    ng = bpy.data.node_groups["DAZ LUT Correction"]
    node = cast(ShaderNodeRGBCurve, ng.nodes["RGB Curves"])

    curve_r = node.mapping.curves[0]
    curve_r.points.new(0.0, 0.0)
    curve_r.points.new(0.1428571, 0.0138953)
    curve_r.points.new(0.2857143, 0.0637371)
    curve_r.points.new(0.4285714, 0.155367)
    curve_r.points.new(0.5714286, 0.2923586)
    curve_r.points.new(0.7142857, 0.4773961)
    curve_r.points.new(0.8571429, 0.7126597)
    curve_r.points.new(1.0, 1.0)

    curve_g = node.mapping.curves[1]
    curve_g.points.new(0.0, 0.0)
    curve_g.points.new(0.1428571, 0.0137095)
    curve_g.points.new(0.2857143, 0.0631871)
    curve_g.points.new(0.4285714, 0.154459)
    curve_g.points.new(0.5714286, 0.2912289)
    curve_g.points.new(0.7142857, 0.476286)
    curve_g.points.new(0.8571429, 0.7119001)
    curve_g.points.new(1.0, 1.0)

    curve_b = node.mapping.curves[2]
    curve_b.points.new(0.0, 0.0)
    curve_b.points.new(0.1428571, 0.0136942)
    curve_b.points.new(0.2857143, 0.0631415)
    curve_b.points.new(0.4285714, 0.1543835)
    curve_b.points.new(0.5714286, 0.291135)
    curve_b.points.new(0.7142857, 0.4761937)
    curve_b.points.new(0.8571429, 0.7118369)
    curve_b.points.new(1.0, 1.0)

    node.mapping.update()
