from typing import override
from manim import *

from common.number_plane_group import *
from base_unit_circle import BaseUnitCircle
from rotation_animation import (
    SineRotation,
    CosineRotation
)


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

        unit_circle_triangle = BaseUnitCircle(npg, font_scale_factor=2)
        self.add(unit_circle_triangle)

        self.play(
            SineRotation(unit_circle_triangle),
            run_time=9
        )
        self.play(
            npg.animate.scale(0.5).to_edge(LEFT)
        )
        self.play(
            SineRotation(unit_circle_triangle, show_brace=False),
            run_time=4.5
        )

        self.wait()


class FindingCosine(Scene):
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

        unit_circle_triangle = BaseUnitCircle(npg, font_scale_factor=1.75)
        self.add(unit_circle_triangle)

        self.play(
            CosineRotation(unit_circle_triangle),
            run_time=9
        )
        self.play(
            npg.animate.scale(0.5).to_edge(LEFT)
        )
        self.play(
            CosineRotation(unit_circle_triangle, show_brace=False),
            run_time=4.5
        )

        self.wait()


class FindingSines(Scene):
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

        unit_circle_triangle = BaseUnitCircle(npg, font_scale_factor=1.75)
        self.add(unit_circle_triangle)

        self.play(
            SineRotation(unit_circle_triangle),
            CosineRotation(unit_circle_triangle),
            run_time=9
        )

        self.wait()


class FindingAll(Scene):
    @override
    def construct(self):
        # 원본 크기의 좌표계를 생성하고 scale 조정
        original_scale = 1.1  # 크기 살짝 키움

        # 세 개의 좌표계와 삼각형 쌍을 생성하고 VGroup으로 묶음
        pairs = VGroup()
        for _ in range(3):
            plane = NumberPlaneGroup(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=4,
                y_length=4
            ).scale(original_scale)

            c = BaseUnitCircle(plane)

            # 각 쌍을 VGroup으로 묶음
            pair = VGroup(plane, c)
            pairs.add(pair)

        # 요소들 사이에 간격을 두고 수평 정렬
        pairs.arrange(RIGHT, buff=0.2)
        pairs.center()  # 전체를 중앙 정렬

        # 씬에 추가
        self.add(pairs)

        # 각각의 애니메이션 실행
        self.play(
            SineRotation(pairs[0][1]),     # 왼쪽: sine
            CosineRotation(pairs[1][1]),   # 중앙: cosine
            SineRotation(pairs[2][1]),     # 오른쪽: sine + cosine
            CosineRotation(pairs[2][1]),   # 오른쪽: sine + cosine
            run_time=9
        )

        self.wait()
