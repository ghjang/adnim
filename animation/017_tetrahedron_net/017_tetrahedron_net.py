from manim import *
import numpy as np


def create_regular_tetrahedron(length=1, face_colors=None, face_opacity=1):
    # 한 변의 길이가 length인 정사면체의 꼭짓점 좌표 계산
    a_x = length / 2
    h_y = length * np.sqrt(3) / 2
    h_z = length * np.sqrt(6) / 3

    vertices = [
        [a_x, 0, 0],              # 첫 번째 꼭짓점
        [0, h_y, 0],              # 두 번째 꼭짓점
        [-a_x, 0, 0],             # 세 번째 꼭짓점
        [0, h_y / 3, h_z],        # 꼭대기 꼭짓점
        [0, h_y / 3, h_z],        # 꼭대기 꼭짓점 복사본
        [0, h_y / 3, h_z]         # 꼭대기 꼭짓점 복사본
    ]

    faces = [
        [0, 1, 2],  # 밑면
        [0, 1, 3],
        [1, 2, 4],
        [2, 0, 5]
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

    tetrahedron = Polyhedron(
        vertex_coords=vertices,
        faces_list=faces,
        faces_config=faces_config,
        graph_config=graph_config
    )

    # 개별 면 색상 설정
    if face_colors:
        for face_index, color in face_colors.items():
            tetrahedron.faces[face_index].set_color(color)

    return tetrahedron


class TetrahedronNet(ThreeDScene):
    def construct(self):
        self.next_section("Initial Settings", skip_animations=False)

        side_length = 2

        face_colors = {
            0: RED,      # 밑면
            1: GREEN,
            2: YELLOW,
            3: BLUE
        }
        tetrahedron = create_regular_tetrahedron(
            length=side_length,
            # face_colors=face_colors
        )
        self.play(FadeIn(tetrahedron))

        self.next_section("Tetrahedron Unfolding", skip_animations=False)

        self.move_camera(phi=45 * DEGREES, theta=-45 * DEGREES, run_time=2)

        number_plane = NumberPlane(
            axis_config={
                "stroke_opacity": 0.2
            },
            background_line_style={
                "stroke_color": TEAL,
                "stroke_opacity": 0.4
            }
        )
        self.play(Create(number_plane), run_time=1)

        self.move_camera(zoom=1.5, run_time=1.5)

        h = (side_length / 2) * np.sqrt(3)
        top_1 = [side_length, h, 0]
        top_2 = [-side_length, h, 0]
        top_3 = [0, -h, 0]

        # 정점들을 완전히 xy평면으로 펼치기
        self.begin_ambient_camera_rotation(rate=0.45)
        self.play(
            tetrahedron.graph[3].animate.move_to(top_1),
            tetrahedron.graph[4].animate.move_to(top_2),
            tetrahedron.graph[5].animate.move_to(top_3),
            run_time=6
        )
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=0)

        self.wait(2)
