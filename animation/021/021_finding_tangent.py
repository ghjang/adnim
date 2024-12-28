from typing import override
from manim import *

from common.number_plane_group import *
from base_unit_circle import BaseUnitCircle
from rotation_animation import TangentRotation, CotangentRotation


class FindingTangent(Scene):
    @override
    def construct(self):
        self.next_section("Initial Setup", skip_animations=True)

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
        self.wait()

        self.next_section("Finding Tangent Main", skip_animations=False)

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,
            y_length=16
        ).scale(3.5)

        self.play(ReplacementTransform(npg, new_npg))
        base_unit_circle.plane_group = new_npg
        base_unit_circle.plane = new_npg.plane

        self.play(
            TangentRotation(base_unit_circle),
            run_time=16
        )

        self.wait()


class FindingCotangent(Scene):
    @override
    def construct(self):
        self.next_section("Initial Setup", skip_animations=True)

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
        self.wait()

        self.next_section("Finding Cotangent Main", skip_animations=False)

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,
            y_length=16
        ).scale(3.5)

        self.play(ReplacementTransform(npg, new_npg))
        base_unit_circle.plane_group = new_npg
        base_unit_circle.plane = new_npg.plane

        self.play(
            CotangentRotation(base_unit_circle),
            run_time=16
        )

        self.wait()


class FindingAllTangents(Scene):
    @override
    def construct(self):
        self.next_section("Initial Setup", skip_animations=True)

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
        self.wait()

        self.next_section("Finding Cotangent Main", skip_animations=False)

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,
            y_length=16
        ).scale(3.5)

        self.play(ReplacementTransform(npg, new_npg))
        base_unit_circle.plane_group = new_npg
        base_unit_circle.plane = new_npg.plane

        self.play(
            TangentRotation(base_unit_circle),
            CotangentRotation(base_unit_circle),
            run_time=16
        )

        self.wait()
