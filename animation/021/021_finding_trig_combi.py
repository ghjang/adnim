from typing import override
from manim import *
from itertools import combinations

from common.number_plane_group import *
from base_unit_circle import BaseUnitCircle

from sine_rotation import SineRotation, CosecantRotation
from cosine_rotation import CosineRotation, SecantRotation
from tangent_rotation import TangentRotation, CotangentRotation


class FindingTrigCombi(Scene):
    def create_rotation_text(self, idx: int, rotation_names: list[str]) -> MathTex:
        """회전 함수들의 이름을 조합하여 텍스트 생성"""
        names_with_comma = ", ".join(rotation_names)
        return MathTex(
            f"\\text{{{idx}. ({names_with_comma})}}",
            color=YELLOW
        ).set_z_index(100).to_corner(UL)

    def animate_rotations(self, idx: int, rotations_list: list, base_unit_circle: BaseUnitCircle):
        """회전 애니메이션 실행"""
        rotation_names = [r.__name__.replace(
            'Rotation', '') for r in rotations_list]
        rotation_text = self.create_rotation_text(idx, rotation_names)

        self.play(FadeIn(rotation_text))
        self.play(
            *[r(base_unit_circle) for r in rotations_list],
            run_time=9
        )
        self.play(FadeOut(rotation_text))

    @override
    def construct(self):
        self.next_section("Initial Setup", skip_animations=False)

        # 좌표계 생성
        npg = NumberPlaneGroup(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        ).scale(1.9)
        self.add(npg)

        # 초기 '단위원' 표시
        base_unit_circle = BaseUnitCircle(npg, font_scale_factor=2)
        unit_circle_text\
            = Text("Unit Circle", font_size=36, color=YELLOW).next_to(base_unit_circle, DOWN)
        self.add(base_unit_circle, unit_circle_text)
        self.wait()

        new_npg = npg.copy_with_transformed_plane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,
            y_length=16
        ).scale(3.5)

        self.play(
            ReplacementTransform(npg, new_npg),
            FadeOut(unit_circle_text)
        )
        base_unit_circle.plane_group = new_npg
        base_unit_circle.plane = new_npg.plane

        self.next_section("Finding Trigonometric Functions, 6",
                          skip_animations=False)

        rotations = [
            SineRotation,        # 첫 번째
            CosineRotation,      # 두 번째
            TangentRotation,     # 세 번째
            CosecantRotation,    # 네 번째
            SecantRotation,      # 다섯 번째
            CotangentRotation    # 여섯 번째
        ]

        # 1. Single Rotations (6C1)
        for idx, rotation in enumerate(rotations, 1):
            self.animate_rotations(idx, [rotation], base_unit_circle)

        # 2. Double Rotations (6C2)
        self.next_section(
            "Finding Trigonometric Combinations, 6C2", skip_animations=False)

        for idx, rotation_pair in enumerate(combinations(rotations, 2), 7):
            self.animate_rotations(idx, rotation_pair, base_unit_circle)

        # 3. Triple Rotations (6C3)
        self.next_section(
            "Finding Trigonometric Combinations, 6C3", skip_animations=False)

        for idx, rotation_triple in enumerate(combinations(rotations, 3), 22):
            self.animate_rotations(idx, rotation_triple, base_unit_circle)

        self.wait()
