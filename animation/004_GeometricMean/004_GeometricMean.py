from manim import *
import numpy as np
from decimal import Decimal, ROUND_HALF_UP


class GeometricMean(Scene):
    def construct(self):
        # 5개의 데이터 포인트만 사용
        years = ["A", "B", "C", "D", "E"]
        values = [45, 85, 78, 110, 120]

        # 바차트 생성 - 크기 조정
        chart = BarChart(
            values,
            y_range=[0, 130, 20],
            x_length=7,  # 가로 길이 더 축소
            y_length=3.5,  # 세로 길이 더 축소
            x_axis_config={"font_size": 18,
                           "include_numbers": False},  # x축 숫자 눈금 제거
            y_axis_config={"font_size": 18},
        )  # 초기 위치는 중앙에 (shift 제거)

        # x축 레이블 추가
        labels = VGroup(*[
            Text(year, font_size=24)
            for year in years
        ])

        # x축 레이블 위치 조정 (좌표 추가 없이 직접 위치 지정)
        for i, label in enumerate(labels):
            label.next_to(chart.bars[i], DOWN, buff=0.4)  # 버퍼 간격 축소

        # 바 위에 값 표시 추가
        value_labels = VGroup()
        for i, value in enumerate(values):
            label = Text(str(value), font_size=16)
            label.next_to(chart.bars[i], UP, buff=0.1)
            value_labels.add(label)

        # 성장률 계산 및 호 추가
        growth_rates = []        # 실제 숫자값
        growth_rates_display = []  # 표시용 문자열 (상단 차트용 - ≈ 유지)
        growth_rates_simple = []  # 좌하단 차트용 - ≈ 없음
        growth_arrows = []
        growth_labels = []

        # 먼저 모든 growth_rates 계산
        for i in range(len(values)-1):
            growth_rate = values[i+1] / values[i]
            growth_rates.append(growth_rate)

        # g_value 미리 계산
        growth_product = np.prod(growth_rates)
        g_value = (growth_product ** 0.25)

        # 이제 화살표와 레이블 생성
        for i in range(len(values)-1):
            growth_rates_display.append(f"≈ {growth_rates[i]:.2f}x")  # 모든 화살표에 실제 성장률 사용
                
            growth_rates_simple.append(f"{growth_rates[i]:.2f}x")
            
            bar_width = chart.bars[0].width
            start = chart.bars[i].get_bottom() + DOWN * 0.8 + \
                RIGHT * (bar_width * 0.3)
            end = chart.bars[i+1].get_bottom() + DOWN * 0.8 + \
                LEFT * (bar_width * 0.3)
            
            arc = CurvedArrow(
                start_point=start,
                end_point=end,
                angle=TAU/4,
                color=BLUE,  # 모든 화살표를 파란색으로
                tip_length=0.2,
                stroke_width=2.5
            )

            rate_text = Text(
                growth_rates_display[-1],
                font_size=14,
                color=BLUE  # 모든 텍스트를 파란색으로
            )
            rate_text.next_to(arc, DOWN, buff=0.1)

            growth_arrows.append(arc)
            growth_labels.append(rate_text)

        # 제목 위치 조정
        title = Text("Growth Pattern Example", font_size=28)  # 폰트 크기 축소
        title.next_to(chart, UP, buff=0.3)  # 버퍼 간격 축소

        # 바차트, 제목, 년도 레이블을 하나의 그룹으로 묶기
        main_chart_group = VGroup(
            chart,
            title,
            labels
        )

        # 애니메이션 - 바차트 그룹과 값 라벨 표시
        self.play(
            Create(main_chart_group),
            Write(value_labels)
        )

        # 성장률 화살표와 레이블 애니메이션
        for arrow, label in zip(growth_arrows, growth_labels):
            self.play(
                Create(arrow),
                Write(label),
                run_time=0.5
            )

        self.wait(1)

        # 모든 요소들을 하나 으로 묶기 (원 제외)
        all_elements = VGroup(
            chart,
            title,
            labels,
            value_labels,
            *growth_arrows,
            *growth_labels
        )

        # 모든 요소를 위로 이동하고 스케일 조정하는 애니메이션 추가
        self.play(
            all_elements.animate.shift(
                UP * 2).scale(0.7),  # 이동과 동시에 크기를 70%로 축소
            run_time=1.5
        )

        self.wait(1)

        # 성장률 값들 추출
        growth_values = growth_rates  # 이미 숫자값으로 저장되어 있으므로 직접 사용

        # 성장률 바차트 생성
        ratio_chart = BarChart(
            growth_values,
            y_range=[0, 3, 0.5],  # 최대값이 3까지, 0.5 단위로
            x_length=4,  # 작은 크기
            y_length=2,
            bar_colors=[BLUE],
            x_axis_config={"font_size": 14},
            y_axis_config={"font_size": 14}  # 따옴표와 등호 사이의 공백 제거
        ).scale(0.8)  # 전체적으로 더 작게

        # 좌하단으로 위치 이동
        ratio_chart.shift(LEFT * 4.5 + DOWN * 2)  # LEFT * 5에서 LEFT * 4.5 수정

        # 바 위에 실제 값 표시 (좌하단 차트)
        ratio_labels = VGroup()
        for i, value in enumerate(growth_rates_simple):  # growth_rates_simple 사용
            label = Text(value, font_size=14, color=BLUE)
            label.next_to(ratio_chart.bars[i], UP, buff=0.1)
            ratio_labels.add(label)

        # "Growth Ratios" 제목 추가
        ratio_title = Text("Actual Growth Ratios", font_size=20)
        ratio_title.next_to(ratio_chart, UP, buff=0.3)

        # 애니메이션으로 표시 (대기시간 축소)
        self.play(
            Create(ratio_chart),
            Write(ratio_title),
            Write(ratio_labels),
            run_time=1
        )

        self.wait(0.5)

        # 이 시점에 원 추가 (좌하단 바차트 생성 후, 수식 전)
        first_circle = Circle(
            radius=0.2,
            color=RED,
            stroke_width=3
        ).move_to(value_labels[0])

        last_circle = Circle(
            radius=0.2,
            color=RED,
            stroke_width=3
        ).move_to(value_labels[-1])

        # 원 애니메이션
        self.play(
            Create(first_circle),
            Create(last_circle),
            run_time=0.5
        )

        self.wait(0.3)

        # 원을 all_elements 그에 추가
        all_elements.add(first_circle, last_circle)

        # growth_product 계산 분 수정
        growth_product = np.prod(growth_rates)
        growth_rates_str = " \\times ".join(
            [f"{rate:.2f}" for rate in growth_rates])

        # ratio_chart 아래 수식의 등호를 근사 기호로 변경
        equation = MathTex(
            f"{values[0]}", "\\times", "(", growth_rates_str, ")", "\\approx", f"{values[-1]}",
            font_size=24
        )
        equation.set_color_by_tex(str(values[0]), RED)
        equation.set_color_by_tex(str(values[-1]), RED)
        # growth_rates_str는 기본 흰색으로 유지
        equation.next_to(ratio_chart, DOWN, buff=0.3)

        self.play(
            Write(equation),
            run_time=1
        )

        self.wait(1)  # 2초에서 1초로 축소

        # 기하평균 계산 과정 수식 (중앙 하단)
        geo_equation1 = MathTex(
            "45", "\\times", "(G \\times G \\times G \\times G)", "=", "120",
            font_size=24
        )
        geo_equation1.set_color_by_tex("45", RED)
        geo_equation1.set_color_by_tex("120", RED)
        geo_equation1.set_color_by_tex("G", GREEN)

        geo_equation2 = MathTex(
            "G \\times G \\times G \\times G", "=", growth_rates_str,
            font_size=24
        )
        geo_equation2.set_color_by_tex("G", GREEN)

        geo_equation3 = MathTex(
            "G^4", "=", growth_rates_str,
            font_size=24
        )
        geo_equation3.set_color_by_tex("G^4", GREEN)

        geo_equation4 = MathTex(
            "G", "=", "\\sqrt[4]{" + growth_rates_str + "}",
            font_size=24
        )
        geo_equation4.set_color_by_tex("G", GREEN)

        # G의 실제 값 계산 및 추가 - 폰트 크기 증가 및 공백 추가
        g_value = (growth_product ** 0.25)
        geo_equation5 = MathTex(
            f"G \\approx {g_value:.2f}",
            font_size=36  # 폰트 크기 24에서 36으로 증가
        )
        geo_equation5.set_color_by_tex("G", GREEN)

        # 수식들을 세로로 정렬 - 마지막 G값 앞에 추가 공백
        geo_equations = VGroup(
            geo_equation1,
            geo_equation2,
            geo_equation3,
            geo_equation4
        ).arrange(DOWN, buff=0.2)

        # G값은 별도로 배하여 추가 간격 확보
        # buff를 0.2에서 0.4로 증가
        geo_equation5.next_to(geo_equations, DOWN, buff=0.4)

        # 전체 그룹을 다시 생성
        all_geo_equations = VGroup(geo_equations, geo_equation5)

        # 위치 약 위로 조정
        all_geo_equations.move_to(DOWN * 1.8)

        # 순차적으 애니메이션 표시 - G값도 포함
        for eq in [geo_equation1, geo_equation2, geo_equation3, geo_equation4, geo_equation5]:
            self.play(
                Write(eq),
                run_time=1
            )
            self.wait(0.5)

        self.wait(1)

        # 기하평균 성장률 바차트 생성 (우하단)
        geo_mean_values = [g_value] * 4  # 같은 값 4번 반복
        geo_mean_chart = BarChart(
            geo_mean_values,
            y_range=[0, 3, 0.5],
            x_length=4,
            y_length=2,
            bar_colors=[GREEN],
            x_axis_config={"font_size": 14},
            y_axis_config={"font_size": 14},
        ).scale(0.8)

        # 우하단으로 위치 이동
        geo_mean_chart.shift(RIGHT * 5 + DOWN * 2)

        # 바 위에 실제 값 표시
        geo_mean_labels = VGroup()
        for i in range(4):
            label = Text(f"{g_value:.2f}x", font_size=14, color=GREEN)
            label.next_to(geo_mean_chart.bars[i], UP, buff=0.1)
            geo_mean_labels.add(label)

        # "Geometric Mean Growth Ratios" 제목 추가
        geo_mean_title = Text("Geometric Mean Growth Ratios", font_size=20)
        geo_mean_title.next_to(geo_mean_chart, UP, buff=0.3)

        # 애니메이션으로 표시
        self.play(
            Create(geo_mean_chart),
            Write(geo_mean_title),
            Write(geo_mean_labels),
            run_time=1
        )

        # 우하단 바차트 아래 수식 추가
        geo_mean_equation = MathTex(
            f"{values[0]}", "\\times", f"({g_value:.2f} \\times {g_value:.2f} \\times {g_value:.2f} \\times {g_value:.2f})", "\\approx", f"{values[-1]}",
            font_size=24
        )
        geo_mean_equation.set_color_by_tex(str(values[0]), RED)
        geo_mean_equation.set_color_by_tex(str(values[-1]), RED)
        geo_mean_equation.next_to(geo_mean_chart, DOWN, buff=0.3)

        self.play(
            Write(geo_mean_equation),
            run_time=1
        )

        self.wait(1)

        # 원본을 좌측으로 이동
        self.play(
            all_elements.animate.shift(LEFT * 4),
            run_time=1.5
        )

        # 중앙에 큰 화살표 추가
        big_arrow = Arrow(
            LEFT * 1.8,
            RIGHT * 1.8,
            stroke_width=30,
            max_tip_length_to_length_ratio=0.25,
            color=YELLOW_B,
            buff=0.8
        ).scale(1.5)

        big_arrow.shift(UP * 2)

        self.play(
            GrowArrow(big_arrow),
            run_time=1
        )

        self.wait(1)

        # 복제본 생성 및 우측으로 이동
        new_chart_group = all_elements.copy()
        new_chart_group.shift(RIGHT * 8.5)  # 원본이 LEFT * 4로 이동했으므로, 총 RIGHT * 8.5 이동
        
        # 타이틀 텍스트 변경
        old_title = new_chart_group[1]
        old_title.become(Text(
            "Geometric  Growth",
            font_size=old_title.font_size
        ).move_to(old_title.get_center()))  # 위치를 유지하면서 텍스트 변경

        # 새로운 값 계산 (기하평균의 누적 곱)
        geo_values = [values[0]]  # 첫 번째 값은 그대로 (45)
        for _ in range(4):  # 4번 반복하여 다음 값 계산
            geo_values.append(geo_values[-1] * g_value)
        geo_values = geo_values[:5]  # 5개 값만 사용

        # 좌상단의 바와 바 상단 텍스트 사이의 버퍼 값
        original_buff = 0.1  # 좌상단에서 사용한 버퍼 값

        # 바의 높이 조정 및 상단 텍스트 변경
        for i in range(len(geo_values)):
            bar = new_chart_group[0].bars[i]
            
            # 복제된 차트의 y_range를 사용하여 정확한 높이 계산
            y_min, y_max, y_step = new_chart_group[0].y_range  # 복제된 차트의 y_range 사용
            value_ratio = (geo_values[i] - y_min) / (y_max - y_min)
            new_height = value_ratio * new_chart_group[0].y_length  # 복제된 차트의 y_length 사용
            
            # 바의 높이를 수동으로 조정 (0.7배)
            new_height *= 0.7
            
            # 바의 높이와 위치 조정
            bar.stretch_to_fit_height(new_height)
            
            # x축 위치 계산 수정 - 눈금 사이 중간에 오도록
            x_coord = i + 0.5  # 0.5를 더해서 눈금 사이 중간으로 이동
            bar_bottom = new_chart_group[0].c2p(x_coord, 0)
            bar.move_to(bar_bottom, aligned_edge=DOWN)
            
            # 상단 라벨의 텍스트와 위치 업데이트
            new_value = round(geo_values[i])  # 소수점 첫째 자리에서 반올림하여 정수부만 사용
            if i == 0:
                new_label = Text(str(new_value), font_size=16)  # 첫 번째 값에는 '거의 같음 기호' 없음
            else:
                new_label = Text(f"≈ {new_value}", font_size=16)  # '거의 같음 기호' 추가
            new_label.scale(0.7)  # 텍스트 크기를 0.7배로 줄임
            new_label.next_to(bar, UP, buff=original_buff * 0.7)  # 좌상단과 동일한 버퍼 사용
            new_chart_group[3][i].become(new_label)  # 기존 라벨을 신규 라벨로 교체

        # 화살표 색상 변경 및 비율 텍스트 업데이트
        for i in range(4):
            new_chart_group[4 + i].set_color(GREEN)
            
            old_text = new_chart_group[8 + i]
            new_text = Text(
                f"≈ {g_value:.2f}x",
                font_size=old_text.font_size,
                color=GREEN
            ).move_to(old_text)
            new_chart_group[8 + i].become(new_text)

        # 차트 그룹을 한 번에 표시
        self.play(
            FadeIn(new_chart_group),
            run_time=1.5
        )

        self.wait(3)
