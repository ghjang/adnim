from typing import override
from manim import *

from common.number_plane_group import NumberPlaneGroup
from base_unit_circle import BaseUnitCircle
from rotation_animation import (
    SineRotation,
    CosineRotation,
    TangentRotation,
)


class FindingAllTrigs(Scene):
    @override
    def construct(self):
        npg = NumberPlaneGroup().scale(3.5)
        self.add(npg)

        base_unit_circle = BaseUnitCircle(npg)
        self.add(base_unit_circle)

        self.play(
            SineRotation(base_unit_circle),
            CosineRotation(base_unit_circle),
            TangentRotation(base_unit_circle),
            run_time=9
        )

        self.wait(0.3)

        self.play(
            SineRotation(base_unit_circle, show_brace=False),
            CosineRotation(base_unit_circle, show_brace=False),
            TangentRotation(base_unit_circle, show_brace=False),
            run_time=9
        )

        self.wait()
