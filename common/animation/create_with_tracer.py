from manim import *


class CreateWithTracer(Create):
    def __init__(self, mobject, tracer_config=None, **kwargs):
        if not hasattr(mobject, 'metadata'):
            raise ValueError("Mobject must have metadata")
        if 'base_plane' not in mobject.metadata:
            raise ValueError("Mobject metadata must contain 'base_plane'")
        if 'x_range' not in mobject.metadata:
            raise ValueError("Mobject metadata must contain 'x_range'")

        # Create의 기본 rate_func 저장 (기본값: smooth)
        self.rate_func = kwargs.get("rate_func", smooth)

        super().__init__(mobject, **kwargs)

        self.base_plane = mobject.metadata["base_plane"]
        self.x_range = mobject.metadata["x_range"]
        self.tracer_config = tracer_config or {}

        # 화면좌표계 고정 위치 모드 추가
        self.screen_fixed_lines = self.tracer_config.get(
            "screen_fixed_lines", False)
        if self.screen_fixed_lines:
            # 화면상의 고정 x, y 좌표 (기본값: 화면 전체)
            self.fixed_x_range = self.tracer_config.get(
                "fixed_x_range", [-config.frame_width/2, config.frame_width/2])
            self.fixed_y_range = self.tracer_config.get(
                "fixed_y_range", [-config.frame_height/2, config.frame_height/2])

        # 평면의 스케일 계산 (원점과 (1,0) 사이의 거리로 계산)
        origin = self.base_plane.c2p(0, 0)
        unit_x = self.base_plane.c2p(1, 0)
        scale_factor = np.linalg.norm(unit_x - origin)

        # 화면 크기의 2배를 기본값으로 설정
        default_width = config.frame_width * 4
        default_height = config.frame_height * 4

        # 점과 십자선의 기본 설정 분리
        base_radius = self.tracer_config.get("radius", 0.08)
        self.dot_config = {
            "color": self.tracer_config.get("color", RED),
            "radius": base_radius * scale_factor,
            "opacity": self.tracer_config.get("dot_opacity", 1.0),  # 점 불투명도
            "cross_lines": self.tracer_config.get("cross_lines", False),
            # 수평선 표시 여부
            "show_h_line": self.tracer_config.get("show_h_line", True),
            # 수직선 표시 여부
            "show_v_line": self.tracer_config.get("show_v_line", True),
            "cross_stroke_width": self.tracer_config.get("cross_stroke_width", 1),
            # 십자선 불투명도: 지정되지 않으면 점의 불투명도 사용
            "cross_opacity": self.tracer_config.get("cross_opacity",
                                                    self.tracer_config.get("dot_opacity", 0.8)),  # 기본값 0.8로 증가
            # 십자선 영역 설정 (넘버플레인 좌표계 단위)
            # 좌측 영역
            "cross_left": self.tracer_config.get("cross_left", default_width),
            # 우측 영역
            "cross_right": self.tracer_config.get("cross_right", default_width),
            # 상단 영역
            "cross_up": self.tracer_config.get("cross_up", default_height),
            # 하단 영역
            "cross_down": self.tracer_config.get("cross_down", default_height)
        }

    def _create_tracer(self):
        """트레이서 그룹(점 + 십자선) 생성"""
        group = VGroup()

        if self.dot_config["cross_lines"]:
            # 수평선 생성 (show_h_line이 True일 때만)
            if self.dot_config["show_h_line"]:
                self.h_line = Line(
                    stroke_width=self.dot_config["cross_stroke_width"],
                    color=self.dot_config["color"]
                )
                self.h_line.set_opacity(self.dot_config["cross_opacity"])
                group.add(self.h_line)

            # 수직선 생성 (show_v_line이 True일 때만)
            if self.dot_config["show_v_line"]:
                self.v_line = Line(
                    stroke_width=self.dot_config["cross_stroke_width"],
                    color=self.dot_config["color"]
                )
                self.v_line.set_opacity(self.dot_config["cross_opacity"])
                group.add(self.v_line)

        # 점을 나중에 생성 (십자선 위에 그려지도록)
        self.dot = Dot(radius=self.dot_config["radius"],
                       color=self.dot_config["color"])
        self.dot.set_opacity(self.dot_config["opacity"])
        group.add(self.dot)

        return group

    def _setup_scene(self, scene):
        self.tracer = self._create_tracer()
        scene.add(self.tracer)

    def interpolate_mobject(self, alpha):
        super().interpolate_mobject(alpha)

        if hasattr(self, 'tracer'):
            # Create 애니메이션의 rate_func을 그대로 적용
            adjusted_alpha = self.rate_func(alpha)

            x = self.x_range[0] + adjusted_alpha * \
                (self.x_range[1] - self.x_range[0])
            y = self.mobject.underlying_function(x)
            transformed_point = self.base_plane.c2p(x, y)
            self.tracer.move_to(transformed_point)

            # 현재 트레이서 위치 계산
            adjusted_alpha = self.rate_func(alpha)
            x = self.x_range[0] + adjusted_alpha * \
                (self.x_range[1] - self.x_range[0])
            y = self.mobject.underlying_function(x)
            current_point = self.base_plane.c2p(x, y)

            # 트레이서 점 이동
            self.dot.move_to(current_point)

            if self.dot_config["cross_lines"]:
                if self.screen_fixed_lines:
                    # 화면좌표계 고정 위치 모드
                    if self.dot_config["show_h_line"]:
                        # 가로선: 고정된 x 범위, 현재 y 위치
                        self.h_line.put_start_and_end_on(
                            [self.fixed_x_range[0], current_point[1], 0],
                            [self.fixed_x_range[1], current_point[1], 0]
                        )
                    if self.dot_config["show_v_line"]:
                        # 세로선: 현재 x 위치, 고정된 y 범위
                        self.v_line.put_start_and_end_on(
                            [current_point[0], self.fixed_y_range[0], 0],
                            [current_point[0], self.fixed_y_range[1], 0]
                        )
                else:
                    # 기존 NumberPlane 좌표계 기준 모드
                    if self.dot_config["show_h_line"]:
                        h_start = self.base_plane.c2p(
                            -self.dot_config["cross_left"], y)
                        h_end = self.base_plane.c2p(
                            self.dot_config["cross_right"], y)
                        self.h_line.put_start_and_end_on(h_start, h_end)
                    if self.dot_config["show_v_line"]:
                        v_start = self.base_plane.c2p(
                            x, -self.dot_config["cross_down"])
                        v_end = self.base_plane.c2p(
                            x, self.dot_config["cross_up"])
                        self.v_line.put_start_and_end_on(v_start, v_end)

    def clean_up_from_scene(self, scene: Scene):
        super().clean_up_from_scene(scene)
        if hasattr(self, 'tracer'):
            scene.remove(self.tracer)
