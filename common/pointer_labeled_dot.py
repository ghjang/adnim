from manim import *


class PointerLabeledDot(VGroup):
    def __init__(
        self,
        point=ORIGIN,
        label_text="",
        pointer_direction=DR,
        pointer_length=0.7,
        dot_radius=0.08,
        dot_color=WHITE,
        arrow_color=WHITE,
        label_color=WHITE,
        label_font_size=24,
        **kwargs
    ):
        super().__init__(**kwargs)

        # 화살표 길이 저장
        self.pointer_length = pointer_length

        # 점 생성
        self.dot = Dot(point=point, radius=dot_radius, color=dot_color)

        # 화살표 끝점은 점의 위치
        arrow_end = point
        # 화살표 시작점은 pointer_direction의 반대 방향으로 pointer_length만큼
        arrow_start = point + pointer_length * (-pointer_direction)

        # 화살표 생성
        self.arrow = Arrow(
            start=arrow_start,
            end=arrow_end,
            buff=dot_radius,
            color=arrow_color
        )

        # 라벨 텍스트 생성 및 화살표 시작점 근처에 배치 (수정된 부분)
        self.label = Text(
            label_text,
            color=label_color,
            font_size=label_font_size
        )
        self.label.next_to(self.arrow.get_start(), -
                           pointer_direction, buff=0.1)

        # 색상 저장을 위한 추가 속성
        self.stored_label_color = label_color

        # VGroup에 요소들 추가
        self.add(self.dot, self.arrow, self.label)

    def get_dot_center(self):
        return self.dot.get_center()

    def move_to(self, point):
        """그룹 전체를 이동 (기존 VGroup의 move_to)"""
        super().move_to(point)
        return self

    def move_dot_to(self, point):
        """점을 특정 위치로 이동하고 화살표와 라벨도 함께 조정"""
        # 현재 점과 목표 위치 간의 이동 벡터 계산
        shift_vec = point - self.dot.get_center()
        # 전체 그룹을 해당 벡터만큼 이동
        self.shift(shift_vec)
        return self

    def set_label_text(self, new_text):
        """라벨 텍스트 변경"""
        new_label = Text(
            new_text,
            color=self.label.get_color(),
            font_size=self.label.font_size
        )
        new_label.move_to(self.label.get_center())
        self.remove(self.label)
        self.label = new_label
        self.add(self.label)
        return self

    def copy_and_change(self, new_point=None, new_label_text=None, new_direction=None):
        """현재 상태를 복사하고 지정된 속성만 변경"""
        new_dot = self.copy()

        if new_point is not None:
            shift_vec = new_point - new_dot.dot.get_center()
            new_dot.shift(shift_vec)

        if new_direction is not None:
            dot_center = new_dot.dot.get_center()

            # 화살표 시작점과 끝점 계산 (저장된 길이 사용)
            arrow_end = dot_center
            arrow_start = dot_center + self.pointer_length * (-new_direction)

            # 새 화살표 생성
            new_arrow = Arrow(
                start=arrow_start,
                end=arrow_end,
                buff=self.dot.radius,
                color=new_dot.arrow.get_color()
            )

            # 화살표 교체
            new_dot.remove(new_dot.arrow)
            new_dot.arrow = new_arrow
            new_dot.add(new_arrow)

            # 라벨 위치 재조정
            new_dot.label.next_to(arrow_start, -new_direction, buff=0.1)

        if new_label_text is not None:
            # NOTE: 'self.label.color' 속성과 유사 속성등이 최초 객체 생성시 지정한 색이 아닌 '검정색'을 반환한다.
            #       별도로 저장한 색상을 사용하여 새 라벨을 생성한다.
            new_label = Text(
                new_label_text,
                color=self.stored_label_color,
                font_size=self.label.font_size
            )

            new_label.move_to(new_dot.label)
            new_dot.remove(new_dot.label)
            new_dot.label = new_label
            new_dot.add(new_label)

        return new_dot
