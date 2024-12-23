from manim import *
from common.number_plane_group import *


class UnitCircleTriangle(VGroup):
    """단위원과 삼각함수 시각화를 위한 삼각형 그룹 클래스"""

    def __init__(self, planeGroup: NumberPlaneGroup, initial_angle=PI/3, **kwargs):
        super().__init__(**kwargs)
        self.plane = planeGroup.plane
        self.plane_group = planeGroup  # NumberPlaneGroup 인스턴스 저장

        # 단위원 생성
        self.unit_circle = planeGroup.add_circle(
            center_point=[0, 0], radius=1, color=PINK, stroke_width=3)

        # 상단 삼각형 그룹 생성
        self.upper_triangle = planeGroup.add_triangle(
            [0, 0],
            [np.cos(initial_angle), np.sin(initial_angle)],
            [np.cos(initial_angle), 0],
        )

        # BasicShapeMixin의 메서드를 사용하여 점과 선 생성
        circle_point = [np.cos(initial_angle), np.sin(initial_angle)]
        x_point = [np.cos(initial_angle), 0]

        self.upper_dot = planeGroup.add_point(circle_point, color=GREEN)
        self.upper_half_chord = planeGroup.add_line(
            circle_point,
            x_point,
            color=WHITE,
            stroke_width=4
        )

        # 하단 삼각형 그룹 생성 (y좌표 반전)
        lower_circle_point = [np.cos(initial_angle), -np.sin(initial_angle)]
        self.lower_triangle = planeGroup.add_triangle(
            [0, 0],
            lower_circle_point,
            x_point,
        ).set_opacity(0.1)

        self.lower_dot = planeGroup.add_point(lower_circle_point, color=GREEN)
        self.lower_half_chord = planeGroup.add_line(
            lower_circle_point,
            x_point,
            color=WHITE,
            stroke_width=4
        ).set_opacity(0.5)

        # 초기에는 브레이스를 생성하지 않음
        self.sine_brace = None
        self.sine_label = None

        # VGroup에 모든 객체 추가 (브레이스 제외)
        self.add(
            self.unit_circle,
            self.upper_triangle,
            self.lower_triangle,
            self.upper_half_chord,
            self.lower_half_chord,
            self.upper_dot,
            self.lower_dot
        )


class CircleRotation(Animation):
    """단위원 위의 점 회전 애니메이션"""

    def __init__(self, unit_circle_triangle, clockwise=False, rotation_count=1, show_brace=True, **kwargs):
        super().__init__(unit_circle_triangle, **kwargs)
        self.clockwise = clockwise
        self.unit_circle_triangle = unit_circle_triangle
        self.rotation_count = rotation_count  # 회전 횟수 추가
        self.show_brace = show_brace  # 브레이스 표시 여부

    def interpolate_mobject(self, alpha):
        # alpha(0~1)에 회전 횟수를 곱해서 총 회전 각도 계산
        angle = alpha * TAU * self.rotation_count
        if self.clockwise:
            angle = -angle

        x = np.cos(angle)
        y = np.sin(angle)

        # 평면 좌표로 변환
        plane = self.unit_circle_triangle.plane
        origin = plane.c2p(0, 0)
        circle_point = plane.c2p(x, y)
        x_point = plane.c2p(x, 0)

        # 삼각형 업데이트
        triangle_points = [origin, circle_point, x_point, origin]
        lower_points = [origin, plane.c2p(
            x, -y), x_point, origin]  # 하단 삼각형은 y 좌표만 반전

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
        if self.unit_circle_triangle.sine_brace is not None:
            self.unit_circle_triangle.remove(self.unit_circle_triangle.sine_brace)
            self.unit_circle_triangle.remove(self.unit_circle_triangle.sine_label)
            self.unit_circle_triangle.plane_group.remove_brace("sine_brace")
            self.unit_circle_triangle.sine_brace = None
            self.unit_circle_triangle.sine_label = None

        # 브레이스 표시 여부에 따라 처리
        if self.show_brace and height > min_height:
            # x 값에 따라 브레이스가 붙을 현의 방향 결정
            brace_direction = RIGHT  # 1, 4분면 (x >= 0)
            if x < 0:  # 2, 3분면
                brace_direction = LEFT
            
            # 높이가 충분하면 새로운 브레이스 생성
            brace, label = self.unit_circle_triangle.plane_group.add_brace(
                self.unit_circle_triangle.upper_half_chord,
                direction=brace_direction,
                name="sine_brace",
                text="\\sin(x)",
                color=YELLOW,
                text_color=YELLOW,
                buff=0.1
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
            self.unit_circle_triangle.sine_brace = brace
            self.unit_circle_triangle.sine_label = label

        # 점 업데이트
        self.unit_circle_triangle.upper_dot.move_to(circle_point)
        self.unit_circle_triangle.lower_dot.move_to(plane.c2p(x, -y))


class FindingSin(Scene):
    def construct(self):
        # 좌표계 생성
        npg = NumberPlaneGroup(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        ).scale(1.9)

        unit_circle_triangle = UnitCircleTriangle(npg)

        self.add(npg, unit_circle_triangle)

        self.play(
            CircleRotation(unit_circle_triangle),
            run_time=9
        )
        self.play(
            npg.animate.scale(0.5).to_edge(LEFT)
        )
        self.play(
            CircleRotation(unit_circle_triangle, show_brace=False),
            run_time=4.5
        )

        self.wait()
