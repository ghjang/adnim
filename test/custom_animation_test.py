from manim import *


class GrowAndSpin(Animation):
    def __init__(self, mobject, scale_factor=2, clockwise=True, **kwargs):
        self.scale_factor = scale_factor
        self.clockwise = clockwise  # 회전 방향 설정
        self.starting_mobject = mobject.copy()
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        # 시작 상태의 복사본 생성
        new_mob = self.starting_mobject.copy()

        # 크기와 회전을 한번에 적용 (회전 방향 고려)
        new_mob.scale(1 + (self.scale_factor * alpha))
        rotation_angle = alpha * 2 * PI * (-1 if self.clockwise else 1)
        new_mob.rotate(rotation_angle)

        # 현재 모브젝트를 새로운 상태로 갱신
        self.mobject.become(new_mob)


class CustomAnimationExample(Scene):
    def construct(self):
        circle = Circle(color=RED, radius=3)
        square = Square(color=BLUE, side_length=1)

        # square를 circle보다 위에 표시
        square.set_z_index(1)
        circle.set_z_index(0)

        self.play(
            Create(circle),
            GrowAndSpin(square, scale_factor=6),
            run_time=5
        )

        self.wait(1)


class CustomAnimationExample2(Scene):
    def construct(self):
        # 두 개의 사각형으로 서로 다른 방향 회전 테스트
        square1 = Square(color=BLUE, side_length=1).shift(LEFT * 2)
        square2 = Square(color=RED, side_length=1).shift(RIGHT * 2)

        # z-index 설정
        square1.set_z_index(1)
        square2.set_z_index(1)

        # 서로 다른 방향으로 회전하는 애니메이션
        self.play(
            GrowAndSpin(square1, scale_factor=3, clockwise=True),
            GrowAndSpin(square2, scale_factor=3, clockwise=False),
            run_time=5
        )

        self.wait(1)
