from typing import override
from manim import *

from common.number_plane_group import *
from base_unit_circle import BaseUnitCircle
from sine_rotation import SineRotation, CosecantRotation


class FindingSine(Scene):
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

        base_unit_circle = BaseUnitCircle(npg, font_scale_factor=2)
        self.add(base_unit_circle)

        self.play(
            SineRotation(base_unit_circle),
            run_time=9
        )
        self.play(npg.animate.scale(0.5).to_edge(LEFT))
        self.play(
            SineRotation(base_unit_circle, show_brace=False),
            run_time=4.5
        )

        self.wait()


class FindingCosecant(Scene):
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

        base_unit_circle = BaseUnitCircle(npg, font_scale_factor=2)
        self.add(base_unit_circle)

        self.play(
            CosecantRotation(base_unit_circle),
            run_time=9
        )
        self.play(npg.animate.scale(0.5).to_edge(LEFT))
        self.play(
            CosecantRotation(base_unit_circle, show_brace=False),
            run_time=4.5
        )

        self.wait()

class FindingSineAndCosecant(Scene):
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

        base_unit_circle = BaseUnitCircle(npg, font_scale_factor=2)
        self.add(base_unit_circle)

        self.play(
            SineRotation(base_unit_circle),
            CosecantRotation(base_unit_circle),
            run_time=9
        )
        self.play(npg.animate.scale(0.5).to_edge(LEFT))
        self.play(
            SineRotation(base_unit_circle, show_brace=False),
            CosecantRotation(base_unit_circle, show_brace=False),
            run_time=4.5
        )

        self.wait()
