from manim import *
from common.manim_utils import create_code_block_from_file


class ThreeDAxesExample(ThreeDScene):
    def construct(self):
        self.next_section("Code - 00", skip_animations=False)

        title_text = Text("Default Scene Settings").to_edge(UL)
        self.add(title_text)

        code_block = create_code_block_from_file(
            "016_code_00.py",
            font_size=20
        ).shift(DOWN / 2)
        self.add(code_block)
        self.wait(2)
        self.play(
            FadeOut(title_text),
            FadeOut(code_block)
        )

        self.next_section("Intro Setting", skip_animations=False)

        number_plane = NumberPlane()
        self.add(number_plane)

        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label(Text("x", font_size=60, color=TEAL))
        y_label = axes.get_y_axis_label(Text("y", font_size=60, color=TEAL))
        z_label = axes.get_z_axis_label(Text("z", font_size=60, color=TEAL))
        axis_labels = VGroup(x_label, y_label, z_label)
        self.add(axes, axis_labels)

        text = Text("3D Axes Example", font_size=68, color=RED)
        self.add(text)

        self.wait(1)

        self.next_section("Camera Move with 'phi' Parameter",
                          skip_animations=False)

        code_block = create_code_block_from_file(
            "016_code_01_phi.py",
            font_size=14.5,
            insert_line_no=False
        ).to_edge(UL, buff=0.2)
        self.add(code_block)
        self.wait(2)

        # 카메라 오리엔테이션 설정을 애니메이션화
        #
        # NOTE: 'phi, theta'의 값은 '구면 좌표계' 상에서 '절대값'이다.
        #       'phi=0도, theta=-90도'가 기본값으로 기본적으로 카메라의 위치는
        #       'xy 평면'을 바라보는 방향
        # 이다. 즉 'z축'과 '평행한 방향'으로 카메라가 위치한다.

        self.move_camera(phi=90 * DEGREES, run_time=2)  # z축을 시야 뒤쪽으로 90도 회전
        self.move_camera(phi=-90 * DEGREES, run_time=4)  # z축을 시야 앞쪽으로 90도 회전
        self.move_camera(phi=0, run_time=2)  # phi의 기본값: 0

        self.next_section("Camera Move with 'theta' parameter",
                          skip_animations=False)

        next_code_block = create_code_block_from_file(
            "016_code_02_theta.py",
            font_size=14.5,
            insert_line_no=False
        ).to_edge(UL, buff=0.2)
        self.play(FadeOut(code_block), FadeIn(next_code_block))
        code_block = next_code_block
        self.wait(2)

        # 대상을 원 기준 위치에서 시계 방향으로 45도 회전
        self.move_camera(theta=-45 * DEGREES, run_time=2)
        self.move_camera(theta=-90 * DEGREES, run_time=2)  # theta의 기본값: -90도
        self.move_camera(theta=0, run_time=4)  # 대상을 원 기준 위치에서 시계 방향으로 90도 회전
        self.move_camera(theta=-90 * DEGREES, run_time=4)  # theta의 기본값: -90도

        self.next_section(
            "Camera Move with 'phi, theta, gamma' parameters", skip_animations=False)

        next_code_block = create_code_block_from_file(
            "016_code_03_all.py",
            font_size=14.5,
            insert_line_no=False
        ).to_edge(UL, buff=0.2)
        self.play(FadeOut(code_block), FadeIn(next_code_block))
        code_block = next_code_block
        self.wait(2)

        # 대상을 원 기준 위치에서 반시계 방향으로 45도 회전
        self.move_camera(theta=-135 * DEGREES, run_time=2)
        self.move_camera(phi=45 * DEGREES, run_time=2)
        self.move_camera(phi=0, run_time=2)
        self.move_camera(theta=-90 * DEGREES, run_time=2)
        self.move_camera(gamma=0, run_time=1)  # gamma의 기본값: 0
        self.move_camera(gamma=45 * DEGREES, run_time=2)  # 반시계 방향으로 45도 회전
        self.move_camera(gamma=-45 * DEGREES, run_time=2)  # 시계 방향으로 90도 회전

        self.wait(3)
