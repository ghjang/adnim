from manim import *
import numpy as np


def create_regular_hexahedron(length=1, face_colors=None, face_opacity=1):
    # 한 변의 길이가 length인 정육면체의 꼭짓점 좌표 계산
    a_x = length / 2
    h_y = length / 2
    h_z = length

    vertices = [
        [a_x, -h_y, 0],           # 0: 밑면 첫 번째 꼭짓점
        [a_x, h_y, 0],            # 1: 밑면 두 번째 꼭짓점
        [-a_x, h_y, 0],           # 2: 밑면 세 번째 꼭짓점
        [-a_x, -h_y, 0],          # 3: 밑면 네 번째 꼭짓점

        [a_x, -h_y, h_z],         # 4: 윗면 첫 번째 꼭짓점
        [a_x, h_y, h_z],          # 5: 윗면 두 번째 꼭짓점
        [-a_x, h_y, h_z],         # 6: 윗면 세 번째 꼭짓점
        [-a_x, -h_y, h_z],        # 7: 윗면 네 번째 꼭짓점

        [a_x, -h_y, h_z],         # 8: 윗면 첫 번째 꼭짓점 복사본
        [a_x, h_y, h_z],          # 9: 윗면 두 번째 꼭짓점 복사본

        [-a_x, h_y, h_z],         # 10: 윗면 세 번째 꼭짓점 복사본
        [-a_x, -h_y, h_z],        # 11: 윗면 네 번째 꼭짓점 복사본

        [a_x, h_y, h_z],          # 12: 윗면 두 번째 꼭짓점 복사본
        [-a_x, h_y, h_z],         # 13: 윗면 세 번째 꼭짓점 복사본
    ]

    faces = [
        [0, 1, 2, 3],       # 0: 밑면
        [0, 4, 7, 3],       # 1: 앞면
        [0, 1, 9, 8],       # 2: 오른쪽 면
        [1, 12, 13, 2],     # 3: 뒷면
        [2, 10, 11, 3],     # 4: 왼쪽 면
        [4, 5, 6, 7],       # 5: 윗면
    ]

    # 기본 면 설정
    faces_config = {
        "fill_color": BLUE_E,
        "fill_opacity": face_opacity,
        "stroke_color": LIGHT_GREY,
        "stroke_width": 1,
    }

    graph_config = {
        "vertex_config": {
            "color": TEAL_A,  # 밝은 청록색
            "radius": 0.035,
        }
    }

    hexahedron = Polyhedron(
        vertex_coords=vertices,
        faces_list=faces,
        faces_config=faces_config,
        graph_config=graph_config
    )

    # 개별 면 색상 설정
    if face_colors:
        for face_index, color in face_colors.items():
            hexahedron.faces[face_index].set_color(color)

    return hexahedron


class HexahedronNet(ThreeDScene):
    def construct(self):
        self.next_section("Initial Settings", skip_animations=False)

        side_length = 2

        face_colors = {
            0: RED,      # 밑면
            1: GREEN,
            2: YELLOW,
            3: BLUE,
            4: PURPLE,
            5: ORANGE
        }
        hexahedron = create_regular_hexahedron(
            length=side_length,
            # face_colors=face_colors
        )
        self.play(FadeIn(hexahedron))

        self.move_camera(phi=45 * DEGREES, theta=45 * DEGREES, run_time=2)

        number_plane = NumberPlane(
            y_range=[-5, 5, 1],
            axis_config={
                "stroke_opacity": 0.2
            },
            background_line_style={
                "stroke_color": TEAL,
                "stroke_opacity": 0.4
            }
        )
        self.play(Create(number_plane), run_time=1)

        # self.move_camera(zoom=1.1, run_time=1.5)

        half_side_len = side_length / 2

        pt_1 = [half_side_len + side_length, -half_side_len, 0]
        pt_2 = [half_side_len + side_length, half_side_len, 0]

        pt_3 = [-(half_side_len + side_length), half_side_len, 0]
        pt_4 = [-(half_side_len + side_length), -half_side_len, 0]

        pt_5 = [half_side_len, half_side_len + side_length, 0]
        pt_6 = [-half_side_len, half_side_len + side_length, 0]

        pt_7 = [half_side_len, -half_side_len, side_length * 2]
        pt_8 = [-half_side_len, -half_side_len, side_length * 2]

        pt_9 = [half_side_len, -(half_side_len + side_length * 2), 0]
        pt_10 = [-half_side_len, -(half_side_len + side_length * 2), 0]
        pt_11 = [half_side_len, -(half_side_len + side_length), 0]
        pt_12 = [-half_side_len, -(half_side_len + side_length), 0]

        self.next_section(
            "Hexahedron Unfolding the Upper Side", skip_animations=False)

        self.begin_ambient_camera_rotation(rate=0.45)
        self.play(
            # 위쪽 면 위쪽 2개 정점
            hexahedron.graph[5].animate.move_to(pt_7),
            hexahedron.graph[6].animate.move_to(pt_8),
            run_time=2
        )
        self.stop_ambient_camera_rotation()

        self.next_section(
            "Hexahedron Unfolding the Rest Sides", skip_animations=False)

        self.begin_ambient_camera_rotation(rate=0.45)
        self.play(
            # 오른쪽 면 위쪽 2개 정점
            hexahedron.graph[8].animate.move_to(pt_1),
            hexahedron.graph[9].animate.move_to(pt_2),

            # 왼쪽 면 위쪽 2개 정점
            hexahedron.graph[10].animate.move_to(pt_3),
            hexahedron.graph[11].animate.move_to(pt_4),

            # 뒤쪽 면 위쪽 2개 정점
            hexahedron.graph[12].animate.move_to(pt_5),
            hexahedron.graph[13].animate.move_to(pt_6),

            #
            hexahedron.graph[5].animate.move_to(pt_9),
            hexahedron.graph[6].animate.move_to(pt_10),
            hexahedron.graph[4].animate.move_to(pt_11),
            hexahedron.graph[7].animate.move_to(pt_12),

            #
            hexahedron.faces[0].animate.set_fill(color=RED),
            hexahedron.faces[1].animate.set_fill(color=GREEN),
            hexahedron.faces[2].animate.set_fill(color=GREEN),
            hexahedron.faces[3].animate.set_fill(color=GREEN, opacity=0.75),
            hexahedron.faces[4].animate.set_fill(color=GREEN, opacity=0.75),
            hexahedron.faces[5].animate.set_fill(color=GREEN),

            run_time=4.5
        )
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=0)

        self.wait(2)
