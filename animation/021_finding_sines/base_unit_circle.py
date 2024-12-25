# fmt: off
import os
import sys

# Python path에 프로젝트 루트 추가
project_dir = os.path.abspath(os.getcwd())
sys.path.append(project_dir)

# 기본 라이브러리
from manim import *

# 사용자 정의 라이브러리
from common.number_plane_group import *
# fmt: on


class BaseUnitCircle(VGroup):
    """단위원과 삼각함수 시각화를 위한 삼각형 그룹 클래스"""

    plane: Mobject
    plane_group: NumberPlaneGroup
    initial_angle: float
    unit_circle: Circle

    # 삼각함수 중 'sin(x)'를 시각화를 위한 도형들
    upper_triangle: Triangle
    lower_triangle: Triangle
    upper_half_chord: Line
    lower_half_chord: Line
    upper_dot: Dot
    lower_dot: Dot

    # 삼각함수 중 'cos(x)'를 시각화를 위한 도형들
    left_triangle: Triangle
    right_triangle: Triangle
    left_half_chord: Line
    right_half_chord: Line
    left_dot: Dot
    right_dot: Dot

    # 브레이스 관련 멤버를 딕셔너리로 관리
    decorations: dict[str, tuple[Brace | None, MathTex | None]] = {}

    def __init__(self,
                 planeGroup: NumberPlaneGroup,
                 initial_angle: float = 0,
                 font_scale_factor: float = 1.0,  # 폰트 스케일 계수
                 text_buff_scale_factor: float = 0.5,  # 텍스트 버퍼 스케일 계수
                 **kwargs):
        super().__init__(**kwargs)
        self.plane = planeGroup.plane
        self.plane_group = planeGroup
        self.initial_angle = initial_angle

        # 단위원 생성
        self.unit_circle = planeGroup.add_circle(
            center_point=[0, 0],
            radius=1,
            color=PINK,
            stroke_width=3
        )
        self.add(self.unit_circle)
        self.decorations = {}  # 초기화

        # 폰트 크기 계산
        self.base_font_size = 36
        self.font_scale = font_scale_factor / \
            abs(planeGroup._get_unit_length())
        self.adjusted_font_size = self.base_font_size * self.font_scale

        # 버퍼 크기 계산
        self.base_buff = 0.1
        self.adjusted_text_buff = (
            self.base_buff * self.font_scale) * text_buff_scale_factor

    def add_shapes_for_sine(self, initial_angle: float | None = None):
        """sin(x) 삼각함수 시각화를 위한 도형 생성"""

        pg = self.plane_group
        angle = initial_angle if initial_angle is not None else self.initial_angle

        # 상단 삼각형 그룹 생성
        self.upper_triangle = pg.add_triangle(
            [0, 0],
            [np.cos(angle), np.sin(angle)],
            [np.cos(angle), 0]
        )

        # BasicShapeMixin의 메서드를 사용하여 점과 선 생성
        circle_point = [np.cos(angle), np.sin(angle)]
        x_point = [np.cos(angle), 0]

        self.upper_dot = pg.add_point(circle_point, color=GREEN)
        self.upper_half_chord = pg.add_line(
            circle_point,
            x_point,
            color=WHITE,
            stroke_width=4
        )

        # 하단 삼각형 그룹 생성 (y좌표 반전)
        lower_circle_point = [np.cos(angle), -np.sin(angle)]
        self.lower_triangle = pg.add_triangle(
            [0, 0],
            lower_circle_point,
            x_point,
        ).set_opacity(0.1)

        self.lower_dot = pg.add_point(lower_circle_point, color=GREEN)
        self.lower_half_chord = pg.add_line(
            lower_circle_point,
            x_point,
            color=WHITE,
            stroke_width=4
        ).set_opacity(0.5)

        # NOTE: VGroup에 모든 객체 추가 (브레이스 제외)
        self.add(
            self.upper_triangle,
            self.lower_triangle,
            self.upper_half_chord,
            self.lower_half_chord,
            self.upper_dot,
            self.lower_dot
        )

    def remove_shapes_for_sine(self):
        """sin(x) 삼각함수 시각화 도형 제거"""

        # 도형들 제거
        removed_objects = [
            self.upper_triangle,
            self.lower_triangle,
            self.upper_half_chord,
            self.lower_half_chord,
            self.upper_dot,
            self.lower_dot
        ]

        self.remove(*removed_objects)
        self.plane_group.remove(*removed_objects)

        # 멤버 변수들을 None으로 설정
        self.upper_triangle = None
        self.lower_triangle = None
        self.upper_half_chord = None
        self.lower_half_chord = None
        self.upper_dot = None
        self.lower_dot = None

        # 싸인 브레이스와 라벨 제거
        if "sine" in self.decorations:
            brace, label = self.decorations["sine"]
            if brace is not None:
                self.remove(brace, label)
                self.plane_group.remove_brace("sine_brace")
            self.decorations.pop("sine")

        return removed_objects

    def add_shapes_for_cosine(self, initial_angle: float | None = None):
        """cos(x) 삼각함수 시각화를 위한 도형 생성"""
        pg = self.plane_group
        angle = initial_angle if initial_angle is not None else self.initial_angle

        # 우측 삼각형 그룹 생성
        self.right_triangle = pg.add_triangle(
            [0, 0],
            [np.cos(angle), np.sin(angle)],
            [0, np.sin(angle)]
        )

        # BasicShapeMixin의 메서드를 사용하여 점과 선 생성
        circle_point = [np.cos(angle), np.sin(angle)]
        y_point = [0, np.sin(angle)]

        self.right_dot = pg.add_point(circle_point, color=GREEN)
        self.right_half_chord = pg.add_line(
            circle_point,
            y_point,
            color=WHITE,
            stroke_width=4
        )

        # 좌측 삼각형 그룹 생성 (x좌표 반전)
        left_circle_point = [-np.cos(angle), np.sin(angle)]
        self.left_triangle = pg.add_triangle(
            [0, 0],
            left_circle_point,
            y_point,
        ).set_opacity(0.1)

        self.left_dot = pg.add_point(left_circle_point, color=GREEN)
        self.left_half_chord = pg.add_line(
            left_circle_point,
            y_point,
            color=WHITE,
            stroke_width=4
        ).set_opacity(0.5)

        # VGroup에 모든 객체 추가
        self.add(
            self.right_triangle,
            self.left_triangle,
            self.right_half_chord,
            self.left_half_chord,
            self.right_dot,
            self.left_dot
        )

    def remove_shapes_for_cosine(self):
        """cos(x) 삼각함수 시각화 도형 제거"""
        # 도형들 제거
        removed_objects = [
            self.right_triangle,
            self.left_triangle,
            self.right_half_chord,
            self.left_half_chord,
            self.right_dot,
            self.left_dot
        ]

        self.remove(*removed_objects)
        self.plane_group.remove(*removed_objects)

        # 멤버 변수들을 None으로 설정
        self.right_triangle = None
        self.left_triangle = None
        self.right_half_chord = None
        self.left_half_chord = None
        self.right_dot = None
        self.left_dot = None

        # 코싸인 브레이스와 라벨 제거
        if "cosine" in self.decorations:
            brace, label = self.decorations["cosine"]
            if brace is not None:
                self.remove(brace, label)
                self.plane_group.remove_brace("cosine_brace")
            self.decorations.pop("cosine")

        return removed_objects
