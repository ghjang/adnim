import numpy as np
from scipy import optimize
from manim import *


# 3D 원형 링을 생성하는 헬퍼 함수 추가
def create_circle_3d(radius, color, normal=None, stroke_width=2, num_components=24):
    """
    3D 공간에서 원형 링을 생성합니다.
    normal: 원이 향하는 방향 벡터 (기본값: z축 방향)
    """
    if normal is None:
        normal = [0, 0, 1]  # 기본 z축 방향

    # 원래 방향(z축)에서 회전할 각도 계산
    normal = np.array(normal) / np.linalg.norm(normal)  # 정규화

    # 원형 경로 생성
    circle = Circle(radius=radius, color=color, stroke_width=stroke_width)
    circle.set_shade_in_3d(True)

    # 지정된 법선 벡터 방향으로 회전
    if not np.allclose(normal, np.array([0, 0, 1])):
        axis = np.cross([0, 0, 1], normal)
        if np.linalg.norm(axis) > 1e-6:  # 회전축이 0이 아닌 경우만
            angle = np.arccos(np.dot([0, 0, 1], normal))
            circle.rotate(angle, axis)

    return circle


# 설정 클래스 정의
class Config:
    def __init__(self, mode="dev", auto_adjust_z=False):
        # 공통 설정
        self.x_range = [-3, 3, 1]
        self.y_range = [-3, 3, 1]
        self.x_length = 6
        self.y_length = 6
        self.z_offset = 2.0  # z축 오프셋 (최솟값을 양수로 만들기 위한 상수)
        self.z_min_margin = 0.5  # 최솟값과 z=0 사이의 최소 간격
        self.auto_adjust_z = auto_adjust_z  # z_offset 자동 계산 여부
        self.dot_height_offset = 0.2  # 법선 벡터 방향으로의 오프셋 크기 증가
        self.surface_opacity = 0.7  # 표면 투명도 증가

        # 색상 설정 (공통)
        self.start_color = GREEN_A  # 시작점 기본 색상
        self.end_color = YELLOW_A  # 끝점 기본 색상
        self.start_highlight_color = GREEN  # 강조 색상 (밝음)
        self.end_highlight_color = YELLOW  # 강조 색상 (밝음)
        self.path_color = RED  # 경로 선 색상

        # 애니메이션 효과 관련 설정 추가
        self.dot_animation_time = 0.3  # 점 생성 애니메이션 시간
        self.line_animation_time = 1.5  # 선 생성 애니메이션 시간
        self.path_tracer_radius = 0.04  # 경로 추적자 크기
        self.path_tracer_color = ORANGE  # 경로 추적자 색상
        self.path_tracer_speed = 5  # 경로 추적자 속도 배율
        self.use_path_tracer = True  # 경로 추적자 사용 여부

        # 등고선 관련 설정 추가
        self.show_contours = False  # 등고선 표시 여부 (기본: 끄기)
        self.contour_opacity = 0.3  # 등고선 투명도
        self.contour_stroke_width = 1.0  # 등고선 두께

        # 축과 그리드에 관한 설정 추가
        self.axes_opacity = 0.4  # 좌표축 투명도
        self.axes_stroke_width = 1.0  # 좌표축 두께

        # 그리드 설정 개선
        self.grid_opacity = 0.7  # 그리드 전체 투명도 증가
        self.grid_stroke_width = 1.0  # 그리드 선 두께 증가
        self.grid_stroke_opacity = 0.6  # 그리드 선 투명도 감소 (더 선명하게)
        self.grid_color = BLUE_B  # 더 밝은 파란색으로 변경
        self.grid_z_offset = 0.01  # 그리드를 z=0 평면보다 살짝 위에 배치

        # 함수 수식 표시 관련 설정 추가
        self.show_formula = True  # 함수 수식 표시 여부
        self.formula_color = YELLOW  # 수식 색상
        self.formula_scale = 0.7  # 수식 크기 (스케일 팩터)
        self.formula_margin = 0.2  # 수식과 NumberPlane 사이 여백

        # 좌표축 위치 조정을 위한 설정 추가
        self.axes_shift = [0, -0.8, 0]  # x, y, z 방향 이동 (y축 방향으로 뒤로 이동)

        # 정보 레이블 관련 설정 추가
        self.show_info_labels = True  # 정보 레이블 표시 여부
        self.label_font_size = 24  # 레이블 폰트 크기
        self.label_color = WHITE  # 레이블 색상
        self.label_buff = 0.4  # 레이블 간격
        self.label_z_index = 200  # 레이블 z-index (모든 것보다 앞에 보이게)
        # 위치 수정: y 값을 작게(0으로) 조정하여 넘버플레인 상단에 맞춤
        self.label_position_offset = [-4, 0, 0.01]  # 레이블 위치 조정

        # 모드별 설정
        if mode == "dev":
            # 개발용 설정 - 빠른 렌더링 우선
            self.surface_resolution = (25, 25)  # 낮은 해상도
            self.contour_levels_count = 3  # 적은 등고선
            self.gd_init_point = (1.5, 1.5)  # 시작점
            # self.gd_learning_rate = 0.1  # 학습률
            # self.gd_learning_rate = 0.075  # 학습률, 굿
            # self.gd_learning_rate = 0.07  # 학습률, 모어 굿
            self.gd_learning_rate = 0.065  # 학습률
            # self.gd_learning_rate = 0.05  # 학습률
            self.gd_steps = 13  # 적은 단계 수
            self.path_animation_time = 0.1  # 빠른 애니메이션
            self.dot_radius = 0.08  # 점 크기
            self.dot_opacity = 1.0  # 점의 투명도 설정 (완전 불투명)
            self.line_thickness = 0.02  # 얇은 선
            self.camera_rotation_rate = 0.1  # 카메라 회전 속도
            self.auto_adjust_z = True
            self.use_path_tracer = True  # 개발 모드에서 경로 추적자 사용
        else:  # "prod" (프로덕션)
            # 프로덕션용 설정 - 고품질 우선
            # self.surface_resolution = (50, 50)  # 높은 해상도
            self.surface_resolution = (50, 50)  # 높은 해상도
            self.contour_levels_count = 8  # 많은 등고선
            self.gd_init_point = (1.5, 1.5)  # 시작점
            # self.gd_learning_rate = 0.1  # 미세 조정된 학습률
            self.gd_learning_rate = 0.065
            # self.gd_steps = 25  # 많은 단계 수
            self.gd_steps = 11
            self.path_animation_time = 0.2  # 적절한 속도
            # self.dot_radius = 0.12  # 점 크기
            self.dot_radius = 0.08  # 점 크기
            self.dot_opacity = 1.0  # 점의 투명도 설정 (완전 불투명)
            self.line_thickness = 0.03  # 굵은 선
            self.camera_rotation_rate = 0.08  # 부드러운 카메라 회전
            self.auto_adjust_z = True
            self.use_path_tracer = True  # 프로덕션 모드에서도 사용


# 2변수 함수 정의
def f(x, y, z_offset=2.0):
    r2 = x**2 + y**2
    # z_offset을 더해 최솟값을 양수로 조정
    return r2**2 - 4 * r2 + 2 * x + 3 * y + 2 + z_offset


# 최솟값을 계산하기 위한 함수 (scipy.optimize용)
def f_for_minimize(xy):
    return f(xy[0], xy[1], 0)  # 오프셋 없이 원래 함수의 최솟값을 계산


# 수치 미분을 이용한 그래디언트 계산
def numerical_gradient(f, xy, h=1e-4, z_offset=2.0):
    x, y = xy
    df_dx = (f(x + h, y, z_offset) - f(x - h, y, z_offset)) / (2 * h)
    df_dy = (f(x, y + h, z_offset) - f(x, y - h, z_offset)) / (2 * h)
    return np.array([df_dx, df_dy])


# 경사 하강법 구현
def gradient_descent(f, init_xy, lr=0.2, steps=10, z_offset=2.0):
    xy = np.array(init_xy, dtype=float)
    path = [xy.copy()]
    for _ in range(steps):
        grad = numerical_gradient(f, xy, z_offset=z_offset)
        xy -= lr * grad  # 학습률 반영
        path.append(xy.copy())
    return np.array(path)


# 자동으로 함수의 최솟값을 찾고 적절한 z_offset 계산
def calculate_z_offset(min_margin=0.5):
    # scipy.optimize를 사용한 정확한 최솟값 계산
    result = optimize.minimize(f_for_minimize, [0, 0], method="BFGS")
    min_value = result.fun

    # 최솟값이 min_margin보다 크게 되는 오프셋 계산
    if min_value < min_margin:
        return min_margin - min_value
    return 0  # 이미 최솟값이 충분히 큰 경우


# 함수의 법선 벡터 계산 함수 - 항상 위를 향하게 수정
def calculate_normal_vector(x, y, z_offset=2.0, h=1e-4):
    """
    주어진 점 (x,y)에서 함수 표면의 법선 벡터를 계산합니다.
    항상 곡면 위쪽을 향하는 법선 벡터를 반환합니다.
    """
    # x, y 방향의 편미분 계산 (그래디언트)
    df_dx = (f(x + h, y, z_offset) - f(x - h, y, z_offset)) / (2 * h)
    df_dy = (f(x, y + h, z_offset) - f(x, y - h, z_offset)) / (2 * h)

    # 법선 벡터: (-df/dx, -df/dy, 1)
    # 이 벡터는 항상 z 성분이 양수입니다 (위를 향함)
    normal = np.array([-df_dx, -df_dy, 1.0])

    # 법선 벡터 정규화 (길이 1로)
    normal_length = np.sqrt(np.sum(normal**2))
    normal = normal / normal_length

    return normal


# 법선 벡터 방향으로 오프셋된 점 계산 함수 - 단순화된 버전
def point_with_normal_offset(axes, x, y, z, normal, offset):
    """
    법선 벡터 방향으로 오프셋된 3D 좌표를 계산합니다.
    단순화된 방식으로 계산하여 확실히 표면 위에 배치합니다.
    """
    # 원본 점의 3D 좌표
    original_point = np.array(axes.c2p(x, y, z))

    # 월드 좌표에서의 법선 벡터 방향으로 오프셋
    # 법선 벡터가 이미 정규화되어 있으므로, 직접 곱함
    offset_vector = normal * offset

    # 오프셋을 적용한 점
    return original_point + offset_vector


# Manim Scene
class GradientDescent3D(ThreeDScene):
    def __init__(self, config=None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or Config("dev")  # 기본값은 개발 모드
        # self.config = config or Config("prod")

        # 자동으로 z_offset 계산
        if hasattr(self.config, "auto_adjust_z") and self.config.auto_adjust_z:
            self.config.z_offset = calculate_z_offset(self.config.z_min_margin)
            print(f"자동 계산된 z_offset: {self.config.z_offset}")

    # 경로에 있는 모든 점과 법선 벡터를 계산하는 함수
    def calculate_path_points_and_normals(self, axes, path_points):
        normals = []
        dot_positions = []
        surface_points = []

        for point in path_points:
            x, y = point
            z_val = f(x, y, self.config.z_offset)
            surface_point = axes.c2p(x, y, z_val)
            surface_points.append(surface_point)

            # 법선 벡터 계산
            normal = calculate_normal_vector(x, y, self.config.z_offset)
            normals.append(normal)

            # 법선 방향으로 오프셋된 점 위치 계산
            offset_point = (
                np.array(surface_point) + normal * self.config.dot_height_offset
            )
            dot_positions.append(offset_point)

        return normals, dot_positions, surface_points

    def create_info_labels(self, axes):
        """정보 레이블 생성 (이터레이션, 학습률, 현재 위치, 그래디언트)"""
        # 시작 위치 계산 (x-y 평면의 좌측 상단에 맞춤)
        base_point = axes.c2p(self.config.x_range[0], self.config.y_range[1], 0)
        base_point = np.array(base_point) + np.array(self.config.label_position_offset)

        # 이터레이션 레이블
        iter_label = Text(
            "Iteration: 0",
            font_size=self.config.label_font_size,
            color=self.config.label_color,
        ).move_to(base_point)
        iter_label.set_z_index(self.config.label_z_index)

        # 학습률 레이블
        lr_label = Text(
            f"Learning Rate: {self.config.gd_learning_rate:.4f}",
            font_size=self.config.label_font_size,
            color=self.config.label_color,
        ).next_to(iter_label, DOWN, buff=self.config.label_buff)
        lr_label.align_to(iter_label, LEFT)
        lr_label.set_z_index(self.config.label_z_index)

        # 현재 위치 레이블 (2D 좌표)
        pos_label = Text(
            f"Position: ({self.config.gd_init_point[0]:.4f}, {self.config.gd_init_point[1]:.4f})",
            font_size=self.config.label_font_size,
            color=self.config.label_color,
        ).next_to(lr_label, DOWN, buff=self.config.label_buff)
        pos_label.align_to(lr_label, LEFT)
        pos_label.set_z_index(self.config.label_z_index)

        # 그래디언트 레이블 (2D 벡터)
        grad_label = Text(
            "Gradient: (0.0000, 0.0000)",
            font_size=self.config.label_font_size,
            color=self.config.label_color,
        ).next_to(pos_label, DOWN, buff=self.config.label_buff)
        grad_label.align_to(pos_label, LEFT)
        grad_label.set_z_index(self.config.label_z_index)

        # 모든 레이블이 3D 공간에서도 잘 보이도록 설정
        for label in [iter_label, lr_label, pos_label, grad_label]:
            label.set_shade_in_3d(True)

        return iter_label, lr_label, pos_label, grad_label

    def create_path_tracer(self, dot_positions):
        """
        경로를 따라 움직이는 추적자 생성
        """
        tracer = Dot3D(
            dot_positions[0],
            color=self.config.path_tracer_color,
            radius=self.config.path_tracer_radius,
        )
        tracer.set_z_index(120)  # 가장 높은 우선순위
        return tracer

    def animate_path_tracer(self, tracer, dot_positions):
        """
        추적자가 경로를 따라 움직이는 애니메이션 생성
        """
        animations = []
        total_time = 0

        # 각 선분마다 별도 애니메이션 생성
        for i in range(1, len(dot_positions)):
            # 선분의 길이에 비례하는 시간 계산
            distance = np.linalg.norm(dot_positions[i] - dot_positions[i - 1])
            segment_time = distance * 0.5 / self.config.path_tracer_speed

            # 최소 시간 보장
            segment_time = max(segment_time, 0.1)
            total_time += segment_time

            # 추적자가 현재 위치에서 다음 위치로 이동
            animations.append(
                tracer.animate(run_time=segment_time).move_to(dot_positions[i])
            )

        return animations, total_time

    def construct(self):
        # 함수의 범위를 미리 계산하여 적절한 z축 범위 설정
        x_vals = np.linspace(-2, 2, 20)
        y_vals = np.linspace(-2, 2, 20)

        # 벡터화된 함수 값 계산
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.zeros_like(X)
        for i in range(len(x_vals)):
            for j in range(len(y_vals)):
                Z[j, i] = f(X[j, i], Y[j, i], self.config.z_offset)

        min_z = np.min(Z)
        max_z = np.max(Z)
        z_margin = (max_z - min_z) * 0.1  # 여백 10%

        print(f"함수의 최솟값: {min_z}, z_offset: {self.config.z_offset}")

        # 3D 좌표축 생성 (z축 범위 최적화 및 흐릿하게 설정)
        z_min = max(0, min_z - z_margin)
        axes = ThreeDAxes(
            x_range=self.config.x_range,
            y_range=self.config.y_range,
            z_range=[z_min, max_z + z_margin, 2],
            x_length=self.config.x_length,
            y_length=self.config.y_length,
            z_length=5,
            axis_config={
                "stroke_opacity": self.config.axes_opacity,  # 축 투명도 설정
                "stroke_width": self.config.axes_stroke_width,  # 축 두께 설정
                "include_ticks": True,  # 눈금 포함
                "include_tip": True,  # 화살표 팁 포함
            },
        )

        # 좌표축 전체를 이동하여 z축이 더 잘 보이도록 조정
        if hasattr(self.config, "axes_shift"):
            axes.shift(self.config.axes_shift)
            print(f"좌표축을 {self.config.axes_shift} 만큼 이동했습니다.")

        # 정보 레이블 생성
        info_labels = None
        if hasattr(self.config, "show_info_labels") and self.config.show_info_labels:
            info_labels = self.create_info_labels(axes)
            iter_label, lr_label, pos_label, grad_label = info_labels

        # 축에 라벨 추가 - 투명도 조정
        x_label = MathTex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), UP)
        z_label = MathTex("z").next_to(axes.z_axis.get_end(), OUT)
        labels = VGroup(x_label, y_label, z_label)
        labels.set_opacity(
            self.config.axes_opacity * 1.2
        )  # 라벨은 축보다 약간 더 진하게

        # x-y 평면에 그리드 (넘버플레인) 추가 - 좌표축 제외, 그리드만 표시
        grid = NumberPlane(
            x_range=self.config.x_range,
            y_range=self.config.y_range,
            x_length=self.config.x_length,
            y_length=self.config.y_length,
            axis_config={
                "stroke_opacity": 0,  # 축 숨기기
            },
            background_line_style={
                "stroke_opacity": self.config.grid_stroke_opacity,
                "stroke_width": self.config.grid_stroke_width,
                "stroke_color": self.config.grid_color,  # 더 밝은 색상으로 변경
            },
            faded_line_style={
                "stroke_opacity": self.config.grid_stroke_opacity
                * 0.7,  # 덜 흐리게 설정
                "stroke_width": self.config.grid_stroke_width * 0.7,
                "stroke_color": self.config.grid_color,
            },
        )
        grid.set_opacity(self.config.grid_opacity)

        # 그리드를 xy 평면에 위치시키고 살짝 위로 올림
        grid_pos = axes.c2p(0, 0, self.config.grid_z_offset)
        grid.move_to(grid_pos)

        # 그리드를 표면과 배경 사이에 배치 (z-index 조정)
        grid.set_z_index(1)  # 양수 값으로 변경하여 적어도 배경보다는 앞에 표시

        # 함수 수식 생성 및 배치
        if hasattr(self.config, "show_formula") and self.config.show_formula:
            # LaTeX으로 함수 수식 작성 (z_offset 값도 포함)
            formula_text = r"f(x,y) = (x^2+y^2)^2 - 4(x^2+y^2) + 2x + 3y + 2"
            if self.config.z_offset > 0:
                formula_text += f" + {self.config.z_offset:.1f}"

            formula = MathTex(formula_text, color=self.config.formula_color)
            formula.scale(self.config.formula_scale)

            # 넘버플레인의 y축 최소값 아래에 배치
            y_min_pos = axes.c2p(0, self.config.y_range[0], 0)
            formula_y_pos = (
                y_min_pos[1] - formula.height / 2 - self.config.formula_margin
            )

            # x축 중앙에 배치 (x축에 평행하게)
            formula.move_to([0, formula_y_pos, self.config.grid_z_offset])

            # 3D 공간에서도 잘 보이도록 설정
            formula.set_z_index(5)
            formula.set_shade_in_3d(True)

        # 등고선 생성 (선택적으로 표시)
        contour_group = VGroup()
        if self.config.show_contours:  # 설정에 따라 등고선 생성 여부 결정
            contour_levels = np.linspace(
                min_z, max_z, self.config.contour_levels_count
            ).tolist()

            for level in contour_levels:
                implicit_func = ImplicitFunction(
                    lambda x, y: f(x, y, self.config.z_offset) - level,
                    color=YELLOW if abs(level) < 0.1 else WHITE,
                    x_range=[-2, 2],
                    y_range=[-2, 2],
                )
                implicit_func.set_stroke(
                    opacity=self.config.contour_opacity,
                    width=self.config.contour_stroke_width,
                )
                contour_group.add(implicit_func)

            contour_group.set_shade_in_3d(True)

        # 3D 곡면 생성 (해상도 설정 반영)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v, self.config.z_offset)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=self.config.surface_resolution,
            color=BLUE,
        )
        surface.set_opacity(self.config.surface_opacity)  # 투명도 증가
        surface.set_shade_in_3d(True)

        # 경사 하강법 실행
        path_points = gradient_descent(
            f,
            init_xy=self.config.gd_init_point,
            lr=self.config.gd_learning_rate,
            steps=self.config.gd_steps,
            z_offset=self.config.z_offset,
        )

        # 법선 벡터와 점 위치 계산
        normals, dot_positions, surface_points = self.calculate_path_points_and_normals(
            axes, path_points
        )

        # 그래디언트 경로 시각화 (점과 선)
        path_dots = VGroup()
        path_lines = VGroup()

        # 각 점마다 3D 점과 선 생성
        for i in range(len(path_points)):
            # 색상 그라데이션
            if i == 0:
                dot_color = self.config.start_color
            elif i == len(path_points) - 1:
                dot_color = self.config.end_color
            else:
                dot_color = color_gradient([GREEN_C, YELLOW_C], len(path_points) - 2)[
                    i - 1
                ]

            # 법선 벡터 방향으로 위치한 점
            dot = Dot3D(
                dot_positions[i],
                color=dot_color,
                radius=self.config.dot_radius,
            )
            dot.set_opacity(self.config.dot_opacity)
            dot.set_z_index(100)  # 높은 우선순위
            path_dots.add(dot)

            # 선도 마찬가지로 법선 방향으로 오프셋된 점들 사이에 연결
            if i > 0:
                line = Line3D(
                    dot_positions[i - 1],
                    dot_positions[i],
                    color=self.config.path_color,
                    thickness=self.config.line_thickness,
                )
                line.set_z_index(90)
                path_lines.add(line)

        # 시작점과 끝점에 강조용 링 추가
        start_ring = create_circle_3d(
            radius=self.config.dot_radius * 2.0,
            color=self.config.start_color,
            stroke_width=2,
        ).move_to(dot_positions[0])

        end_ring = create_circle_3d(
            radius=self.config.dot_radius * 2.0,
            color=self.config.end_color,
            stroke_width=2,
        ).move_to(dot_positions[-1])

        # 링을 법선 벡터에 맞춰 회전
        for ring, normal, pos in [
            (start_ring, normals[0], dot_positions[0]),
            (end_ring, normals[-1], dot_positions[-1]),
        ]:
            dot_product = np.clip(np.dot([0, 0, 1], normal), -1.0, 1.0)
            angle = np.arccos(dot_product)
            axis = np.cross([0, 0, 1], normal)
            if np.linalg.norm(axis) > 1e-6:
                ring.rotate(angle, axis, about_point=pos)
            ring.set_z_index(105)

        # 강조 점 미리 생성
        start_highlight_dot = (
            Dot3D(
                dot_positions[0],
                color=self.config.start_highlight_color,
                radius=self.config.dot_radius * 1.2,
            )
            .set_z_index(110)
            .set_opacity(self.config.dot_opacity)
        )

        end_highlight_dot = (
            Dot3D(
                dot_positions[-1],
                color=self.config.end_highlight_color,
                radius=self.config.dot_radius * 1.2,
            )
            .set_z_index(110)
            .set_opacity(self.config.dot_opacity)
        )

        # 경로 추적자 생성 (선택적)
        if self.config.use_path_tracer:
            path_tracer = self.create_path_tracer(dot_positions)
            tracer_animations, tracer_time = self.animate_path_tracer(
                path_tracer, dot_positions
            )

        # 애니메이션 구성
        self.set_camera_orientation(phi=50 * DEGREES, theta=-45 * DEGREES, zoom=0.9)
        self.begin_ambient_camera_rotation(rate=self.config.camera_rotation_rate)

        # 그리드와 축을 먼저 추가 (그리드가 표면 아래에 보이도록 순서 변경)
        self.add(axes, labels, grid)

        # 함수 수식 표시 (설정에 따라)
        if hasattr(self.config, "show_formula") and self.config.show_formula:
            self.add(formula)

        # 설정에 따라 등고선 표시 여부 결정
        if self.config.show_contours:
            self.add(contour_group)

        # 표면 생성 애니메이션
        self.play(Create(surface), run_time=2)

        # 시작점 애니메이션 - 점이 작은 크기에서 자라나는 효과
        starting_dot = Dot3D(
            dot_positions[0], color=self.config.start_color, radius=0.01
        )
        self.add(starting_dot)
        self.play(
            starting_dot.animate.scale(
                self.config.dot_radius * 100
            ),  # 작은 점에서 원래 크기로
            Create(start_ring),
            run_time=self.config.dot_animation_time,
        )
        self.remove(starting_dot)
        self.add(path_dots[0])

        self.wait(0.3)

        # 점과 선을 순차적으로 표시 - 자연스러운 성장 효과 추가
        for i in range(len(path_lines)):
            # 새 점이 작게 시작해서 커지는 효과
            next_dot = Dot3D(
                dot_positions[i + 1], color=path_dots[i + 1].get_color(), radius=0.01
            )
            self.add(next_dot)

            # 선이 시작점에서 끝점으로 자라나는 효과
            line_anim = Create(path_lines[i], run_time=self.config.line_animation_time)

            # 점 크기가 자라나는 효과
            dot_anim = next_dot.animate(run_time=self.config.dot_animation_time).scale(
                self.config.dot_radius * 100
            )

            # 현재 경사하강법 정보 업데이트 (레이블이 있을 경우)
            if info_labels and self.config.show_info_labels:
                # 현재 위치 및 그래디언트
                current_pos = path_points[i + 1]
                if i < len(path_points) - 1:
                    # 그래디언트 계산
                    grad = numerical_gradient(
                        f, path_points[i], z_offset=self.config.z_offset
                    )

                    # 레이블 업데이트
                    new_iter_label = Text(
                        f"Iteration: {i+1}",
                        font_size=self.config.label_font_size,
                        color=self.config.label_color,
                    ).move_to(iter_label)
                    new_iter_label.set_z_index(self.config.label_z_index)
                    new_iter_label.set_shade_in_3d(True)

                    # 학습률 레이블은 값이 변하지 않아도 매 반복마다 포함시켜 깜빡임 방지
                    new_lr_label = Text(
                        f"Learning Rate: {self.config.gd_learning_rate:.4f}",
                        font_size=self.config.label_font_size,
                        color=self.config.label_color,
                    ).move_to(lr_label)
                    new_lr_label.set_z_index(self.config.label_z_index)
                    new_lr_label.set_shade_in_3d(True)

                    new_pos_label = Text(
                        f"Position: ({current_pos[0]:.4f}, {current_pos[1]:.4f})",
                        font_size=self.config.label_font_size,
                        color=self.config.label_color,
                    ).move_to(pos_label)
                    new_pos_label.set_z_index(self.config.label_z_index)
                    new_pos_label.set_shade_in_3d(True)

                    new_grad_label = Text(
                        f"Gradient: ({grad[0]:.4f}, {grad[1]:.4f})",
                        font_size=self.config.label_font_size,
                        color=self.config.label_color,
                    ).move_to(grad_label)
                    new_grad_label.set_z_index(self.config.label_z_index)
                    new_grad_label.set_shade_in_3d(True)

                    # 레이블 애니메이션 (학습률 레이블 포함)
                    self.play(
                        Transform(iter_label, new_iter_label),
                        Transform(lr_label, new_lr_label),  # 학습률 업데이트 추가
                        Transform(pos_label, new_pos_label),
                        Transform(grad_label, new_grad_label),
                        run_time=0.2,  # 빠르게 업데이트
                    )

            # 선과 점 애니메이션 동시 실행
            self.play(line_anim, dot_anim)

            # 임시 점을 실제 점으로 교체
            self.remove(next_dot)
            self.add(path_dots[i + 1])

        # 경로 추적자 애니메이션 (선택적)
        if self.config.use_path_tracer:
            self.add(path_tracer)

            # 추적자가 전체 경로를 따라 움직이는 애니메이션
            for tracer_anim in tracer_animations:
                self.play(tracer_anim)

            # 추적자가 마지막에 팝 효과와 함께 사라짐
            self.play(path_tracer.animate.scale(3).set_opacity(0), run_time=0.5)
            self.remove(path_tracer)

        # 끝점 강조 - 간소화된 방식
        self.play(
            FadeOut(path_dots[0]),
            FadeOut(path_dots[-1]),
            FadeIn(start_highlight_dot),
            FadeIn(end_highlight_dot),
            Create(end_ring),
            run_time=1,
        )

        self.wait(2)
        self.stop_ambient_camera_rotation()

        # 다른 각도에서 보기
        self.move_camera(phi=80 * DEGREES, theta=0, run_time=2)
        self.wait(1)
        self.move_camera(phi=35 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.wait(1)
