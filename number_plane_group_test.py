from manim import *
from common.number_plane_group import NumberPlaneGroup, OriginStyle


class NumberPlaneTransformExample(Scene):
    def construct(self):
        # 더 넓은 범위의 NumberPlane 생성 ([-40, 40] 범위로 확장)
        plane = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,           # 화면에서의 x축 길이
            y_length=16,           # 화면에서의 y축 길이
            background_line_style={
                "stroke_opacity": 0.6
            }
        )

        plane.scale(2)
        self.play(Create(plane))

        self.play(plane.animate.shift(UP * 2))
        self.play(plane.animate.shift(DOWN * 3 + RIGHT * 2))
        self.play(plane.animate.scale(2.5, about_point=ORIGIN))
        self.play(plane.animate.scale(0.5, about_point=DOWN * 3 + RIGHT * 2))

        self.wait(2)


class NumberPlaneWithOriginExample(Scene):
    def construct(self):
        # NumberPlane 생성
        plane = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            x_length=16,
            y_length=16,
            background_line_style={
                "stroke_opacity": 0.6
            }
        )

        # 원점 표시 (여러 ��지 방법)
        origin_dot = Dot(ORIGIN, color=RED)  # 점으로 표시
        origin_circle = Circle(radius=0.1, color=BLUE,
                               fill_opacity=0.5)  # 작은 원으로 표시

        # 십자 표시 생성
        cross = VGroup(
            Line(UP * 0.2, DOWN * 0.2, color=YELLOW),
            Line(LEFT * 0.2, RIGHT * 0.2, color=YELLOW)
        )

        # 모든 요소를 하나의 그룹으로 만들기
        plane_group = VGroup(
            plane,
            origin_dot,
            origin_circle,
            cross
        )

        # 초기 스케일 설정
        plane_group.scale(0.5)

        # 애니메이션 시작
        self.play(Create(plane_group))
        self.wait()

        # 이동 테스트
        self.play(plane_group.animate.shift(RIGHT * 2 + UP))
        self.wait()

        # 확대 테스트
        self.play(plane_group.animate.scale(2, about_point=ORIGIN))
        self.wait()

        # 회전 테스트 (원점 표시가 잘 따라오는지 확인)
        self.play(plane_group.animate.rotate(PI/4))
        self.wait()

        # 복합 변환
        self.play(
            plane_group.animate
            .scale(0.5)
            .shift(LEFT * 3 + DOWN * 2)
        )
        self.wait(2)


class NumberPlaneGroupExample(Scene):
    def construct(self):
        # 기본 DOT 스타일로 생성
        plane_group = NumberPlaneGroup(
            origin_style_type=OriginStyle.DOT,
            origin_config={
                "color": RED,
                "size": 0.15,
                "opacity": 1.0
            }
        )
        plane_group.scale(1.2)
        self.play(Create(plane_group))
        self.wait()

        # CROSS 스타일로 변경
        self.play(plane_group.animate.shift(RIGHT * 2))
        plane_group.set_origin_style(
            OriginStyle.CROSS,
            {"color": YELLOW, "size": 0.2}
        )
        self.wait()

        # CIRCLE 스타일로 변경
        self.play(plane_group.animate.scale(1.5, about_point=ORIGIN))
        plane_group.set_origin_style(
            OriginStyle.CIRCLE,
            {"color": BLUE, "size": 0.12}
        )
        self.wait()

        # 원점 표시 숨기기/보이기
        self.play(plane_group.animate.rotate(PI/6))
        plane_group.hide_origin()
        self.wait()
        plane_group.show_origin()
        self.wait()

        # 복합 변환
        self.play(
            plane_group.animate
            .scale(0.8)
            .shift(LEFT * 2 + UP * 1.5)
        )
        self.wait(2)


class NumberPlaneGroupFunctionExample(Scene):
    def construct(self):
        # 좌표평면 생성 (보기 좋은 범위로 설정)
        plane_group = NumberPlaneGroup(
            background_line_style={
                "stroke_opacity": 0.6
            },
            origin_style_type=OriginStyle.CROSS,  # 원점은 십자로 표시
            origin_config={
                "color": YELLOW,
                "size": 0.15
            }
        )
        plane_group.scale(1.2)

        # 다양한 함수들 정의
        def parabola(x): return 0.5 * x**2  # y = 0.5x²
        def sine(x): return np.sin(x)        # y = sin(x)
        def cubic(x): return 0.1 * x**3      # y = 0.1x³

        # 좌표평면 생성
        self.play(Create(plane_group))
        self.wait()

        # 포물선 그래프 추가 (파란색)
        parabola_graph = plane_group.plot_function(
            parabola,
            name="parabola",
            color=BLUE
        )
        self.play(Create(parabola_graph))
        self.wait()

        # 사인 함수 그래프 추가 (초록색)
        sine_graph = plane_group.plot_function(
            sine,
            name="sine",
            color=GREEN
        )
        self.play(Create(sine_graph))
        self.wait()

        # 전체 평면 이동
        self.play(
            plane_group.animate.shift(RIGHT * 1.5 + UP)
        )
        self.wait()

        # 3차 함수 그래프 추가 (빨간색)
        cubic_graph = plane_group.plot_function(
            cubic,
            name="cubic",
            color=RED
        )
        self.play(Create(cubic_graph))
        self.wait()

        # 확대
        self.play(
            plane_group.animate.scale(1.5, about_point=ORIGIN)
        )
        self.wait()

        # 포물선 그래프 제거
        self.play(FadeOut(plane_group.get_function_graph("parabola")))
        plane_group.remove_function("parabola")
        self.wait()

        # 회전 애니메이션
        self.play(
            plane_group.animate.rotate(PI/6)  # 30도 회전
        )
        self.wait(2)


class NumberPlaneGroupFunctionExample1(ThreeDScene):  # Scene -> ThreeDScene
    def construct(self):
        # 좌표평면 생성 (더 넓은 범위로 설정)
        plane_group = NumberPlaneGroup(
            background_line_style={
                "stroke_opacity": 0.3
            },
            origin_style_type=OriginStyle.DOT,
            origin_config={
                "size": 0.05
            }
        )

        # 초기 크기와 위치 조정
        plane_group.scale(1.2)

        # 함수들 정의 (일반 함수와 파라메트릭 함수 분리)
        def parabola(x): return 0.25 * x**2    # 원래대로 x축 방향
        def sine(x): return 1.5 * np.sin(x)    # 원래대로 x축 방향

        def cosine_vertical(t): return np.array(
            [-2 * np.cos(t), t, 0])  # y축 방향 코사인

        # 좌표평면 생성
        self.play(Create(plane_group))
        self.wait()

        # 포물선 그래프 추가 (일반 함수)
        parabola_graph = plane_group.plot_function(
            parabola,
            name="parabola",
            color=BLUE
        )
        self.play(Create(parabola_graph))
        self.wait()

        # 전체 평면 이동 (이동 거리 감소)
        self.play(
            plane_group.animate.shift(RIGHT * 1 + UP * 0.5)  # 이동 거리 감소
        )
        self.wait()

        # 확대 (비율 감소)
        self.play(
            plane_group.animate.scale(1.3, about_point=ORIGIN)  # 확대 비율 감소
        )
        self.wait()

        # 회전 애니메이션 (ORIGIN 기준으로 회전)
        self.play(
            plane_group.animate.rotate(PI/6, about_point=ORIGIN)
        )
        self.wait()

        # 사인 함수 그래프 추가 (일반 함수)
        sine_graph = plane_group.plot_function(
            sine,
            name="sine",
            color=GREEN
        )
        self.play(Create(sine_graph))
        self.wait()

        # 코사인 함수만 y축 방향으로 그리기 (파라메트릭)
        cosine_graph = plane_group.plot_parametric(
            cosine_vertical,
            t_range=[-20, 20],  # y축 범위 확장
            name="cosine",
            color=RED
        )
        self.play(Create(cosine_graph))
        self.wait()

        # 포물선 그래프 제거
        self.play(FadeOut(plane_group.get_function_graph("parabola")))
        plane_group.remove_function("parabola")
        self.wait()

        # 반지름이 2인 원 그리기 (파라메트릭 방정식: x = 2cos(t), y = 2sin(t))
        def circle_func(t):
            return np.array([2 * np.cos(t), 2 * np.sin(t), 0])

        circle_graph = plane_group.plot_parametric(
            circle_func,
            name="circle",
            color=YELLOW,
            stroke_width=3
        )
        self.play(Create(circle_graph))
        self.wait()

        # 원 그리기 후 카메라 초기 위치 설정
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        self.wait()

        # 원의 현재 변환 상태를 반영한 헬릭스 생성
        circle_center = circle_graph.get_center()

        # 원이 그려진 실제 좌표를 이용하여 크기와 회전 계산
        circle_start = circle_graph.point_from_proportion(0)  # t=0일 때의 점
        circle_quarter = circle_graph.point_from_proportion(
            0.25)  # t=π/2일 때의 점

        # 반지름 계산 (원의 크기)
        radius = np.linalg.norm(circle_start - circle_center)

        # 회전각 계산 (x축과 이루는 각도)
        rotation = np.arctan2(
            circle_start[1] - circle_center[1],
            circle_start[0] - circle_center[0]
        )

        def helix_func(t):
            # 기본 헬릭스 좌표 (z축 높이는 유지하면서 회전수 증가)
            base_x = radius * np.cos(t)
            base_y = radius * np.sin(t)
            base_z = 0.8 * t / (2*PI)  # 높이는 그대로 유지

            # 회전 적용
            rotated_x = base_x * np.cos(rotation) - base_y * np.sin(rotation)
            rotated_y = base_x * np.sin(rotation) + base_y * np.cos(rotation)

            # 이동 적용
            final_point = np.array([
                rotated_x + circle_center[0],
                rotated_y + circle_center[1],
                base_z
            ])

            return final_point

        # 헬릭스를 여러 단계로 나누어 생성 (회전수 감소)
        helix_pieces = []
        num_pieces = 8  # 조각 수 조정
        total_rotations = 8 * PI  # 4번 회전으로 감소

        for i in range(num_pieces):
            t_range = [i * total_rotations/num_pieces,
                       (i + 1) * total_rotations/num_pieces]
            piece = ParametricFunction(
                helix_func,
                t_range=t_range,
                color=PINK,
                stroke_width=4
            )
            helix_pieces.append(piece)

        # 카메라 움직임을 더 부드럽게 조정
        # 1. 현재 위치에서 시작하여 조금씩 움직임
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        self.wait()

        # 2. 먼저 살짝 위로 올라가기
        self.move_camera(
            phi=30 * DEGREES,
            theta=-90 * DEGREES,
            run_time=2
        )
        self.wait(0.5)

        # 3. 천천히 회전하면서 더 올라가기
        self.move_camera(
            phi=45 * DEGREES,
            theta=-45 * DEGREES,
            run_time=3
        )
        self.wait(0.5)

        # 4. 최종 위치로 부��럽게 이동
        self.move_camera(
            phi=60 * DEGREES,
            theta=30 * DEGREES,   # 큐빅 함수가 잘 보이는 각도
            run_time=2
        )

        # 5. 각 조각을 순차적으로 생성
        for piece in helix_pieces:
            self.play(Create(piece), run_time=0.4)
        self.wait()

        # 6. 부드러운 카메라 회전 (더 천천히)
        self.begin_ambient_camera_rotation(rate=0.05)  # 회전 속도 감소
        self.wait(10)  # 회전 시간 증가

        # 7. 마지막 뷰로 이동
        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=50 * DEGREES,    # 각도 조정
            theta=45 * DEGREES,  # 큐빅 함수가 잘 보이는 각도
            run_time=3
        )
        self.wait(2)
