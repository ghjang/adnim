from manim import *

class FunctionMapping(Scene):
    def construct(self):
        # 부분 타원 생성 (위쪽이 열린 형태)
        domain = Arc(
            radius=1.5,
            start_angle=110 * DEGREES,
            angle=320 * DEGREES,
            color=BLUE
        ).stretch(2.0, 1).stretch(1.2, 0).shift(LEFT*3)
        
        codomain = Arc(
            radius=1.5,
            start_angle=110 * DEGREES,
            angle=320 * DEGREES,
            color=RED
        ).stretch(2.0, 1).stretch(1.2, 0).shift(RIGHT*3)
        
        # 집합 이름 위치 수정 - 호의 상단 중앙에 배치
        x_label = Text("X", color=BLUE).move_to(
            domain.get_center() + UP*3  # 호의 상단 위치로 조정
        )
        y_label = Text("Y", color=RED).move_to(
            codomain.get_center() + UP*3
        )
        
        # 도메인 원소 레이블 위치 조정 - 수직 간격 증가
        d1 = Text("1").move_to(domain.get_center() + UP*1.2)    # 0.7 -> 1.2
        d2 = Text("2").move_to(domain.get_center())
        d3 = Text("3").move_to(domain.get_center() + DOWN*1.2)  # 0.7 -> 1.2
        
        # 코도메인 원소 레이블 위치 조정 - 수직 간격 증가
        c1 = Text("a").move_to(codomain.get_center() + UP*0.8)  # 0.5 -> 0.8
        c2 = Text("b").move_to(codomain.get_center() + DOWN*0.8)  # 0.5 -> 0.8
        
        # 대응 화살표 - 날렵한 화살촉으로 통일
        arrow1 = Arrow(
            d1.get_right(), c1.get_left(),
            buff=0.1,
            max_tip_length_to_length_ratio=0.025,  # 화살촉 크기 비율
            max_stroke_width_to_length_ratio=1,   # 선 굵기 비율
            stroke_width=2                        # 선 두께
        )
        arrow2 = Arrow(
            d2.get_right(), c2.get_left(),
            buff=0.1,
            max_tip_length_to_length_ratio=0.025,
            max_stroke_width_to_length_ratio=1,
            stroke_width=2
        )
        arrow3 = Arrow(
            d3.get_right(), c2.get_left(),
            buff=0.1,
            max_tip_length_to_length_ratio=0.025,
            max_stroke_width_to_length_ratio=1,
            stroke_width=2
        )
        
        # 애니메이션 수정 - 화살표 순차 생성
        self.play(Create(domain), Create(codomain))
        self.play(Write(x_label), Write(y_label))
        self.play(Write(VGroup(d1, d2, d3)), Write(VGroup(c1, c2)))
        # 화살표 순차적으로 생성
        self.play(Create(arrow1))
        self.play(Create(arrow2))
        self.play(Create(arrow3))
        self.wait(2)


class EllipticalArc(Scene):
    def construct(self):
        # 위가 열린 타원형 호 생성
        arc = Arc(
            radius=1.5,          # radius 줄임
            start_angle=110 * DEGREES,
            angle=320 * DEGREES,
            color=BLUE
        )
        
        # stretch 비율 조정
        arc.stretch(2.0, 1)      # 수직방향 2.0배로 줄임
        arc.stretch(1.2, 0)      # 수평방향 1.2배로 줄임
        
        # 씬에 추가
        self.play(Create(arc))
        self.wait()
