from manim import *


class AngleMarker(VMobject):
    def __init__(
        self,
        angle: Angle,
        length: float = 0.15,
        color: str = YELLOW,
        count: int = 1,
        spacing: float = 0.1,
        stroke_width: float = 2,
        **kwargs
    ):
        super().__init__(**kwargs)

        # 각의 중심점과 반지름 가져오기
        radius = angle.radius
        line1, line2 = angle.lines
        center = line1.get_start()  # 각의 중심점

        # 각 선분의 방향 벡터 계산 (중심점 기준)
        v1 = line1.get_end() - center
        v2 = line2.get_end() - center

        # 시작 각도와 끝 각도 계산
        start_angle = np.arctan2(v1[1], v1[0])
        end_angle = np.arctan2(v2[1], v2[0])

        # 반시계 방향으로 각도 계산
        if end_angle < start_angle:
            end_angle += 2*PI

        # 실제 각도와 이등분선 각도 계산
        angle_value = end_angle - start_angle
        bisector_angle = start_angle + angle_value/2

        # 마커 간격을 실제 호의 길이에 기반하여 계산
        radian_spacing = spacing

        # 마커 각도 위치 계산
        if count == 1:
            angles = [bisector_angle]
        else:
            if count % 2 == 1:  # 홀수 개수
                angles = [
                    bisector_angle + radian_spacing * (i - (count-1)/2)
                    for i in range(count)
                ]
            else:  # 짝수 개수
                angles = [
                    bisector_angle + radian_spacing * (i - (count/2 - 0.5))
                    for i in range(count)
                ]

        # 각 위치에 마커 생성 (중심점 기준)
        half_length = length / 2
        for theta in angles:
            direction = np.array([
                np.cos(theta),
                np.sin(theta),
                0
            ])
            marker = Line(
                center + radius * direction - half_length * direction,
                center + radius * direction + half_length * direction,
                color=color,
                stroke_width=stroke_width
            )
            self.add(marker)
