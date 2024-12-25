from manim import *
from common.angle_decoration import AngleMarker


class RightAngleTest(Scene):
    def construct(self):
        line1 = Line(ORIGIN, RIGHT)
        line2 = Line(ORIGIN, UP)
        mob = RightAngle(line1, line2, color=YELLOW, stroke_width=7)
        self.add(VGroup(mob, line1, line2).shift(DL*0.3))


class AngleTest(Scene):
    def construct(self):
        line1 = Line(LEFT*0.2, RIGHT)
        line2 = Line(DOWN*0.2, UP)
        a = Angle(line1, line2, dot=True, color=YELLOW, dot_color=YELLOW)
        self.add(VGroup(line1, line2, a).move_to(ORIGIN))


class AngleWithLabelTest(Scene):
    def construct(self):
        line1 = Line((LEFT+(1/3)*UP)*0.1, RIGHT+(1/3)*DOWN)
        line2 = Line((DOWN+(1/3)*RIGHT)*0.1, UP+(1/3)*LEFT)
        angle = Angle(line1, line2, radius=0.3)
        value = Integer(angle.get_value(degrees=True),
                        unit='^{\circ}', color=YELLOW)
        value.next_to(angle, UR, buff=0)
        self.add(VGroup(line1, line2, angle, value).move_to(ORIGIN))


class AngleBisectorTest(Scene):
    def construct(self):
        # 두 선 생성
        line1 = Line(ORIGIN, 2*RIGHT)
        line2 = Line(ORIGIN, 2*UP)

        # 각 생성
        angle = Angle(line1, line2, radius=0.5, color=BLUE)

        # 이등분선 생성
        bisector_angle = angle.get_value() / 2  # 라디안 단위
        bisector = Line(
            ORIGIN,
            2 * (np.cos(bisector_angle) * RIGHT + np.sin(bisector_angle) * UP),
            color=YELLOW
        )

        # 그룹으로 만들어 표시
        self.add(VGroup(line1, line2, angle, bisector).move_to(ORIGIN))


class ShortAngleBisectorTest(Scene):
    def construct(self):
        # 두 선 생성 (60도 각도로 설정)
        line1 = Line(ORIGIN, 2*RIGHT)
        line2 = Line(ORIGIN, 2*(np.cos(PI/3)*RIGHT + np.sin(PI/3)*UP))

        # 각 생성
        radius = 0.5
        angle = Angle(line1, line2, radius=radius, color=BLUE)

        # 이등분선의 방향 계산
        bisector_angle = angle.get_value() / 2
        direction = np.array([
            np.cos(bisector_angle),
            np.sin(bisector_angle),
            0
        ])

        # 호와 교차하는 점을 중심으로 더 짧은 선분 생성 (총 길이 0.2)
        short_bisector = Line(
            radius * direction - 0.1 * direction,  # 시작점
            radius * direction + 0.1 * direction,  # 끝점
            color=YELLOW
        )

        # 그룹으로 만들어 표시
        self.add(VGroup(line1, line2, angle, short_bisector))


class AngleMarkerTest(Scene):
    def construct(self):
        # 첫 번째 각도 (60도) - 변경없음
        line1 = Line(ORIGIN, RIGHT*2)
        line2 = Line(ORIGIN, 2*(np.cos(PI/3)*RIGHT + np.sin(PI/3)*UP))
        angle1 = Angle(line1, line2, radius=0.5, color=BLUE)
        marker1 = AngleMarker(angle1)
        group1 = VGroup(line1, line2, angle1, marker1)

        # 두 번째 각도 (같은 60도, 선분 순서 수정)
        line3 = Line(ORIGIN, 2*(np.cos(4*PI/3)*LEFT + np.sin(4*PI/3)*UP))  # 수정
        line4 = Line(ORIGIN, 2*LEFT)  # 수정
        angle2 = Angle(line3, line4, radius=0.5, color=BLUE)
        marker2 = AngleMarker(angle2)
        group2 = VGroup(line3, line4, angle2, marker2)

        # 배치는 동일
        group1.shift(RIGHT*2)
        group2.shift(LEFT*2)

        self.add(group1, group2)


class MultipleAngleMarkersTest(Scene):
    def construct(self):
        # 60도 각도 생성
        line1 = Line(ORIGIN, 2*RIGHT)
        line2 = Line(ORIGIN, 2*(np.cos(PI/3)*RIGHT + np.sin(PI/3)*UP))

        # 홀수 개수 마커 테스트
        angle1 = Angle(line1, line2, radius=0.5, color=BLUE)
        markers1 = AngleMarker(angle1, count=3)
        group1 = VGroup(line1, line2, angle1, markers1)

        # 짝수 개수 마커 테스트
        line3 = Line(ORIGIN, 2*RIGHT)
        line4 = Line(ORIGIN, 2*(np.cos(-PI/3)*RIGHT + np.sin(-PI/3)*DOWN))
        angle2 = Angle(line3, line4, radius=0.5, color=BLUE)
        markers2 = AngleMarker(angle2, count=4)
        group2 = VGroup(line3, line4, angle2, markers2)

        # 배치
        group1.shift(RIGHT*2)
        group2.shift(LEFT*2)

        self.add(group1, group2)


class MultipleMarkerRangeTest(Scene):
    def construct(self):
        examples = [
            # [각도, 마커수, 위치좌표, 방향]
            # 첫 번째 행: 1,2,3개 마커
            [PI/3, 1, [-4, 1.5, 0], 0],          # 60도, 1개 마커
            [PI/2, 2, [0, 1.5, 0], PI/6],        # 90도, 2개 마커
            [2*PI/3, 3, [4, 1.5, 0], -PI/6],     # 120도, 3개 마커
            # 두 번째 행: 4,5,6개 마커
            [3*PI/4, 4, [-4, -1.5, 0], PI/4],    # 135도, 4개 마커
            [PI/4, 5, [0, -1.5, 0], -PI/4],      # 45도, 5개 마커
            [PI/2, 6, [4, -1.5, 0], 0],          # 90도, 6개 마커
        ]

        for angle_value, marker_count, pos, rotation in examples:
            # 회전된 각도 생성
            line1 = Line(ORIGIN, RIGHT*2.0)  # 선 길이 증가
            line2 = Line(
                ORIGIN,
                2.0*(np.cos(angle_value)*RIGHT +
                     np.sin(angle_value)*UP)  # 선 길이 증가
            )
            group = VGroup(line1, line2)
            group.rotate(rotation)

            # 각과 마커 생성
            angle = Angle(line1, line2, radius=0.6, color=BLUE)  # 반지름 증가
            markers = AngleMarker(
                angle,
                count=marker_count,
                stroke_width=1.5,
                length=0.15  # 마커 길이도 약간 증가
            )

            # 그룹으로 만들고 위치 지정
            group = VGroup(line1, line2, angle, markers)
            group.move_to(pos)

            self.add(group)
