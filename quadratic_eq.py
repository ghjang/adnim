from manim import *


class QuadraticFormulaDerivation(Scene):
    def construct(self):
        steps = [
            {
                "explanation": {
                    "text": "이차방정식의 표준형",
                    "render": True,
                },
                "equation": "{{ax^2 + bx}} {{+ c}} {{= 0}}",
            },
            {
                "explanation": "c항을 우변으로 이항",
                "equation": "{{ax^2 + bx}} {{= -c}}",
            },
            {
                "explanation": "양변을 a로 나누기",
                "equation": "{{x^2 + \\frac{b}{a}x}} {{= -\\frac{c}{a}}}",
            },
            {
                "explanation": {
                    "text": "좌변 x항 계수의 절반의 제곱을 양변에 더하기",
                    "render": True,
                },
                "equation": "{{x^2 + \\frac{b}{a}x}} + \\left(\\dfrac{\\frac{b}{a}}{2}\\right)^2 = \\left(\\dfrac{\\frac{b}{a}}{2}\\right)^2 {{- \\frac{c}{a}}}",
            },
            {
                "explanation": "양변 정리",
                "equation": "{{x^2 + \\frac{b}{a}x}} {{+ \\left(\\frac{b}{2a}\\right)^2}} {{= \\left(\\frac{b}{2a}\\right)^2 - \\frac{c}{a}}}",
            },
            {
                "explanation": {
                    "text": "좌변의 x항 표현을 완전제곱식으로 정리하기 위해서 변형",
                    "render": True,
                },
                "equation": "{{x^2}} {{+ 2 \\cdot x \\cdot \\frac{b}{2a}}} {{+ \\left(\\frac{b}{2a}\\right)^2}} {{= \\left(\\frac{b}{2a}\\right)^2 - \\frac{c}{a}}}",
            },
        ]

        # 수식 크기 조절 상수
        EQUATION_SCALE = 1.2
        # 설명 텍스트 크기 조절 상수
        TEXT_SCALE = 1.2

        # 초기 방정식 표시
        current_eq = MathTex(steps[0]["equation"]).scale(EQUATION_SCALE)
        current_exp = None
        if isinstance(steps[0]["explanation"], dict) and steps[0]["explanation"].get(
            "render"
        ):
            current_exp = Text(
                steps[0]["explanation"]["text"], font_size=24 * TEXT_SCALE
            ).next_to(current_eq, DOWN, buff=LARGE_BUFF)
            self.play(Write(current_eq), Write(current_exp))
        else:
            self.play(Write(current_eq))

        # 각 단계별로 방정식 변형 (첫 번째 단계부터 시작)
        for step in steps:
            new_eq = MathTex(step["equation"]).scale(EQUATION_SCALE)
            new_exp = None
            if isinstance(step["explanation"], dict) and step["explanation"].get(
                "render"
            ):
                new_exp = Text(
                    step["explanation"]["text"], font_size=24 * TEXT_SCALE
                ).next_to(new_eq, DOWN, buff=LARGE_BUFF)
                if current_exp:
                    self.play(
                        Transform(current_eq, new_eq), Transform(current_exp, new_exp)
                    )
                else:
                    self.play(Transform(current_eq, new_eq), FadeIn(new_exp))
                    current_exp = new_exp
            else:
                if current_exp:
                    self.play(Transform(current_eq, new_eq), FadeOut(current_exp))
                    current_exp = None
                else:
                    self.play(Transform(current_eq, new_eq))

            # 첫 번째 요소가 아닐 경우에만 wait 실행
            if step != steps[0]:
                self.wait(2)

        # 최종 공식 강조 (이미 크기가 조절되어 있으므로 추가 확대는 하지 않음)
        self.play(current_eq.animate.set_color(GREEN).scale(1.5))
        if current_exp:
            self.play(FadeOut(current_exp))
        self.wait(3)
