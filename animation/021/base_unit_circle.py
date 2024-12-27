from manim import *
from common.number_plane_group import *
from enum import IntEnum
from dataclasses import dataclass


class ZIndexEnum(IntEnum):
    """삼각함수 시각화에서 사용되는 z-index 값들"""
    BACKGROUND = 0      # 기본 배경
    GRID = 1           # 격자
    BASE_SHAPES = 11   # 기본 도형들 (삼각형, 원 등)
    LINES = 12         # 선들 (현, 반지름 등)
    POINTS = 13        # 점들
    DECORATIONS = 14   # 브레이스, 라벨 등


@dataclass
class StyleConfig:
    """삼각함수 시각화에서 사용되는 스타일 설정"""
    # 기본 색상
    UNIT_CIRCLE_COLOR = PINK
    POINT_COLOR = GREEN
    LINE_COLOR = WHITE
    SHAPE_COLOR = BLUE
    BRACE_COLOR = YELLOW
    BRACE_TEXT_COLOR = YELLOW

    # 선 두께
    UNIT_CIRCLE_STROKE_WIDTH = 3
    CHORD_STROKE_WIDTH = 4
    RADIUS_STROKE_WIDTH = 3
    TANGENT_STROKE_WIDTH = 2
    HYPOTENUSE_STROKE_WIDTH = 5
    SHAPE_STROKE_WIDTH = 2

    # 투명도
    TANGENT_LINE_OPACITY = 0.5
    SECONDARY_SHAPE_OPACITY = 0.1  # 반전된 도형의 투명도
    SHAPE_FILL_OPACITY = 0.2
    TRIANGLE_FILL_OPACITY = 0.5

    # 점 크기
    DOT_RADIUS = DEFAULT_DOT_RADIUS


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

    # 삼각함수 중 'tan(x)'를 시각화를 위한 도형들
    point_of_tangency: Dot
    x_axis_intercept: Dot
    circle_radius: Line
    tangent_line: Line
    hypotenuse: Line
    inner_triangle: Triangle
    tangent_triangle: Triangle

    # 브레이스 관련 멤버를 딕셔너리로 관리
    decorations: dict[str, tuple[Brace | None, MathTex | None]] = {}

    def __init__(self,
                 planeGroup: NumberPlaneGroup,
                 initial_angle: float = 0,
                 base_font_size: int = 36,
                 font_scale_factor: float = 1.0,       # 폰트 스케일 계수
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
            color=StyleConfig.UNIT_CIRCLE_COLOR,
            stroke_width=StyleConfig.UNIT_CIRCLE_STROKE_WIDTH
        )
        self.add(self.unit_circle)
        self.decorations = {}  # 초기화

        # 폰트 크기 계산
        self.base_font_size = base_font_size
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

        self.upper_dot = pg.add_point(
            circle_point,
            color=StyleConfig.POINT_COLOR,
            radius=StyleConfig.DOT_RADIUS
        ).set_z_index(ZIndexEnum.POINTS)
        self.upper_half_chord = pg.add_line(
            circle_point,
            x_point,
            color=StyleConfig.LINE_COLOR,
            stroke_width=StyleConfig.CHORD_STROKE_WIDTH
        ).set_z_index(ZIndexEnum.LINES)

        # 하단 삼각형 그룹 생성 (y좌표 반전)
        lower_circle_point = [np.cos(angle), -np.sin(angle)]
        self.lower_triangle = pg.add_triangle(
            [0, 0],
            lower_circle_point,
            x_point,
        ).set_opacity(StyleConfig.SECONDARY_SHAPE_OPACITY)

        self.lower_dot = pg.add_point(
            lower_circle_point,
            color=StyleConfig.POINT_COLOR
        ).set_z_index(ZIndexEnum.POINTS)
        self.lower_half_chord = pg.add_line(
            lower_circle_point,
            x_point,
            color=StyleConfig.LINE_COLOR,
            stroke_width=StyleConfig.CHORD_STROKE_WIDTH
        ).set_opacity(StyleConfig.SECONDARY_SHAPE_OPACITY)

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

        self.right_dot = pg.add_point(
            circle_point,
            color=StyleConfig.POINT_COLOR,
            radius=StyleConfig.DOT_RADIUS
        ).set_z_index(ZIndexEnum.POINTS)
        self.right_half_chord = pg.add_line(
            circle_point,
            y_point,
            color=WHITE,
            stroke_width=4
        ).set_z_index(ZIndexEnum.LINES)

        # 좌측 삼각형 그룹 생성 (x좌표 반전)
        left_circle_point = [-np.cos(angle), np.sin(angle)]
        self.left_triangle = pg.add_triangle(
            [0, 0],
            left_circle_point,
            y_point,
        ).set_opacity(0.1)

        self.left_dot = pg.add_point(
            left_circle_point,
            color=StyleConfig.POINT_COLOR,
            radius=StyleConfig.DOT_RADIUS
        ).set_z_index(ZIndexEnum.POINTS)
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

    def calculate_tangent_line_points(self, angle: float) -> tuple[list[float], list[float], list[float]]:
        """주어진 각도에서의 접선 관련 정보를 계산합니다.

        Args:
            angle: 라디안 단위의 각도

        Returns:
            tuple[list[float], list[float], list[float]]: 
                - 단위원 위의 접점 좌표
                - 접선의 시작점 좌표
                - 접선의 끝점 좌표
        """
        # 단위원 위의 접점 계산
        point_on_circle = [np.cos(angle), np.sin(angle)]

        # 접선의 방향 벡터 계산 (-y, x)
        tangent_direction = [-np.sin(angle), np.cos(angle)]

        # 평면의 크기를 고려한 충분한 길이 계산 (대각선 길이 사용)
        plane_width = self.plane.get_width()
        plane_height = self.plane.get_height()
        line_length = np.sqrt(plane_width**2 + plane_height**2)

        # 접점에서 양방향으로 뻗어나가는 접선의 시작점과 끝점 계산
        start_point = [
            point_on_circle[0] - tangent_direction[0] * line_length,
            point_on_circle[1] - tangent_direction[1] * line_length
        ]
        end_point = [
            point_on_circle[0] + tangent_direction[0] * line_length,
            point_on_circle[1] + tangent_direction[1] * line_length
        ]

        return point_on_circle, start_point, end_point

    def add_shapes_for_tangent(self, initial_angle: float | None = None):
        """tan(x) 삼각함수 시각화를 위한 도형 생성"""
        pg = self.plane_group
        angle = initial_angle if initial_angle is not None else self.initial_angle

        # 기존 브레이스 제거 (혹시 남아있을 수 있으므로)
        if "tangent" in self.decorations:
            brace, label = self.decorations["tangent"]
            if brace is not None:
                self.remove(brace, label)
                self.plane_group.remove_brace("tangent_brace")
            self.decorations.pop("tangent")

        # 접선 관련 정보 계산
        point_on_circle, start_point, end_point = self.calculate_tangent_line_points(
            angle)

        # 1. 단위원 위의 접점 생성
        self.point_of_tangency = pg.add_point(
            point_on_circle,
            color=StyleConfig.POINT_COLOR,
            radius=StyleConfig.DOT_RADIUS
        ).set_z_index(ZIndexEnum.POINTS)

        # 2. x축 상의 점 (접점의 x축 정사영)
        x_projection = [np.cos(angle), 0]

        # 3. 접선의 기울기를 이용하여 x축과의 교점 계산
        # 접선의 기울기는 -x/y (단위원 위의 점에서의 법선 벡터가 (x,y)이므로)
        if np.abs(np.sin(angle)) > 1e-10:  # divide by zero 방지
            slope = -np.cos(angle) / np.sin(angle)
            x_intercept = [1/np.cos(angle), 0]  # x = sec(θ)
        else:
            # θ가 0° 또는 180°인 경우 수직선
            x_intercept = [1, 0] if np.cos(angle) > 0 else [-1, 0]

        self.x_axis_intercept = pg.add_point(
            x_intercept,
            color=GREEN
        ).set_z_index(ZIndexEnum.POINTS)

        # 4. 단위원의 반지름 생성
        self.circle_radius = pg.add_line(
            [0, 0],
            point_on_circle,
            color=StyleConfig.SHAPE_COLOR,
            stroke_width=StyleConfig.RADIUS_STROKE_WIDTH
        ).set_z_index(ZIndexEnum.LINES)

        # 5. 단위원의 'point_on_circle' 지점에서 접하는 접선 생성
        self.tangent_line = pg.add_line(
            start_point=start_point,
            end_point=end_point,
            color=StyleConfig.LINE_COLOR,
            stroke_width=StyleConfig.TANGENT_STROKE_WIDTH,
            stroke_opacity=StyleConfig.TANGENT_LINE_OPACITY
        ).set_z_index(ZIndexEnum.BASE_SHAPES)

        # 6. 빗변(hypotenuse) 생성
        self.hypotenuse = pg.add_line(
            point_on_circle,
            x_intercept,
            color=StyleConfig.LINE_COLOR,
            stroke_width=StyleConfig.HYPOTENUSE_STROKE_WIDTH
        ).set_z_index(ZIndexEnum.LINES)

        # 7. 단위원내 삼각형 생성
        self.inner_triangle = pg.add_triangle(
            [0, 0],
            point_on_circle,
            x_intercept
        ).set_stroke(
            color=StyleConfig.SHAPE_COLOR,
            width=StyleConfig.SHAPE_STROKE_WIDTH,
            opacity=StyleConfig.SECONDARY_SHAPE_OPACITY
        ).set_fill(
            StyleConfig.SHAPE_COLOR,
            opacity=StyleConfig.SHAPE_FILL_OPACITY
        ).set_z_index(ZIndexEnum.BASE_SHAPES)

        # 8. 직각 삼각형 생성
        self.tangent_triangle = pg.add_triangle(
            point_on_circle,  # 접점
            x_intercept,      # x축 절편점
            x_projection      # 접점의 x축 정사영
        ).set_stroke(color=StyleConfig.SHAPE_COLOR, width=StyleConfig.SHAPE_STROKE_WIDTH)\
            .set_fill(StyleConfig.SHAPE_COLOR, opacity=StyleConfig.TRIANGLE_FILL_OPACITY)\
            .set_z_index(ZIndexEnum.BASE_SHAPES)

        # 9. 모든 객체를 VGroup에 추가
        self.add(
            self.point_of_tangency,
            self.x_axis_intercept,
            self.circle_radius,
            self.tangent_line,
            self.hypotenuse,
            self.inner_triangle,
            self.tangent_triangle
        )

    def remove_shapes_for_tangent(self):
        """tan(x) 삼각함수 시각화 도형 제거"""
        # 도형들 제거
        removed_objects = [
            self.point_of_tangency,
            self.x_axis_intercept,
            self.circle_radius,
            self.tangent_line,
            self.hypotenuse,
            self.inner_triangle,
            self.tangent_triangle
        ]

        self.remove(*removed_objects)
        self.plane_group.remove(*removed_objects)

        # 멤버 변수들을 None으로 설정
        self.point_of_tangency = None
        self.x_axis_intercept = None
        self.circle_radius = None
        self.tangent_line = None
        self.hypotenuse = None
        self.inner_triangle = None
        self.tangent_triangle = None

        # 탄젠트 브레이스와 라벨 제거
        if "tangent" in self.decorations:
            brace, label = self.decorations["tangent"]
            if brace is not None:
                self.remove(brace, label)
                self.plane_group.remove_brace("tangent_brace")
            self.decorations.pop("tangent")

        return removed_objects
