from manim import *
import numpy as np


class SieveOfEratosthenes1(Scene):
    def construct(self):
        # 상수 정의
        TEXT_SIZE = 12

        # 먼저 가장 큰 숫자(100)의 크기를 측정하여 컨테이너 크기 결정
        reference_text = Text("100", font_size=TEXT_SIZE)
        container_width = reference_text.width + 0.08  # 여백 추가
        container_height = reference_text.height + 0.08  # 여백 추가

        # 100개의 숫자들을 담을 VGroup 생성
        numbers = VGroup()

        # 100개의 숫자 생성
        for i in range(100):
            # 숫자 텍스트 생성
            num_text = Text(str(i + 1), font_size=TEXT_SIZE)
            num_text.set_color(YELLOW_A)

            # 숫자를 담을 고정 너비의 컨테이너 생성
            container = Rectangle(
                width=container_width,
                height=container_height,
                fill_opacity=0,
                stroke_opacity=1,
                stroke_color=BLUE,
                stroke_width=1,
            )

            # 숫자를 컨테이 중앙 배치
            num_text.move_to(container.get_center())

            # 컨테이너와 숫자를 그룹으로 묶기
            num_group = VGroup(container, num_text)
            numbers.add(num_group)

        # 숫자들을 2x50 그리드로 배치
        numbers.arrange_in_grid(
            rows=2,
            cols=50,
            buff_x=0,
            buff_y=0.015,
            cell_alignment=np.array([0, 0, 0]),
            aligned_edge=LEFT,
        )

        # 전체 그룹을 화면 너비에 맞추기
        numbers.stretch_to_fit_width(config.frame_width - 0.5)

        # 화면 상단에 배치
        numbers.to_edge(UP, buff=0.15)

        # 초기 애니메이션
        self.play(FadeIn(numbers, shift=UP), run_time=1)

        # 숫자 1에 대한 처리
        number_1 = numbers[0]

        # Cross 객체 생성
        cross = Cross(number_1, stroke_color=RED, stroke_width=2)

        # Cross 애니메이션
        self.play(Create(cross), run_time=0.5)
        self.wait(0.5)  # 잠시 대기

        # 숫자 1과 X 표시 함께 페이드아웃
        self.play(FadeOut(number_1), FadeOut(cross), run_time=0.5)

        # "Filter of 2" 텍스트 생성 - 볼드체와 색상 적용
        filter_text = Text("Filter of 2", font_size=18, weight=BOLD).set_color(GREEN_B)

        # 필 사형들을 담을 VGroup 생성
        filter_squares = VGroup()

        # 99개의 패턴 생성 (2부터 100까지, 채워진 사각형과 빈 사각형 번갈아가며)
        rect_width = container_width
        rect_height = container_height * 0.4
        for i in range(99):  # 100개에서 99개로 변경
            rect = Rectangle(
                width=rect_width,
                height=rect_height,
                stroke_color=BLUE,
                stroke_width=1,
            )
            # i가 짝수일 때 채우기 (i=0은 숫자 2에 해당)
            if i % 2 == 0:
                rect.set_fill(BLUE_D, opacity=1)
            else:
                rect.set_stroke(color=GREY_B, opacity=0.4)  # 테두리를 회색으로 변경
                rect.set_fill(GREY_C, opacity=0.2)  # 회색 계열로 채우기, 투명도 증가

            filter_squares.add(rect)

        # 사각형들을 일정한 간격으로 배열 (간격 없이)
        filter_squares.arrange(RIGHT, buff=0)

        # 필 라인 전체를 화면 너비에 맞추기 (여백 최소화)
        target_width = config.frame_width - 0.4
        filter_squares.stretch_to_fit_width(target_width)

        # 필터 라인을 화면 중앙에 맞추고 위치 조정
        filter_squares.move_to(ORIGIN).shift(UP * (config.frame_height / 4))

        # 텍스트를 필터 인 쪽 위에 배치
        filter_text.next_to(filter_squares, UP, buff=0.2)
        filter_text.align_to(filter_squares, LEFT)

        # 필터 텍스트와 사각형들 애니메이션
        self.play(Write(filter_text), run_time=0.5)
        self.play(
            LaggedStart(
                *[FadeIn(rect, shift=UP * 0.2) for rect in filter_squares],
                lag_ratio=0.05
            ),
            run_time=1.5,
        )

        self.wait(0.5)

        # 텍스트만 페이드아웃
        self.play(FadeOut(filter_text), run_time=0.5)

        # 짝수들을 필터로 이동시키는 애니메이션
        moves = []
        for i in range(1, 101):  # 2부터 100까지
            if i % 2 == 0:  # 짝수인 경우
                number = numbers[i - 1]  # 인덱스는 0부터 시작하므로 1을 빼줌
                # 필터에서의 대응되는 위치 계산
                filter_rect = filter_squares[i - 2]  # 1을 제외했으므로 2를 빼줌

                # 필터 사각형의 상단 중앙 위치 계산
                target_pos = filter_rect.get_top() + UP * 0.1  # 필터 상단에서 약간 위로

                # 이동 애니메이션 추가
                moves.append(number.animate.move_to(target_pos))

        # 모든 짝수를 동시에 이동
        self.play(*moves, run_time=1.5)

        self.wait(0.5)

        # 남은 홀수들을 필터의 빈 사각형 위치에 맞춰 상단에 재배치
        moves = []
        for i in range(3, 101, 2):  # 3부터 시작하는 홀수들만
            number = numbers[i - 1]  # 인덱스는 0부터 시작하므로 1을 빼줌

            # 필터에서의 대응되는 빈 사각형 위치 찾기
            filter_rect = filter_squares[i - 2]  # 1을 제외했으므로 2를 빼줌

            # 상단 두 번째 줄의 y좌표 찾기 (51번째 숫자의 y좌표 사용)
            second_row_y = numbers[50].get_center()[1]

            # 상단에 배치하되 x좌표는 필터의 빈 사각형과 맞춤
            target_pos = np.array(
                [
                    filter_rect.get_center()[0],  # x좌표는 필터의 빈 사각형 위치
                    second_row_y,  # y좌표는 두 번째 줄의 높이로
                    0,
                ]
            )

            # 이동 애니메이션 추가
            moves.append(number.animate.move_to(target_pos))

        # 홀수들 재배 애니메이션
        self.play(*moves, run_time=1.5)

        self.wait(0.5)

        # "Filter of 3" 텍스트 생성 - 볼드체와 색상 적용
        filter3_text = Text("Filter of 3", font_size=18, weight=BOLD).set_color(GREEN_B)

        # 2의 필터 아래에 텍스트 배치
        filter3_text.next_to(filter_squares, DOWN, buff=0.5)
        filter3_text.align_to(filter_squares, LEFT)

        # 텍스트 애니메이션
        self.play(Write(filter3_text), run_time=0.5)

        # 3의 필터 사각형들을 담을 VGroup 생성
        filter3_squares = VGroup()

        # 99개의 패턴 생성 (3의 배수 위치만 채우기)
        for i in range(99):  # 1을 제외한 2부터 100까지
            rect = Rectangle(
                width=rect_width,
                height=rect_height,
                stroke_color=BLUE,
                stroke_width=1,
            )
            # (i+2)가 3의 배수일 때 채우기 (i+2는 실제 숫자)
            if (i + 2) % 3 == 0:
                rect.set_fill(BLUE_D, opacity=1)
            else:
                rect.set_stroke(color=GREY_B, opacity=0.4)  # 테두리를 회색으로 변경
                rect.set_fill(GREY_C, opacity=0.2)  # 회색 계열로 채우기, 투도 증가

            filter3_squares.add(rect)

        # 사각형들을 일정한 간격으로 배열 (간격 없이)
        filter3_squares.arrange(RIGHT, buff=0)

        # 필터 라인 전체를 화면 너비에 맞추기
        filter3_squares.stretch_to_fit_width(target_width)

        # 3의 필터를 텍스트 아래에 배치
        filter3_squares.next_to(filter3_text, DOWN, buff=0.2)
        filter3_squares.align_to(filter_squares, LEFT)  # 2의 필터와 왼쪽 정렬 맞추기

        # 3의 필터 사각형들 애니메이션
        self.play(
            LaggedStart(
                *[FadeIn(rect, shift=UP * 0.2) for rect in filter3_squares],
                lag_ratio=0.05
            ),
            run_time=1.5,
        )

        self.wait(0.5)  # 잠시 대기

        # "Filter of 3" 텍스트 페이드아웃
        self.play(FadeOut(filter3_text), run_time=0.5)

        # 홀수들에서 3의 필터로 화살표 그리기
        arrows = VGroup()
        for i in range(3, 101, 2):  # 3부터 시작하는 홀수들
            number = numbers[i - 1]
            filter3_rect = filter3_squares[i - 2]  # 1을 제외했으므로 2를 빼줌

            # 화살표 시작점 (홀수 테이너의 하 중앙)
            start_point = number[0].get_bottom()  # number[0]은 컨테이너

            # 화살표 끝점 (3의 필터 사각형의 상단 중앙)
            end_point = filter3_rect.get_top()

            # 화살표 생성
            arrow = Arrow(
                start=start_point,
                end=end_point,
                buff=0,  # 시작점과 끝점에 여백 없음
                stroke_width=1,
                color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                tip_length=0.1,
                max_tip_length_to_length_ratio=0.3,
            )

            arrows.add(arrow)

        # 화살표들 동시에 그리기 애니메이션
        self.play(*[GrowArrow(arrow) for arrow in arrows], run_time=0.8)

        self.wait(0.5)

        # 3의 배수 이동 및 화살표 축소 애니메이션
        moves = []
        arrow_shrinks = []
        arrows_to_fade = []

        # 홀수 인덱스 핑을 위한 딕셔너리 생성
        arrow_indices = {num: idx for idx, num in enumerate(range(3, 101, 2))}

        for i in range(3, 101, 2):  # 홀수들 중에서
            if i % 3 == 0:  # 3의 배수인 경우
                number = numbers[i - 1]
                filter3_rect = filter3_squares[i - 2]
                arrow = arrows[arrow_indices[i]]

                # 이동할 위치 계산 (필터 사각형 상단 약간 위)
                target_pos = filter3_rect.get_top() + UP * 0.1

                # 숫자 이동 애니메이션
                moves.append(number.animate.move_to(target_pos))

                # 화살표 축소 애니메이션 (시작점을 끝점으로 변경)
                new_arrow = Arrow(
                    start=target_pos + DOWN * 0.1,  # 이동하는 숫자의 밑변에 맞춤
                    end=target_pos + DOWN * 0.1,  # 같은 위치로 설정하여 라지게 함
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )
                arrow_shrinks.append(Transform(arrow, new_arrow))
                arrows_to_fade.append(arrow)

        # 3의 배수 이동과 화살표 축소 동시 애니메이션
        self.play(*moves, *arrow_shrinks, run_time=1.0)

        # 해당 화살표들 페이드아웃
        # self.play(
        #     *[FadeOut(arrow) for arrow in arrows_to_fade],
        #     run_time=0.3
        # )

        self.wait(0.5)

        # "Filter of 5" 텍스트 생성 - 볼드체와 색상 적용
        filter5_text = Text("Filter of 5", font_size=18, weight=BOLD).set_color(GREEN_B)

        # 3의 필터 아래에 텍스트 배치
        filter5_text.next_to(filter3_squares, DOWN, buff=0.5)
        filter5_text.align_to(filter3_squares, LEFT)

        # 텍스트 애니메이션
        self.play(Write(filter5_text), run_time=0.5)

        # 5의 필터 사각형들을 담을 VGroup 생성
        filter5_squares = VGroup()

        # 99개의 패턴 생성 (5의 배수 위치만 채우기)
        for i in range(99):  # 1을 제외한 2부터 100까지
            rect = Rectangle(
                width=rect_width,
                height=rect_height,
                stroke_color=BLUE,
                stroke_width=1,
            )
            # (i+2)가 5의 배수일 때 채우기
            if (i + 2) % 5 == 0:
                rect.set_fill(BLUE_D, opacity=1)
            else:
                rect.set_stroke(color=GREY_B, opacity=0.4)
                rect.set_fill(GREY_C, opacity=0.2)

            filter5_squares.add(rect)

        # 사각형들을 일정한 간격으로 배열
        filter5_squares.arrange(RIGHT, buff=0)
        filter5_squares.stretch_to_fit_width(target_width)

        # 5의 필터를 텍스트 아래에 배치
        filter5_squares.next_to(filter5_text, DOWN, buff=0.2)
        filter5_squares.align_to(filter3_squares, LEFT)

        # 5의 필터 사각형들 애니메이션
        self.play(
            LaggedStart(
                *[FadeIn(rect, shift=UP * 0.2) for rect in filter5_squares],
                lag_ratio=0.05
            ),
            run_time=1.5,
        )

        self.wait(0.5)

        # "Filter of 5" 텍스트 페이드아웃
        self.play(FadeOut(filter5_text), run_time=0.5)

        # 기존 화살표들을 5의 필터까지 연장
        arrow_extensions = []
        for i in range(3, 101, 2):  # 홀수들 중에서
            if i % 3 != 0:  # 3의 배수가 아닌 것들만
                number = numbers[i - 1]
                filter5_rect = filter5_squares[i - 2]
                arrow = arrows[arrow_indices[i]]  # 기존 화살표

                # 화살표 연장 애니메이션 (시작점은 유지, 끝점만 변경)
                extended_arrow = Arrow(
                    start=arrow.get_start(),  # 기존 시작점 유지
                    end=filter5_rect.get_top(),  # 5의 필터까지
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )

                # Transform을 사용하여 기존 화살표를 연장
                arrow_extensions.append(Transform(arrow, extended_arrow))

        # 화살표 연장 애니메이션
        self.play(*arrow_extensions, run_time=0.8)

        self.wait(0.5)

        # 5의 배수 이동 및 화살표 축소 애니메이션
        moves = []
        arrow_shrinks = []
        arrows_to_fade = []

        for i in range(3, 101, 2):  # 홀수들 중에서
            if i % 3 != 0 and i % 5 == 0:  # 3의 배수가 아니면서 5의 배수인 경우
                number = numbers[i - 1]
                filter5_rect = filter5_squares[i - 2]
                arrow = arrows[arrow_indices[i]]

                # 이동할 위치 계산
                target_pos = filter5_rect.get_top() + UP * 0.1

                # 숫자 이동 애니메이션
                moves.append(number.animate.move_to(target_pos))

                # 화살표 축소 애니메이션
                new_arrow = Arrow(
                    start=target_pos + DOWN * 0.1,
                    end=target_pos + DOWN * 0.1,
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )
                arrow_shrinks.append(Transform(arrow, new_arrow))
                arrows_to_fade.append(arrow)

        # 5의 배수 이동과 화살표 축소 동시 애니메이션
        self.play(*moves, *arrow_shrinks, run_time=1.0)

        # 해당 화살표들 페이드아웃
        self.play(*[FadeOut(arrow) for arrow in arrows_to_fade], run_time=0.3)

        self.wait(1)

        # "Filter of 7" 텍스트 생성 - 볼드체와 색상 적용
        filter7_text = Text("Filter of 7", font_size=18, weight=BOLD).set_color(GREEN_B)

        # 5의 필터 아래에 텍스트 배치
        filter7_text.next_to(filter5_squares, DOWN, buff=0.5)
        filter7_text.align_to(filter5_squares, LEFT)

        # 텍스트 애니메이션
        self.play(Write(filter7_text), run_time=0.5)

        # 7의 필터 사각형들을 담을 VGroup 생성
        filter7_squares = VGroup()

        # 99개의 패턴 생성 (7의 배수 위치만 채우기)
        for i in range(99):  # 1을 제외한 2부터 100까지
            rect = Rectangle(
                width=rect_width,
                height=rect_height,
                stroke_color=BLUE,
                stroke_width=1,
            )
            # (i+2) 7의 배수일 때 채우기
            if (i + 2) % 7 == 0:
                rect.set_fill(BLUE_D, opacity=1)
            else:
                rect.set_stroke(color=GREY_B, opacity=0.4)
                rect.set_fill(GREY_C, opacity=0.2)

            filter7_squares.add(rect)

        # 사각형들을 일정한 간격으로 배열
        filter7_squares.arrange(RIGHT, buff=0)
        filter7_squares.stretch_to_fit_width(target_width)

        # 7의 필터를 텍스트 아래에 배치
        filter7_squares.next_to(filter7_text, DOWN, buff=0.2)
        filter7_squares.align_to(filter5_squares, LEFT)

        # 7의 필터 사각형들 애니메이션
        self.play(
            LaggedStart(
                *[FadeIn(rect, shift=UP * 0.2) for rect in filter7_squares],
                lag_ratio=0.05
            ),
            run_time=1.5,
        )

        self.wait(0.5)

        # "Filter of 7" 텍스트 페이드아웃
        self.play(FadeOut(filter7_text), run_time=0.5)

        # 기존 화살표들을 7의 필터까지 연장
        arrow_extensions = []
        for i in range(3, 101, 2):  # 홀수들 중에서
            if i % 3 != 0 and i % 5 != 0:  # 3과 5의 배수가 아닌 것들만
                number = numbers[i - 1]
                filter7_rect = filter7_squares[i - 2]
                arrow = arrows[arrow_indices[i]]  # 기존 화살표

                # 화살표 연장 애니메이션 (시작점은 유지, 끝점만 경)
                extended_arrow = Arrow(
                    start=arrow.get_start(),  # 기존 시작점 유지
                    end=filter7_rect.get_top(),  # 7의 필터까지
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )

                # Transform을 사용하여 기존 화살표를 연장
                arrow_extensions.append(Transform(arrow, extended_arrow))

        # 화살표 연장 애니메이션
        self.play(*arrow_extensions, run_time=0.8)

        self.wait(0.5)

        # 7의 배수 이동 및 화살표 축소 애니메이션
        moves = []
        arrow_shrinks = []
        arrows_to_fade = []

        for i in range(3, 101, 2):  # 홀수들 중에서
            if (
                i % 3 != 0 and i % 5 != 0 and i % 7 == 0
            ):  # 3과 5의 배수가 아니면서 7의 배수인 경우
                number = numbers[i - 1]
                filter7_rect = filter7_squares[i - 2]
                arrow = arrows[arrow_indices[i]]

                # 이동할 위치 계산
                target_pos = filter7_rect.get_top() + UP * 0.1

                # 숫자 이동 애니메이션
                moves.append(number.animate.move_to(target_pos))

                # 화살표 축소 애니메이션
                new_arrow = Arrow(
                    start=target_pos + DOWN * 0.1,
                    end=target_pos + DOWN * 0.1,
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )
                arrow_shrinks.append(Transform(arrow, new_arrow))
                arrows_to_fade.append(arrow)

        # 7의 배수 이동과 살표 축소 동시 애니메이션
        self.play(*moves, *arrow_shrinks, run_time=1.0)

        # 해당 화살표들 페이드아웃
        self.play(*[FadeOut(arrow) for arrow in arrows_to_fade], run_time=0.3)

        self.wait(1)

        # 소수들의 최종 위치 계산 (7의 필터 아래)
        final_y = filter7_squares.get_bottom()[1] - 1.5

        # 기존 화살표들을 최종 위치까지 연장
        arrow_extensions = []
        moves = []
        arrow_shrinks = []
        arrows_to_fade = []

        # 남은 소수들(3,5,7의 배수가 아닌 수들)에 대한 화살표 연장 및 이동
        for i in range(3, 101, 2):
            if i % 3 != 0 and i % 5 != 0 and i % 7 != 0:
                number = numbers[i - 1]
                arrow = arrows[arrow_indices[i]]

                # 최종 위치 계산 (재 x좌표 유지, y좌표만 변경)
                target_pos = np.array([number.get_center()[0], final_y, 0])

                # 화살표 연장
                extended_arrow = Arrow(
                    start=arrow.get_start(),
                    end=target_pos + DOWN * 0.1,
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )
                arrow_extensions.append(Transform(arrow, extended_arrow))

                # 숫자 이동
                moves.append(number.animate.move_to(target_pos))

                # 화살표 축소 준비
                shrunk_arrow = Arrow(
                    start=target_pos + DOWN * 0.1,
                    end=target_pos + DOWN * 0.1,
                    buff=0,
                    stroke_width=1,
                    color=GOLD_C,  # TEAL_B에서 GOLD_C로 변경
                    tip_length=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )
                arrow_shrinks.append(Transform(arrow, shrunk_arrow))
                arrows_to_fade.append(arrow)

        # 화살표 연장 애니메이션
        self.play(*arrow_extensions, run_time=0.8)

        self.wait(0.5)

        # 소수들 이동과 화살표 축소 동시 애니메이션
        self.play(*moves, *arrow_shrinks, run_time=1.0)

        # 화살표 페이드아웃
        self.play(*[FadeOut(arrow) for arrow in arrows_to_fade], run_time=0.3)

        self.wait(1)

        # 이제 필터에 있는 2,3,5,7의 복사본 생성 및 최종 배치
        final_primes = VGroup()

        # 먼저 필터에 있는 2,3,5,7의 복사본 생성
        prime_filters = [2, 3, 5, 7]
        filter_positions = {
            2: filter_squares,
            3: filter3_squares,
            5: filter5_squares,
            7: filter7_squares,
        }

        for num in prime_filters:
            filter_rect = filter_positions[num][num - 2]

            # 새로운 큰 텍스트 생성
            new_text = Text(str(num), font_size=36)
            new_text.set_color(YELLOW_A)

            # 새로운 컨테이너 생성 - 필터 숫자임을 나타내는 특별한 색상 적용
            new_container = Rectangle(
                width=new_text.width + 0.2,
                height=new_text.height + 0.2,
                fill_opacity=0.15,  # 약간의 채우기 추가
                stroke_opacity=1,
                stroke_color=PURPLE_A,  # 테두리 색상 변경
                stroke_width=2,
            )

            # 텍스트를 컨테이너 중앙에 배치
            new_text.move_to(new_container.get_center())

            # 새로운 그룹 생성
            new_prime = VGroup(new_container, new_text)
            # 필터에서의 위치에서 시작
            new_prime.move_to(filter_rect.get_top() + UP * 0.1)
            final_primes.add(new_prime)

        # 이미 이동된 소수들 추가 (복사본 생성하지 않고 직접 추가)
        for i in range(3, 101, 2):
            if i % 3 != 0 and i % 5 != 0 and i % 7 != 0:
                number = numbers[i - 1]
                final_primes.add(number)

        # 최종 배치 계산
        arranged_primes = VGroup()

        # 2,3,5,7의 최종 위치 계산 - 각각 개별적으로 처리
        small_primes = VGroup()  # 2,3,5,7만을 위한 임시 그룹
        for i in range(4):  # 처음 4개는 2,3,5,7의 복사본
            prime = final_primes[i]
            # 새로운 위치의 복사본 생성
            arranged_prime = prime.copy()
            small_primes.add(arranged_prime)

        # 2,3,5,7을 먼저 간격을 두고 배치
        small_primes.arrange(RIGHT, buff=0.3)  # 동일한 간격으로 배치
        arranged_primes.add(*small_primes)  # 개별 객체로 추가

        # 나머지 소수들의 최종 크기와 위치 계산
        for i in range(4, len(final_primes)):
            old_prime = final_primes[i]

            # 큰 텍스트 생성
            new_text = Text(str(old_prime[1].text), font_size=36)
            new_text.set_color(YELLOW_A)

            # 큰 컨테이너 생성
            new_container = Rectangle(
                width=new_text.width + 0.2,
                height=new_text.height + 0.2,
                fill_opacity=0,
                stroke_opacity=1,
                stroke_color=BLUE,
                stroke_width=2,
            )

            # 텍스트를 컨테이너 중앙에 배치
            new_text.move_to(new_container.get_center())

            # 새로운 그룹 생성
            new_prime = VGroup(new_container, new_text)
            arranged_primes.add(new_prime)

        # 모든 소수들을 일렬로 배치 (동일한 간격으로)
        arranged_primes.arrange(RIGHT, buff=0.3)
        arranged_primes.stretch_to_fit_width(config.frame_width - 1)
        arranged_primes.move_to(ORIGIN)
        arranged_primes.shift(UP * final_y)

        # 변환 애니메이션 생성
        transforms = []
        for i in range(len(final_primes)):
            if i < 4:  # 2,3,5,7의 복사본은 이동만
                transforms.append(
                    final_primes[i].animate.move_to(arranged_primes[i].get_center())
                )
            else:  # 나머지 소수들은 크기 변경과 이동을 함께
                transforms.append(Transform(final_primes[i], arranged_primes[i]))

        # 최종 이동 애니메이션
        self.play(*transforms, run_time=1.5)

        self.wait(2)
