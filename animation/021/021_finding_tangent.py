from typing import override
from manim import *

from common.number_plane_group import *
from base_unit_circle import BaseUnitCircle
from rotation_animation import TangentRotation


class FindingTangent(Scene):
    @override
    def construct(self):
        # 좌표계 생성
        npg = NumberPlaneGroup(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        ).scale(1.9)
        self.add(npg)

        unit_circle_triangle = BaseUnitCircle(npg, font_scale_factor=2)
        self.add(unit_circle_triangle)
        self.wait()

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,
            y_length=16
        ).scale(3.5)

        self.play(ReplacementTransform(npg, new_npg))
        unit_circle_triangle.plane_group = new_npg
        unit_circle_triangle.plane = new_npg.plane

        self.play(
            TangentRotation(unit_circle_triangle),
            run_time=16
        )

        self.wait()
