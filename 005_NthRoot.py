from manim import *


class NthRootByBisection(Scene):
    def construct(self):
        NUMBER_LINE_Y = DOWN

        # 타이틀과 범위를 하나의 그룹으로 처리
        title = MathTex(
            r"\text{Finding }\sqrt[12]{2}\text{ using Bisection Method}", font_size=60)
        title.to_edge(UP)
        range_text = MathTex(r"1 < \sqrt[12]{2} < 2", font_size=56, color=GREEN)
        range_text.next_to(title, DOWN, buff=1)
        title_group = VGroup(title, range_text)
        # 타이틀과 범위 텍스트 애니메이션 분리
        self.play(FadeIn(title, shift=UP*0.3))
        self.play(FadeIn(range_text, shift=UP*0.3))

        # 이터레이션 카운트 텍스트 초기화 (range_text 다음에 추가)
        iteration_counter = MathTex(r"\text{Iteration: } 1", font_size=56, color=BLUE)
        iteration_counter.move_to(range_text)

        # 초기 구간 설정
        left, right = 1, 2
        iterations = 10

        # 초기 위치 설정을 위한 상수
        SCALE_FACTOR = 3
        NUMBER_LINE_Y = [0, -1.5, 0]  # -2에서 -1.5로 변경

        # 초기 넘버라인 설정
        initial_numberline = NumberLine(
            x_range=[0.9, 2.1, 0.1],
            length=10,
            include_numbers=False,
            include_ticks=True
        ).move_to([0, -0.4, 0])
        self.play(FadeIn(initial_numberline))
        curr_number_line = initial_numberline

        # 이전 버라인을 저장할 추가
        prev_number_line = None

        # 이분법 반복
        for i in range(iterations):
            mid = (left + right) / 2
            interval_size = right - left

            # 새로운 number line 생성 및 중앙 배치
            new_number_line = NumberLine(
                x_range=[
                    left - interval_size * 0.1,  # 여유 공간 10%
                    right + interval_size * 0.1,
                    interval_size / 20  # 구간을 20등분하는 눈금
                ],
                length=10,
                include_numbers=False,  # 숫자 제거
                include_ticks=True
            )

            # 현재 구간 표시
            interval = Line(
                new_number_line.number_to_point(left),
                new_number_line.number_to_point(right),
                color="#607D8B"
            )

            # 좌우 경계점과 중점 표시 (반지름 더 축소)
            left_point = Dot(
                new_number_line.number_to_point(left),
                color=GREEN_E,
                radius=0.06  # 0.08에서 0.06으로 축소
            )

            right_point = Dot(
                new_number_line.number_to_point(right),
                color=GREEN_E,
                radius=0.06
            )

            # 중점 표시
            midpoint = Dot(
                new_number_line.number_to_point(mid),
                color=RED_E,
                radius=0.06
            )

            # 화살표와 텍스트 생성 부분 수정
            arrow_config = {
                "buff": 0.2,
                "stroke_width": 6,
                "max_tip_length_to_length_ratio": 0.5,
                "tip_length": 0.25
            }

            # 화살표 크기 설정 수정
            arrow_scale = 4.0
            y_offset = 0.2

            left_arrow = Arrow(
                new_number_line.number_to_point(
                    left) + DOWN * (1.6 - y_offset),  # 1.8에서 1.6으로 수정
                new_number_line.number_to_point(
                    left) + DOWN * (0.8 - y_offset),  # 1.0에서 0.8으로 수정
                color=GREEN_E,
                **arrow_config
            ).scale(arrow_scale)

            right_arrow = Arrow(
                new_number_line.number_to_point(
                    right) + DOWN * (1.6 - y_offset),
                new_number_line.number_to_point(
                    right) + DOWN * (0.8 - y_offset),
                color=GREEN_E,
                **arrow_config
            ).scale(arrow_scale)

            # 중점 화살표
            mid_arrow = Arrow(
                new_number_line.number_to_point(mid) + DOWN * (1.6 - y_offset),
                new_number_line.number_to_point(mid) + DOWN * (0.8 - y_offset),
                color=RED_E,
                **arrow_config
            ).scale(arrow_scale)

            # 불필요한 0을 제거하는 헬퍼 함수 추가
            def format_number(num, precision=5, truncate=False):
                if truncate:
                    factor = 10 ** precision
                    num = int(num * factor) / factor
                # 소수점 precision자리까지 문자열로 변환
                str_num = f"{num:.{precision}f}"
                # 소수점이 있는 경우
                if '.' in str_num:
                    # 뒤의 불필요한 0 제거
                    str_num = str_num.rstrip('0')
                    # 소수점만 남은 경우 제거
                    if str_num.endswith('.'):
                        str_num = str_num[:-1]
                return str_num

            # 텍스트 생성 부분 수정
            left_text = MathTex(format_number(
                left), color=GREEN_E, font_size=36)
            right_text = MathTex(format_number(
                right), color=GREEN_E, font_size=36)
            mid_text = MathTex(format_number(mid), color=RED_E, font_size=36)

            left_text.next_to(left_arrow, DOWN, buff=0.1)
            right_text.next_to(right_arrow, DOWN, buff=0.1)
            mid_text.next_to(mid_arrow, DOWN, buff=0.1)

            # 새로운 넘버라인 위치 정 (화면 중앙에서 시작)
            new_number_line.move_to([0, 0, 0])

            # 구간 표시 위치 조정
            interval.move_to(new_number_line)

            # 중점 관련 요소들은 처음에 투명하게 설정
            mid_arrow.set_opacity(0)
            mid_text.set_opacity(0)

            # 그룹화 (원래 위치에서 시작)
            new_group = VGroup(
                new_number_line, interval,
                left_point, right_point,
                left_arrow, right_arrow,
                left_text, right_text,
                mid_arrow, mid_text
            ).move_to([0, 0, 0])

            new_group.scale(1/SCALE_FACTOR)

            # 넘버라인 애니메이션 수정 (확대 후 위치도 NUMBER_LINE_Y[1]로 변경)
            if i > 0:
                # 이터레이션 카운트 업데이트
                new_counter = MathTex(f"\\text{{Iteration: }} {i+1}", font_size=56, color=BLUE)
                new_counter.move_to(iteration_counter)
                self.play(Transform(iteration_counter, new_counter))
                
                # 선택 구간에 따라 초기 위치 설정
                if mid_value > 2:
                    initial_shift = LEFT * 4
                else:
                    initial_shift = RIGHT * 4

                # 기존 애니메이션 계속
                new_group.shift(initial_shift)

                self.play(
                    AnimationGroup(
                        curr_number_line.animate.scale(
                            SCALE_FACTOR).set_opacity(0),
                        Animation(Mobject(), run_time=0.8),
                        new_group.animate.scale(SCALE_FACTOR).move_to(
                            [0, NUMBER_LINE_Y[1], 0]),
                        lag_ratio=0.07
                    ),
                    run_time=1.2
                )
                self.remove(curr_number_line)
            else:
                self.play(
                    AnimationGroup(
                        initial_numberline.animate.scale(
                            SCALE_FACTOR).set_opacity(0),
                        Animation(Mobject(), run_time=0.8),
                        new_group.animate.scale(SCALE_FACTOR).move_to(
                            [0, NUMBER_LINE_Y[1], 0]),
                        lag_ratio=0.07
                    ),
                    run_time=1.2
                )
                self.remove(initial_numberline)
                # range_text를 iteration_counter로 트랜스폼
                self.play(Transform(range_text, iteration_counter))
                iteration_counter = range_text  # 이후 업데이트를 위해 참조 변경

            # 현재 넘버라인 업데이트
            curr_number_line = new_number_line

            # 중점을 노란선 위에 정확히 배치하고 표시
            midpoint_pos = new_number_line.number_to_point(mid)
            midpoint.move_to(midpoint_pos)
            self.add(midpoint)

            # 중점 관련 요소들을 불투명하게 변경
            self.play(
                mid_arrow.animate.set_opacity(1),
                mid_text.animate.set_opacity(1)
            )

            # 중간값 계산 결과
            mid_value = mid ** 12
            
            # 중간값 계산 결과 표시 (텍스트 추가)
            power_calc = MathTex(
                f"({format_number(mid)})^{{12}} = {format_number(mid_value)}", 
                font_size=36,
                color=RED if mid_value > 2 else GREEN
            )
            comparison = MathTex(
                r">2" if mid_value > 2 else r"\leq 2",
                font_size=36,
                color=RED if mid_value > 2 else GREEN
            )
            
            power_calc.next_to(iteration_counter, DOWN, buff=0.5)
            comparison.next_to(power_calc, RIGHT, buff=0.2)
            
            self.play(
                FadeIn(power_calc),
                FadeIn(comparison)
            )

            # X 표시 생성
            if mid_value > 2:
                right = mid
                cross = Text("×", color=RED_E, font_size=120)
                cross.move_to(right_text)
                # 다음 구간 하이라이트 라인 생성
                highlight_line = Line(
                    new_number_line.number_to_point(left),
                    new_number_line.number_to_point(mid),
                    color=YELLOW,
                    stroke_width=8
                )
            else:
                left = mid
                cross = Text("×", color=RED_E, font_size=120)
                cross.move_to(left_text)
                # 다음 구간 하이라이트 라인 생성
                highlight_line = Line(
                    new_number_line.number_to_point(mid),
                    new_number_line.number_to_point(right),
                    color=YELLOW,
                    stroke_width=8
                )

            # X 표시 추가
            self.add(cross)

            # 하이라이트 라인 표시
            self.bring_to_back(highlight_line)
            self.play(FadeIn(highlight_line))

            # 선택되지 않은 요소들 제거
            if mid_value > 2:
                self.play(
                    FadeOut(right_point),
                    FadeOut(right_arrow),
                    FadeOut(right_text),
                    FadeOut(cross)
                )
            else:
                self.play(
                    FadeOut(left_point),
                    FadeOut(left_arrow),
                    FadeOut(left_text),
                    FadeOut(cross)
                )

            # 계산 결과 텍스트 페이드아웃
            self.play(
                FadeOut(power_calc),
                FadeOut(comparison)
            )

            # 잠시 대기
            self.wait(0.5)

            # 현재 화면의 선택된 요소들을 하나의 그룹으로 묶기
            if mid_value > 2:
                fade_group = VGroup(
                    curr_number_line,
                    interval, highlight_line,
                    left_point, left_arrow, left_text,
                    midpoint, mid_arrow, mid_text
                )
            else:
                fade_group = VGroup(
                    curr_number_line,
                    interval, highlight_line,
                    right_point, right_arrow, right_text,
                    midpoint, mid_arrow, mid_text
                )

            # 현재 위치와 목표 위치
            start_y = fade_group.get_center()[1]
            target_y = NUMBER_LINE_Y[1]

            # 기존 요소들이 확대되며 동시에 아래로 이동하는 애니메이션
            if mid_value > 2:
                shift_direction = RIGHT
            else:
                shift_direction = LEFT

            if i < iterations - 1:
                self.play(
                    fade_group.animate.scale(SCALE_FACTOR).shift(
                        DOWN * 2 + shift_direction * 7).set_opacity(0),
                    run_time=1.2
                )
                # 이전 요소들 제거
                self.remove(fade_group)
            else:
                # 마지막 이터레이션에서는 넘버라인을 확대하면서 사라지게 하지 않음
                result_value = format_number(mid, precision=3, truncate=True)
                result = MathTex(r"\sqrt[12]{2} \approx " + result_value, color=RED_E, font_size=56)
                result.move_to(ORIGIN)  # 결과 텍스트를 화면 중앙에 배치
                
                # 소수점 아래 3자리까지 수렴했다는 메시지 추가
                convergence_message = Text("The value has converged to 3 decimal places.", font_size=36, color=BLUE)
                convergence_message.next_to(result, DOWN, buff=0.5)
                
                mid_text_copy = mid_text.copy()  # mid_text의 사본 생성
                self.play(
                    AnimationGroup(
                        Transform(mid_text_copy, result),
                        FadeOut(fade_group),
                        lag_ratio=0.0
                    ),
                    run_time=1.2
                )
                self.play(FadeIn(convergence_message))

            # 현재 넘버라인 업데이트
            curr_number_line = new_number_line

        self.wait(2)
