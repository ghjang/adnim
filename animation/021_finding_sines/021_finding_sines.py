# fmt: off
import os
import sys

# Python path에 프로젝트 루트 추가
project_dir = os.path.abspath(os.getcwd())
sys.path.append(project_dir)

# 기본 라이브러리
from typing import override
from manim import *

# 프로젝트 모듈
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


class SineRotation(Animation):
    """단위원에서 '싸인 활꼴 회전'을 시각화하는 애니메이션"""

    clockwise: bool
    unit_circle_triangle: BaseUnitCircle
    rotation_count: int
    show_brace: bool
    remove_shapes: bool

    def __init__(
        self,
        unit_circle_triangle: BaseUnitCircle,
        clockwise: bool = False,
        rotation_count: int = 1,
        show_brace: bool = True,
        remove_shapes: bool = True,
        **kwargs
    ):
        super().__init__(unit_circle_triangle, **kwargs)
        self.clockwise = clockwise
        self.unit_circle_triangle = unit_circle_triangle
        self.rotation_count = rotation_count  # 회전 횟수 추가
        self.show_brace = show_brace  # 브레이스 표시 여부
        self.remove_shapes = remove_shapes  # 애니메이션 종료 시 도형 제거 여부

    @override
    def begin(self):
        self.unit_circle_triangle.add_shapes_for_sine()
        return super().begin()

    @override
    def finish(self):
        retVal = super().finish()
        if self.remove_shapes:
            self.unit_circle_triangle.remove_shapes_for_sine()
        return retVal

    @override
    def interpolate_mobject(self, alpha):
        # 첫 프레임에서는 브레이스를 표시하지 않음
        show_brace_for_frame = self.show_brace and alpha > 0

        # initial_angle부터 시작하여 회전
        angle = self.unit_circle_triangle.initial_angle + \
            (alpha * TAU * self.rotation_count)
        if self.clockwise:
            angle = self.unit_circle_triangle.initial_angle - \
                (alpha * TAU * self.rotation_count)

        x = np.cos(angle)
        y = np.sin(angle)

        # 평면 좌표로 변환
        plane = self.unit_circle_triangle.plane
        origin = plane.c2p(0, 0)
        circle_point = plane.c2p(x, y)
        x_point = plane.c2p(x, 0)

        # 삼각형 업데이트
        triangle_points = [origin, circle_point, x_point, origin]
        lower_points = [
            origin,
            plane.c2p(x, -y),
            x_point,
            origin
        ]  # 하단 삼각형은 y 좌표만 반전

        # 상단 삼각형
        self.unit_circle_triangle.upper_triangle.set_points_as_corners(
            triangle_points)

        # 하단 삼각형 (flip 불필요)
        self.unit_circle_triangle.lower_triangle.set_points_as_corners(
            lower_points)

        # 현 업데이트
        self.unit_circle_triangle.upper_half_chord.set_points_by_ends(
            circle_point, x_point)
        self.unit_circle_triangle.lower_half_chord.set_points_by_ends(
            plane.c2p(x, -y), x_point)

        # 현의 높이(sin 값)가 일정 크기 이상일 때만 브레이스 표시
        height = abs(y)

        # 현재 좌표계의 스케일을 고려한 최소 높이 계산
        unit_y = abs(self.unit_circle_triangle.plane.c2p(0, 1)[1] -
                     self.unit_circle_triangle.plane.c2p(0, 0)[1])
        min_height = 0.1 * unit_y

        # 기존 브레이스 제거
        if "sine" in self.unit_circle_triangle.decorations:
            brace, label = self.unit_circle_triangle.decorations["sine"]
            if brace is not None:
                self.unit_circle_triangle.remove(brace, label)
                self.unit_circle_triangle.plane_group.remove_brace(
                    "sine_brace")
            self.unit_circle_triangle.decorations.pop("sine")

        # 브레이스 표시 여부에 따라 처리
        if show_brace_for_frame and height > min_height:
            # x 값에 따라 브레이스가 붙을 현의 방향 결정
            brace_direction = RIGHT  # 1, 4분면 (x >= 0)
            if x < 0:  # 2, 3분면
                brace_direction = LEFT

            # 미리 계산된 폰트 크기 사용
            brace, label = self.unit_circle_triangle.plane_group.add_brace(
                self.unit_circle_triangle.upper_half_chord,
                direction=brace_direction,
                name="sine_brace",
                text="\\sin(x)",
                color=YELLOW,
                text_color=YELLOW,
                buff=self.unit_circle_triangle.base_buff,  # 기본 버퍼 사용
                text_buff=self.unit_circle_triangle.adjusted_text_buff,  # 조정된 버퍼 사용
                font_size=self.unit_circle_triangle.adjusted_font_size
            )

            # z_index 설정으로 항상 위에 표시
            brace.set_z_index(2)
            label.set_z_index(2)

            # VGroup에 추가하기 전에 기존 객체들의 z_index 확인
            for mob in self.unit_circle_triangle.submobjects:
                if not hasattr(mob, 'z_index'):
                    mob.set_z_index(0)

            # VGroup에도 추가
            self.unit_circle_triangle.add(brace, label)
            self.unit_circle_triangle.decorations["sine"] = (brace, label)

        # 점 업데이트
        self.unit_circle_triangle.upper_dot.move_to(circle_point)
        self.unit_circle_triangle.lower_dot.move_to(plane.c2p(x, -y))


class CosineRotation(Animation):
    """단위원에서 '코싸인 활꼴 회전'을 시각화하는 애니메이션"""

    clockwise: bool
    unit_circle_triangle: BaseUnitCircle
    rotation_count: int
    show_brace: bool
    remove_shapes: bool

    def __init__(
        self,
        unit_circle_triangle: BaseUnitCircle,
        clockwise: bool = False,
        rotation_count: int = 1,
        show_brace: bool = True,
        remove_shapes: bool = True,
        **kwargs
    ):
        super().__init__(unit_circle_triangle, **kwargs)
        self.clockwise = clockwise
        self.unit_circle_triangle = unit_circle_triangle
        self.rotation_count = rotation_count
        self.show_brace = show_brace
        self.remove_shapes = remove_shapes

    @override
    def begin(self):
        self.unit_circle_triangle.add_shapes_for_cosine()
        return super().begin()

    @override
    def finish(self):
        retVal = super().finish()
        if self.remove_shapes:
            self.unit_circle_triangle.remove_shapes_for_cosine()
        return retVal

    @override
    def interpolate_mobject(self, alpha):
        # 첫 프레임에서는 브레이스를 표시하지 않음
        show_brace_for_frame = self.show_brace and alpha > 0

        # 회전 각도 계산 방식 수정
        total_rotation = TAU * self.rotation_count
        if self.clockwise:
            total_rotation = -total_rotation

        # initial_angle을 시작점으로, 거기서부터 total_rotation만큼 회전
        angle = self.unit_circle_triangle.initial_angle + \
            (alpha * total_rotation)

        x = np.cos(angle)
        y = np.sin(angle)

        # 평면 좌표로 변환
        plane = self.unit_circle_triangle.plane
        origin = plane.c2p(0, 0)
        circle_point = plane.c2p(x, y)
        y_point = plane.c2p(0, y)  # cosine은 y축 기준점

        # 삼각형 업데이트
        triangle_points = [origin, circle_point, y_point, origin]
        left_points = [
            origin,
            plane.c2p(-x, y),  # x좌표 반전
            y_point,
            origin
        ]

        # 우측 삼각형
        self.unit_circle_triangle.right_triangle.set_points_as_corners(
            triangle_points)

        # 좌측 삼각형
        self.unit_circle_triangle.left_triangle.set_points_as_corners(
            left_points)

        # 현 업데이트
        self.unit_circle_triangle.right_half_chord.set_points_by_ends(
            circle_point, y_point)
        self.unit_circle_triangle.left_half_chord.set_points_by_ends(
            plane.c2p(-x, y), y_point)

        # 현의 너비(cos 값)가 일정 크기 이상일 때만 브레이스 표시
        width = abs(x)

        # 현재 좌표계의 스케일을 고려한 최소 너비 계산
        unit_x = abs(self.unit_circle_triangle.plane.c2p(1, 0)[0] -
                     self.unit_circle_triangle.plane.c2p(0, 0)[0])
        min_width = 0.1 * unit_x

        # 기존 브레이스 제거
        if "cosine" in self.unit_circle_triangle.decorations:
            brace, label = self.unit_circle_triangle.decorations["cosine"]
            if brace is not None:
                self.unit_circle_triangle.remove(brace, label)
                self.unit_circle_triangle.plane_group.remove_brace(
                    "cosine_brace")
            self.unit_circle_triangle.decorations.pop("cosine")

        # 브레이스 표시 여부에 따라 처리
        if show_brace_for_frame and width > min_width:
            # y 값에 따라 브레이스가 붙을 현의 방향 결정
            brace_direction = UP  # 1, 2분면 (y >= 0)
            if y < 0:  # 3, 4분면
                brace_direction = DOWN

            # 미리 계산된 폰트 크기 사용
            brace, label = self.unit_circle_triangle.plane_group.add_brace(
                self.unit_circle_triangle.right_half_chord,
                direction=brace_direction,
                name="cosine_brace",
                text="\\cos(x)",
                color=YELLOW,
                text_color=YELLOW,
                buff=self.unit_circle_triangle.base_buff,  # 기본 버퍼 사용
                text_buff=self.unit_circle_triangle.adjusted_text_buff,  # 조정된 버퍼 사용
                font_size=self.unit_circle_triangle.adjusted_font_size
            )

            # z_index 설정
            brace.set_z_index(2)
            label.set_z_index(2)

            # VGroup에 추가하기 전에 기존 객체들의 z_index 확인
            for mob in self.unit_circle_triangle.submobjects:
                if not hasattr(mob, 'z_index'):
                    mob.set_z_index(0)

            # VGroup에도 추가
            self.unit_circle_triangle.add(brace, label)
            self.unit_circle_triangle.decorations["cosine"] = (brace, label)

        # 점 업데이트
        self.unit_circle_triangle.right_dot.move_to(circle_point)
        self.unit_circle_triangle.left_dot.move_to(plane.c2p(-x, y))


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

        unit_circle_triangle = BaseUnitCircle(npg)
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

        unit_circle_triangle = BaseUnitCircle(npg)
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

        unit_circle_triangle = BaseUnitCircle(npg)
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
