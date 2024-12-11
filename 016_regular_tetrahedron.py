from manim import *
import numpy as np


class TetrahedronPlanarFigure(ThreeDScene):
    @staticmethod
    def create_regular_tetrahedron(length=1, face_colors=None, face_opacity=1):
        # 한 변의 길이가 length인 정사면체의 꼭짓점 좌표 계산
        a = length / 2
        h = length * np.sqrt(3) / 2
        h2 = length * np.sqrt(6) / 3

        vertices = [
            [a, 0, 0],              # 첫 번째 꼭짓점
            [0, h, 0],              # 두 번째 꼭짓점
            [-a, 0, 0],             # 세 번째 꼭짓점
            [0, h/3, h2],           # 꼭대기 꼭짓점
            [0, h/3, h2],           # 꼭대기 꼭짓점 복사본
            [0, h/3, h2]            # 꼭대기 꼭짓점 복사본
        ]

        faces = [
            [0, 1, 2],  # 밑면
            [0, 1, 3],  # 앞면
            [1, 2, 4],  # 오른쪽면
            [2, 0, 5]   # 왼쪽면
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

        rotation_edges = {
            0: (vertices[0], vertices[1]),
            1: (vertices[1], vertices[2]),
            2: (vertices[2], vertices[0])
        }

        return tetrahedron, rotation_edges

    def construct(self):
        # 면 색상 지정 예시
        face_colors = {
            0: RED,      # 밑면
            2: YELLOW,   # 오른쪽 면
        }
        tetrahedron, rotation_edges = self.create_regular_tetrahedron(
            length=2,
            face_colors=face_colors
        )
        # tetrahedron.move_to(ORIGIN)
        self.add(tetrahedron)

        # 카메라 설정
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait(1)

        # xy평면 상의 두 점으로부터 정삼각형의 세 번��� 점 계산
        def calc_triangle_point(p1, p2, direction):
            # 두 점 사이의 거리 계산
            edge_len = np.linalg.norm(p2[:2] - p1[:2])
            # 정삼각형의 높이
            height = edge_len * np.sqrt(3) / 2

            # 변의 중점
            mid = (p1[:2] + p2[:2]) / 2
            # 변에 수직인 방향 벡터
            normal = np.array([-p2[1] + p1[1], p2[0] - p1[0]])
            normal = normal / np.linalg.norm(normal)

            # 중점에서 높이만큼 수직방향으로 이동
            top = mid + height * normal * direction
            return np.array([top[0], top[1], 0])

        # 각 변에 대해 정삼각형의 세 번째 점 계산
        edge1 = np.array(rotation_edges[0])  # 첫 번째 변의 두 점
        edge2 = np.array(rotation_edges[1])  # 두 번째 변의 두 점
        edge3 = np.array(rotation_edges[2])  # 세 번째 변의 두 점

        top_1 = calc_triangle_point(edge1[0], edge1[1], 1)  # 우상단
        top_2 = calc_triangle_point(edge2[0], edge2[1], -1)  # 좌상단
        top_3 = calc_triangle_point(edge3[0], edge3[1], -1)  # 하단

        top_1 = [(1 + np.sqrt(3)) / 4, (3 + np.sqrt(3)) / 4, 0]
        top_2 = [-(1 + np.sqrt(3)) / 4, (3 + np.sqrt(3)) / 4, 0]
        top_3 = [0, -(np.sqrt(3) / 2), 0]

        # 정점들을 완전히 xy평면으로 펼치기
        self.play(
            tetrahedron.graph[3].animate.move_to(top_1),
            tetrahedron.graph[4].animate.move_to(top_2),
            tetrahedron.graph[5].animate.move_to(top_3),
            run_time=2
        )

        self.wait(2)
