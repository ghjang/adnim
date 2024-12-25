from manim import *
import numpy as np


class SieveOfEratosthenes(Scene):
    def construct(self):
        # 상수 정의
        GRID_SIZE = 10
        SQUARE_SIZE = 0.6
        TEXT_SIZE = 16

        # 그리드 생성
        squares = VGroup()
        numbers = VGroup()
        target_positions = []

        # 10x10 그리드 생성
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                num = i * GRID_SIZE + j + 1

                # 정사각형 위치 계산
                pos_x = (j - GRID_SIZE / 2 + 0.5) * SQUARE_SIZE
                pos_y = (-i + GRID_SIZE / 2 - 0.5) * SQUARE_SIZE

                # 정사각형 생성
                square = Square(side_length=SQUARE_SIZE)
                square.set_stroke(BLUE_B, 2)
                square.set_fill(BLACK, 0.1)
                square.move_to([pos_x, pos_y, 0])

                # 숫자 텍스트 생성
                number = Text(str(num), font_size=TEXT_SIZE)
                number.set_color(YELLOW_A)

                center_pos = square.get_center()
                target_positions.append(center_pos)
                number.move_to(center_pos)

                squares.add(square)
                numbers.add(number)

        # 전체 그리드를 VGroup으로 묶기
        grid = VGroup(squares)
        grid.move_to(ORIGIN).shift(DOWN * 0.8)

        # target_positions 업데이트 (그리드 이동 반영)
        target_positions = [pos + DOWN * 0.8 for pos in target_positions]

        # 상단에 표시될 100개의 숫자들 생성 (4줄)
        top_numbers = VGroup()

        # 4줄로 나누어 생성 (각 줄 25개씩)
        rows = []
        for row_idx in range(4):
            row = VGroup()
            start_num = row_idx * 25
            for i in range(25):
                # 각 숫자를 고정된 너비의 배경과 함께 생성
                num_text = Text(str(start_num + i + 1), font_size=TEXT_SIZE)
                num_text.set_color(YELLOW_A)

                # 숫자를 담을 고정 너비의 컨테이너 생성
                container = Rectangle(
                    width=0.3,  # 고정된 너비
                    height=0.3,  # 고정된 높이
                    fill_opacity=0,
                    stroke_opacity=0,
                )

                # 숫자를 테이너 중앙 배치
                num_text.move_to(container.get_center())

                # 컨테이너와 숫자를 그룹으로 묶기
                num_group = VGroup(container, num_text)
                row.add(num_group)

            # 각 행의 요소들을 간격 없이 배열
            row.arrange(RIGHT, buff=0.1)
            rows.append(row)

        # 4줄을 세로로 배열
        top_numbers.add(*rows)
        top_numbers.arrange(DOWN, buff=0.1)

        # 숫자들을 그리드 위에 배치
        top_numbers.to_edge(UP, buff=0.15)
        top_numbers.shift(grid.get_center()[0] * RIGHT)

        # 애니메이션 시퀀스
        # 1. 상단에 100개의 숫자를 한 번에 표시
        self.add(top_numbers)
        self.play(FadeIn(top_numbers, shift=UP), run_time=1)
        self.wait(0.3)

        # 2. 그리드 생성 (한 번에 페이드 인)
        self.play(FadeIn(squares), run_time=0.8)
        self.wait(0.3)

        # 3. 숫자들을 그리드로 이동
        animations = []
        for i in range(100):
            source_number = top_numbers[i // 25][i % 25][1]
            target_pos = target_positions[i]
            animations.append(source_number.animate.move_to(target_pos))

        self.play(*animations, run_time=1.5)

        # 4. 최종 위치의 숫자들로 교체
        self.remove(top_numbers)
        for i in range(100):
            numbers[i].move_to(target_positions[i])
        self.add(numbers)

        # 그리드를 감싸는 큰 원 생성
        big_circle = Circle(radius=GRID_SIZE * SQUARE_SIZE / 1.4)
        big_circle.set_stroke(GOLD, 6)
        big_circle.move_to(grid.get_center())

        # 전체 영역을 채우는 배경 그리드 생성
        background_squares = VGroup()
        grid_extent = int(big_circle.radius / SQUARE_SIZE) + 2

        # 기준점 계산 (10x10 그리드의 좌상단 모서리 위치)
        grid_top_left = grid[0][0].get_center()  # 첫 번째 사각형의 중심
        base_x = grid_top_left[0] - SQUARE_SIZE / 2  # 왼쪽 모서리 x좌표
        base_y = grid_top_left[1] + SQUARE_SIZE / 2  # 위쪽 모서리 y좌표

        for i in range(-grid_extent, grid_extent + 1):
            for j in range(-grid_extent, grid_extent + 1):
                # 중앙 10x10 그리드 영역은 건너뛰기
                if (-5 <= i <= 4) and (-5 <= j <= 4):
                    continue

                # 기준점으로부터의 상대적 위치 계산
                pos_x = (
                    base_x + (j + 5) * SQUARE_SIZE
                )  # +5는 10x10 그리드의 왼쪽 경계에 맞추기 위함
                pos_y = (
                    base_y - (i + 5) * SQUARE_SIZE
                )  # +5는 10x10 그리드의 위쪽 경계에 맞추기 위함
                center = np.array(
                    [pos_x + SQUARE_SIZE / 2, pos_y - SQUARE_SIZE / 2, 0]
                )  # 사각형 중심점

                # 원의 중심으로부터의 거리 계산
                dist_from_center = np.linalg.norm(center - grid.get_center())

                # 원 안에 있는 사각형만 추가
                if dist_from_center <= big_circle.radius:
                    square = Square(side_length=SQUARE_SIZE)
                    square.set_stroke(BLUE_D, 0.8)
                    square.set_fill(BLACK, 0.05)
                    square.move_to(center)
                    background_squares.add(square)

        background_squares.move_to(grid.get_center())

        # z-index 설정
        background_squares.set_z_index(-1)  # 배경을 가장 아래로
        big_circle.set_z_index(0)  # 원을 중간으로
        grid.set_z_index(1)  # 그리드를 위로
        numbers.set_z_index(2)  # 숫자를 상위로

        everything = VGroup(background_squares, grid, numbers)

        # 5. 원과 배경 그리드가 나타나면서 전체 확대
        circle_diameter = big_circle.height
        target_scale = (config.frame_height * 0.95) / circle_diameter

        # 애니메이션 순서
        self.add(background_squares)  # 클리핑된 배경 그리드를 먼저
        self.add(big_circle)  # 그 다음 원
        self.play(
            everything.animate.scale(target_scale).move_to(ORIGIN),
            big_circle.animate.scale(target_scale).move_to(ORIGIN),
            run_time=1.5,
        )
        self.wait(0.5)

        # target_positions 업데이트
        target_positions = [pos * target_scale for pos in target_positions]

        # 이후 소수 처리 시작
        # 1 제거
        self.play(
            FadeOut(numbers[0]),
            squares[0].animate.set_fill(GREY, opacity=0.3),
            run_time=0.5,
        )
        self.wait(0.8)  # 대기 시간을 0.3에서 0.8로 증가

        # 2부터 시작하여 √100까지 순차적으로 처리
        for current_num in range(2, int(np.sqrt(100)) + 1):
            idx = current_num - 1

            # 이미 제거된 숫자는 건너뛰기 (fill opacity가 0.3인 경우)
            if squares[idx].get_fill_opacity() == 0.3:
                continue

            # 현재 숫자 강조 (배경색과 볼드체 숫자를 애니메이션 없이 즉시 )
            bold_num = Text(
                str(current_num), font_size=TEXT_SIZE * 1.3, weight=BOLD
            ).move_to(numbers[idx])
            bold_num.set_color(YELLOW)
            numbers[idx].become(bold_num)  # 숫자를 볼드체로 즉시 변경
            squares[idx].set_fill(TEAL, opacity=0.8)  # 배경색을 TEAL로 변경

            # 배수 제거
            fade_outs = []
            color_changes = []
            removed_cells = []

            # current_num의 배수들 처리
            for i in range(current_num * 2, 101, current_num):
                target_idx = i - 1
                # 이미 제거된 숫자는 건너뛰기
                if squares[target_idx].get_fill_opacity() == 0.3:
                    continue
                fade_outs.append(FadeOut(numbers[target_idx]))
                color_changes.append(
                    squares[target_idx].animate.set_fill(RED_A, opacity=0.4)
                )
                removed_cells.append(squares[target_idx])

            if fade_outs:  # 제거할 숫자가 있는 경우만 애니메이션 실행
                self.play(*fade_outs, *color_changes, run_time=1.0)
                self.wait(0.3)

                # 제거된 셀들의 색상을 회색으로 변경
                self.play(
                    *[
                        square.animate.set_fill(GREY, opacity=0.3)
                        for square in removed_cells
                    ],
                    run_time=0.5
                )

        # 마지막으로 남은 소수들 강조
        highlight_primes = []
        for i in range(100):
            if squares[i].get_fill_opacity() != 0.3:  # 제거되지 않은 숫자만
                highlight_primes.append(
                    squares[i].animate.set_fill(GREEN_A, opacity=0.6)
                )
                # 숫자를 볼드체로 변경하고 흰색으로 강조
                bold_num = Text(
                    str(i + 1), font_size=TEXT_SIZE * 1.3, weight=BOLD
                ).move_to(numbers[i])
                bold_num.set_color(WHITE)
                highlight_primes.append(Transform(numbers[i], bold_num))

        if highlight_primes:
            self.play(*highlight_primes, run_time=1.0)

        self.wait(4)


def get_dist_from_origin(point):
    return np.sqrt(point[0] ** 2 + point[1] ** 2)
