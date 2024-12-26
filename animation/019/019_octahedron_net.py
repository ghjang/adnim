from manim import *
import numpy as np


def create_regular_octahedron(length=1, face_colors=None, face_opacity=1):
    # 정8면체의 꼭짓점 좌표 계산
    a = length / np.sqrt(2)
    vertices = [
        [0, 0, a],        # 0: 상단 꼭짓점
        [a, 0, 0],        # 1: 중간 첫 번째 꼭짓점
        [0, a, 0],        # 2: 중간 두 번째 꼭짓점
        [-a, 0, 0],       # 3: 중간 세 번째 꼭짓점
        [0, -a, 0],       # 4: 중간 네 번째 꼭짓점
        [0, 0, -a],       # 5: 하단 꼭짓점

        # 전개도를 위한 복제 꼭짓점
        [0, 0, a],        # 6: 상단 꼭짓점 복사
        [a, 0, 0],        # 7: 중간 첫 번째 꼭짓점 복사
        [-a, 0, 0],        # 8: 중간 세 번째 꼭짓점 복사
        [0, 0, -a],       # 9: 하단 꼭짓점 복사
    ]

    faces = [
        [0, 4, 1],      # 0: 상단 앞쪽 오른쪽
        [6, 3, 4],      # 1: 상단 앞쪽 왼쪽
        [6, 7, 2],      # 2: 상단 뒤쪽 오른쪽
        [6, 3, 2],      # 3: 상단 뒤쪽 왼쪽

        [4, 5, 1],      # 4: 하단 앞쪽 오른쪽
        [4, 3, 5],      # 5: 하단 앞쪽 왼쪽
        [9, 7, 2],      # 6: 하단 뒤쪽 오른쪽
        [9, 8, 2],      # 7: 하단 뒤쪽 왼쪽
    ]

    faces_config = {
        "fill_color": BLUE_E,
        "fill_opacity": face_opacity,
        "stroke_color": LIGHT_GREY,
        "stroke_width": 1,
    }

    graph_config = {
        "vertex_config": {
            "color": TEAL_A,
            "radius": 0.035,
        }
    }

    octahedron = Polyhedron(
        vertex_coords=vertices,
        faces_list=faces,
        faces_config=faces_config,
        graph_config=graph_config
    )

    if face_colors:
        for face_index, color in face_colors.items():
            octahedron.faces[face_index].set_color(color)

    return octahedron


class OctahedronNet(ThreeDScene):
    def construct(self):
        self.next_section("Initial Settings", skip_animations=False)

        side_length = 2
        octahedron = create_regular_octahedron(length=side_length)
        octahedron.shift([0, 0, side_length / np.sqrt(2)])
        self.play(FadeIn(octahedron))

        self.move_camera(phi=55 * DEGREES, theta=-55 * DEGREES, run_time=2)

        number_plane = NumberPlane(
            y_range=[-5, 5, 1],
            axis_config={"stroke_opacity": 0.2},
            background_line_style={
                "stroke_color": TEAL,
                "stroke_opacity": 0.4
            }
        )
        self.play(Create(number_plane), run_time=1)

        half_side_len = side_length / 2
        h = side_length * np.sqrt(3) / 2

        pt_0 = [side_length, h * 2, 0]
        pt_1 = [side_length + half_side_len, h, 0]
        pt_2 = [-side_length, 0, 0]
        pt_3 = [0, 0, 0]
        pt_4 = [half_side_len, h, 0]
        pt_5 = [side_length, 0, 0]
        pt_6 = [-half_side_len, h, 0]
        pt_7 = [-(side_length + half_side_len), h, 0]
        pt_8 = [-(side_length + half_side_len), -h, 0]
        pt_9 = [-side_length * 2, 0, 0]

        self.next_section("Octahedron Unfolding", skip_animations=False)

        self.move_camera(zoom=1.2, run_time=1.5)

        self.begin_ambient_camera_rotation(rate=0.65)
        self.play(
            # 위쪽 삼각형들 펼치기
            octahedron.graph[0].animate.move_to(pt_0),
            octahedron.graph[1].animate.move_to(pt_1),
            octahedron.graph[2].animate.move_to(pt_2),
            octahedron.graph[3].animate.move_to(pt_3),
            octahedron.graph[4].animate.move_to(pt_4),
            octahedron.graph[5].animate.move_to(pt_5),
            octahedron.graph[6].animate.move_to(pt_6),
            octahedron.graph[7].animate.move_to(pt_7),
            octahedron.graph[8].animate.move_to(pt_8),
            octahedron.graph[9].animate.move_to(pt_9),

            # 면 색상 변경
            octahedron.faces[0].animate.set_fill(color=PINK),
            octahedron.faces[1].animate.set_fill(color=GREEN),
            octahedron.faces[2].animate.set_fill(color=GREEN),
            octahedron.faces[3].animate.set_fill(color=PINK),
            octahedron.faces[4].animate.set_fill(color=GREEN),
            octahedron.faces[5].animate.set_fill(color=PINK),
            octahedron.faces[6].animate.set_fill(color=PINK),
            octahedron.faces[7].animate.set_fill(color=GREEN),

            run_time=9
        )
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=0)
        self.wait(2)
