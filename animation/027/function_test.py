from manim import *


class SurfaceExample(ThreeDScene):
    def construct(self):
        # 축과 격자를 포함한 3D 좌표계 생성
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],  # 눈금 간격을 0.5로 조정
            y_range=[-2, 2, 0.5],  # 눈금 간격을 0.5로 조정
            z_range=[0, 8, 2],
            x_length=4,  # x축 길이
            y_length=4,  # y축 길이
            z_length=4,  # z축 길이
        )

        # x-y 평면에 넘버플레인 추가
        number_plane = NumberPlane(
            x_range=[-2, 2, 0.5],  # axes와 동일한 눈금 간격
            y_range=[-2, 2, 0.5],  # axes와 동일한 눈금 간격
            x_length=4,  # axes와 동일한 길이
            y_length=4,  # axes와 동일한 길이
            background_line_style={
                "stroke_opacity": 0.8,
                "stroke_width": 1,
                "stroke_color": BLUE_D,
            },
            axis_config={"stroke_opacity": 0.8},
        )
        number_plane.set_opacity(0.9)  # 투명도 조정
        number_plane.shift(IN * 0)  # z=0 평면에 위치하도록

        # f(x,y) = x^2 + y^2 함수 정의
        def param_surface(u, v):
            x = u
            y = v
            z = x**2 + y**2
            return np.array([x, y, z])

        # 표면 생성
        surface = Surface(
            param_surface,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            should_make_jagged=False,
        )

        # 표면 스타일 설정
        surface.set_style(fill_opacity=0.7)
        surface.set_fill_by_value(axes=axes, colors=[(BLUE, -0.5), (RED, 3)], axis=2)

        # 씬에 요소들 추가
        self.set_camera_orientation(
            phi=35 * DEGREES, theta=60 * DEGREES, zoom=0.7  # 카메라를 좀 더 멀리 이동
        )
        self.add(number_plane, axes, surface)

        # 카메라 회전 애니메이션 추가
        self.begin_ambient_camera_rotation(rate=0.2)  # 초당 0.2라디안 속도로 회전
        self.wait(10)  # 10초 동안 회전
        self.stop_ambient_camera_rotation()
        self.wait(1)


class HimmelblauSurface(ThreeDScene):
    def construct(self):
        # 축과 격자를 포함한 3D 좌표계 생성
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[0, 200, 50],
            x_length=8,
            y_length=8,
            z_length=4,
        )

        # x-y 평면에 넘버플레인 추가
        number_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.8,
                "stroke_width": 1,
                "stroke_color": BLUE_D,
            },
            axis_config={"stroke_opacity": 0.8},
        )
        number_plane.set_opacity(0.5)
        number_plane.shift(IN * 0)

        # 힘스브로트 함수 정의
        def himmelblau(u, v):
            x = u
            y = v
            z = (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2
            return np.array([x, y, z])

        # 표면 생성
        surface = Surface(
            himmelblau,
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(30, 30),
            should_make_jagged=False,
        )

        # 표면 스타일 설정
        surface.set_style(fill_opacity=0.7)
        surface.set_fill_by_value(
            axes=axes,
            colors=[(BLUE, 0), (GREEN, 50), (YELLOW, 100), (RED, 150)],
            axis=2,
        )

        # 씬에 요소들 추가
        self.set_camera_orientation(phi=35 * DEGREES, theta=60 * DEGREES, zoom=0.6)
        self.add(number_plane, axes, surface)

        # 카메라 회전 애니메이션
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class RosenbrockSurface(ThreeDScene):
    def construct(self):
        # 축과 격자를 포함한 3D 좌표계 생성
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-1, 3, 0.5],
            z_range=[0, 250, 50],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        # x-y 평면에 넘버플레인 추가
        number_plane = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-1, 3, 0.5],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_opacity": 0.8,
                "stroke_width": 1,
                "stroke_color": BLUE_D,
            },
            axis_config={"stroke_opacity": 0.8},
        )
        number_plane.set_opacity(0.5)
        number_plane.shift(IN * 0)

        # Rosenbrock 함수 정의 (a=1, b=100)
        def rosenbrock(u, v):
            x = u
            y = v
            z = (1 - x) ** 2 + 100 * (y - x**2) ** 2
            return np.array([x, y, z])

        # 표면 생성
        surface = Surface(
            rosenbrock,
            u_range=[-2, 2],
            v_range=[-1, 3],
            resolution=(30, 30),
            should_make_jagged=False,
        )

        # 표면 스타일 설정
        surface.set_style(fill_opacity=0.7)
        surface.set_fill_by_value(
            axes=axes,
            colors=[(BLUE, 0), (GREEN_B, 10), (YELLOW, 50), (RED, 200)],
            axis=2,
        )

        # 씬에 요소들 추가
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES, zoom=0.6)
        self.add(number_plane, axes, surface)

        # 카메라 회전 애니메이션
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class BowlSurface(ThreeDScene):
    def construct(self):
        # 축과 격자를 포함한 3D 좌표계 생성
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        # x-y 평면에 넘버플레인 추가
        number_plane = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_opacity": 0.8,
                "stroke_width": 1,
                "stroke_color": BLUE_D,
            },
            axis_config={"stroke_opacity": 0.8},
        )
        number_plane.set_opacity(0.5)
        number_plane.shift(IN * 0)

        # 수정된 Bowl 형태의 함수 정의 - 더 극적인 굴곡과 바깥쪽으로 휘어지는 형태
        def bowl_function(u, v):
            x = u
            y = v
            r = np.sqrt(x**2 + y**2)
            # 기본 bowl 형태 (바깥쪽으로 휘어지도록 수정)
            base = 0.3 * (x**2 + y**2) * (1 + 0.2 * r)
            # 더 극적인 굴곡 패턴 생성
            waves = (
                0.4 * np.sin(3.5 * x) * np.sin(2.5 * y)  # 더 큰 비대칭 굴곡
                + 0.35 * np.sin(4 * x) * np.cos(3.5 * y)  # 더 강한 교차 패턴
                + 0.3 * np.sin(6 * x - 3 * y)  # 더 깊은 대각선 굴곡
                + 0.25 * np.cos(5 * x + 4 * y)  # 추가 대각선 패턴
                + 0.2 * np.sin(8 * x) * np.sin(8 * y)  # 더 촘촘한 굴곡
                + 0.15 * np.sin(10 * r)  # 원형 물결 패턴
            )
            # 높이에 따른 굴곡 강도 조절 + 바깥쪽 휘어짐 강화
            z = base + waves * (1.2 - 0.1 * base) + 0.1 * r**2
            return np.array([x, y, z])

        # 표면 생성
        surface = Surface(
            bowl_function,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(60, 60),  # 해상도 더 증가
            should_make_jagged=False,
        )

        # 표면 스타일 설정
        surface.set_style(fill_opacity=0.7)
        surface.set_fill_by_value(
            axes=axes, colors=[(BLUE, 0), (GREEN_B, 1), (YELLOW, 2), (RED, 4)], axis=2
        )

        # 씬에 요소들 추가
        self.set_camera_orientation(phi=50 * DEGREES, theta=30 * DEGREES, zoom=0.7)
        self.add(number_plane, axes, surface)

        # 카메라 회전 애니메이션
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class SmoothBowlSurface(ThreeDScene):
    def construct(self):
        # 축과 격자를 포함한 3D 좌표계 생성
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[0, 4, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        # x-y 평면에 넘버플레인 추가
        number_plane = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_opacity": 0.8,
                "stroke_width": 1,
                "stroke_color": BLUE_D,
            },
            axis_config={"stroke_opacity": 0.8},
        )
        number_plane.set_opacity(0.5)
        number_plane.shift(IN * 0)

        # 부드러운 Bowl 형태의 함수 정의
        def smooth_bowl(u, v):
            x = u
            y = v
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            
            # 기본 bowl 형태 (더 가파르게)
            base = 0.6 * (x**2 + y**2) * (1 + 0.15*r)
            
            # 더 복잡한 굴곡 패턴
            waves = (
                0.35 * np.sin(3.2 * x) * np.sin(2.8 * y) +        # 비대칭 큰 굴곡
                0.3 * np.cos(2.5 * x - 2.2 * y) +                 # 대각선 굴곡
                0.25 * np.sin(4 * r) * np.exp(-0.2 * r) +         # 원형 물결
                0.2 * np.sin(5 * x + 3 * y) * np.cos(2 * x - y) + # 격자 패턴
                0.15 * np.sin(6 * theta) * np.exp(-0.1 * r) +     # 방사형 패턴
                0.1 * np.sin(8 * x) * np.sin(8 * y)               # 미세 굴곡
            )
            
            # 굴곡의 강도를 위치에 따라 조절
            modulation = (1.2 - 0.1 * base) * (1 + 0.2 * np.sin(2.5 * r))
            z = base + waves * modulation
            return np.array([x, y, z])

        # 표면 생성
        surface = Surface(
            smooth_bowl,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(70, 70),  # 더 높은 해상도
            should_make_jagged=False,
        )

        # 색상 범위 조정
        surface.set_style(fill_opacity=0.7)
        surface.set_fill_by_value(
            axes=axes,
            colors=[
                (BLUE, 0),
                (GREEN_B, 0.6),
                (YELLOW, 1.4),
                (RED, 2.5)
            ],
            axis=2
        )

        # 씬에 요소들 추가 (약간 위에서 보는 각도)
        self.set_camera_orientation(phi=40 * DEGREES, theta=45 * DEGREES, zoom=0.7)
        self.add(number_plane, axes, surface)

        # 카메라 회전 애니메이션
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.wait(1)
