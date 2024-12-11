from manim import *
import numpy as np


class RegularTriangleIn3D(ThreeDScene):
    def construct(self):
        # 좌표축 생성
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-2, 2],
        )

        # 축 레이블 생성
        x_label = Text("x").next_to(axes.x_axis, RIGHT)
        y_label = Text("y").next_to(axes.y_axis, UP)
        z_label = Text("z").next_to(axes.z_axis, OUT)
        labels = VGroup(x_label, y_label, z_label)

        # 정삼각형 생성 - 논리 좌표를 화면 좌표로 변환
        triangle = Polygon(
            axes.c2p(0, 0, 0),
            axes.c2p(1, 0, 0),
            axes.c2p(0.5, np.sqrt(3)/2, 0),
            color=BLUE
        )

        # 씬에 추가
        self.add(axes, labels, triangle)

        # 카메라 설정 - 축과 정삼각형이 잘 보이는 각도
        # self.set_camera_orientation(
        #     phi=75 * DEGREES,
        #     theta=30 * DEGREES,
        #     zoom=1.5  # 확대 설정
        # )

        self.wait(2)


class SquarePyramidScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        vertex_coords = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
            [0, 0, 2],
            [0, 0, 3],
        ]
        faces_list = [
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 1, 2, 3]
        ]
        pyramid = Polyhedron(vertex_coords, faces_list)
        self.add(pyramid)

        self.wait(2)


class SineSurfaceExample(ThreeDScene):
    def construct(self):
        # 기본적인 포물면 생성
        paraboloid = Surface(
            lambda u, v: np.array([
                u,
                v,
                u**2 + v**2
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2]
        )

        # 사인파 표면
        wave = Surface(
            lambda u, v: np.array([
                u,
                v,
                np.sin(u) * np.cos(v)
            ]),
            u_range=[-3, 3],
            v_range=[-3, 3]
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(paraboloid)  # or self.add(wave)

        self.wait(2)

    class TetrahedronScene(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(phi=0, theta=0, gamma=0)

        base_tetrahedron = Tetrahedron()
        self.add(base_tetrahedron)

        for i in range(4):
            vertex = base_tetrahedron.graph[i]
            coords = vertex.get_center()
            print(f"Vertex {i}: {coords}")

        self.wait(2)


class TriangleScene(ThreeDScene):
    def construct(self):
        # 카메라 위치 설정
        # self.set_camera_orientation(phi=0, theta=0)

        # 정삼각형의 꼭짓점 정의
        vertices = [
            [0.5, 0, 0],
            [0, np.sqrt(3)/2, 0],
            [-0.5, 0, 0]
        ]

        # 면 정의 (시계방향)
        faces = [[0, 1, 2]]

        # 정삼각형 생성
        triangle = Polyhedron(vertex_coords=vertices, faces_list=faces)
        triangle.set_fill(BLUE, opacity=0.5)
        triangle.set_stroke(WHITE, width=1)

        self.add(triangle)
        self.wait(2)
