from manim import *

class ArithmaticMean(Scene):
    def construct(self):
        # 격자 생성
        plane = NumberPlane(
            x_range=[0, 12],
            y_range=[0, 12],
            x_length=12,
            y_length=12,
            background_line_style={
                "stroke_opacity": 0.6,
                "stroke_width": 1.2
            }
        )
        
        # 좌표축 생성
        axes = Axes(
            x_range=[0, 12],
            y_range=[0, 12],
            x_length=12,
            y_length=12,
            tips=True,
            axis_config={
                "include_numbers": True,
                "stroke_width": 2,
                "font_size": 24,
                "numbers_to_exclude": []
            }
        )

        # 전체 그래프를 좌하단으로 이동
        graph_group = VGroup(plane, axes)
        graph_group.scale(0.575)

        # 1~10까지 모든 막대 그래프 생성
        bars = VGroup()
        for x in range(1, 11):
            start_point = axes.c2p(x, 0)
            end_point = axes.c2p(x, x)
            
            bar = Rectangle(
                height=abs(end_point[1] - start_point[1]),
                width=0.3,
                fill_opacity=1.0,
                fill_color="#2EAEFF",
                stroke_width=1.5,
                stroke_color=WHITE
            ).move_to(start_point, aligned_edge=DOWN)
            bars.add(bar)

        # 1과 10의 막대 복제본 생성 (테두리 두께와 색상 강조)
        bar_1 = bars[0].copy().set_fill("#FFA726").set_stroke(WHITE, width=2.5)
        bar_10 = bars[9].copy().set_fill("#FFA726").set_stroke(WHITE, width=2.5)

        # 모든 요소를 포함하는 그룹 생성
        all_elements = VGroup(graph_group, bars)

        # 애니메이션 순서
        self.add(plane, axes)
        self.play(Create(bars))
        self.wait()

        # 모든 요소를 왼쪽으로 이동
        self.play(
            all_elements.animate.shift(LEFT * 3)
        )
        self.wait()

        # 1과 10의 막대 하이라이트
        self.play(
            bars[0].animate.set_fill("#FFA726").set_stroke(WHITE, width=2.5),
            bars[9].animate.set_fill("#FFA726").set_stroke(WHITE, width=2.5)
        )
        self.wait()

        # 복제된 막대들을 우측으로 이동 (위치 조정)
        bar_group = VGroup(bar_1, bar_10)
        bar_group.arrange(RIGHT, buff=0.3)
        bar_group.move_to(RIGHT * 4)
        
        self.play(
            TransformFromCopy(bars[0], bar_1),
            TransformFromCopy(bars[9], bar_10)
        )
        self.wait()

        # 두 막대를 합치는 애니메이션 (중앙 정렬)
        target_center = RIGHT * 4  # 위치 조정
        
        # 먼저 bar_1을 bar_10 위로 이동
        self.play(
            bar_1.animate.next_to(bar_10, UP, buff=0)
        )
        self.wait()

        # 합쳐진 막대들을 수직 중앙으로 이동 (더 왼쪽으로)
        combined_bars = VGroup(bar_1, bar_10)
        self.play(
            combined_bars.animate.move_to(RIGHT * 1.5)
        )
        self.wait()

        # 합친 높이 텍스트를 (1 + 10)으로 표시
        sum_value = MathTex("(1 + 10)", color=WHITE).scale(0.8)
        sum_value.next_to(combined_bars, RIGHT, buff=0.4)
        self.play(Write(sum_value))

        # 절반을 나누는 선과 "÷2" 텍스트, "=" 한번에 추가
        half_line = DashedLine(
            combined_bars.get_left() + RIGHT * 0.15,
            combined_bars.get_right() - RIGHT * 0.15,
            stroke_width=2,
            color=WHITE
        ).move_to(combined_bars.get_center())

        divide_text = MathTex(r"\div \;\; 2", color=WHITE).scale(0.8)
        equals = MathTex("=", color=WHITE).scale(0.8)
        
        divide_text.next_to(sum_value, RIGHT, buff=0.5)
        equals.next_to(divide_text, RIGHT, buff=0.5)
        
        # 나누기 선과 텍스트를 동시에 표시
        self.play(
            Create(half_line),
            Write(divide_text),
            Write(equals),
            run_time=0.8  # 실행 시간 단축
        )
        self.wait()

        # 최종 평균 막대 생성 (높이 5.5)
        final_mean_bar = Rectangle(
            height=abs(axes.c2p(0, 5.5)[1] - axes.c2p(0, 0)[1]),
            width=0.3,
            fill_opacity=1.0,
            fill_color="#FF6B6B",
            stroke_width=2,
            stroke_color=WHITE
        )

        # 평균 막대를 등호 오른쪽에 배치하고 수직 중앙 정렬
        final_mean_bar.next_to(equals, RIGHT, buff=2.2)
        final_mean_bar.move_to(combined_bars.get_center() + RIGHT * 4.2, aligned_edge=ORIGIN)

        # 평균값 텍스트 추가
        mean_value = MathTex("5.5", color=WHITE).scale(0.8)
        mean_value.next_to(final_mean_bar, RIGHT, buff=0.3)

        # 최종 평균 막대와 값 표시 (더 빠르게)
        self.play(
            Create(final_mean_bar),
            Write(mean_value),
            run_time=0.5
        )

        # Arithmetic Mean 텍스트 
        mean_text = Text("Arithmetic Mean", color=WHITE).scale(0.4)
        mean_text.next_to(final_mean_bar, DOWN, buff=0.3)
        
        self.play(
            Write(mean_text),
            run_time=0.5
        )
        self.wait()  # 1초 유지

        # 평균 막대 복제 후 좌표평면으로 이동
        mean_bar_copy = final_mean_bar.copy()
        target_position = axes.c2p(5.5, 0)
        
        self.play(
            mean_bar_copy.animate.move_to(target_position, aligned_edge=DOWN),
            run_time=0.8
        )

        # 나머지 요소들 페이드 아웃
        self.play(
            FadeOut(VGroup(
                bar_1, bar_10, half_line, sum_value, 
                divide_text, equals, final_mean_bar, mean_value,
                mean_text
            )),
            bars[0].animate.set_fill("#2EAEFF").set_stroke(WHITE, width=1.5),
            bars[9].animate.set_fill("#2EAEFF").set_stroke(WHITE, width=1.5),
            run_time=0.8
        )
        self.wait()

        # 새로운 y축 스케일로 조정된 좌표평면 생성 (x축은 아직 12까지만)
        new_plane = NumberPlane(
            x_range=[0, 12],      # 56에서 12로 수정
            y_range=[0, 12],
            x_length=12,          # 24에서 12로 수정
            y_length=6,
            background_line_style={
                "stroke_opacity": 0.6,
                "stroke_width": 1.2
            }
        )
        
        new_axes = Axes(
            x_range=[0, 12],      # 56에서 12로 수정
            y_range=[0, 12],
            x_length=12,          # 24에서 12로 수정
            y_length=6,
            tips=True,
            axis_config={
                "include_numbers": True,
                "stroke_width": 2,
                "font_size": 24,
                "numbers_to_exclude": []
            }
        )

        new_graph_group = VGroup(new_plane, new_axes)
        new_graph_group.scale(0.575)
        new_graph_group.shift(LEFT * 3 + UP * 2)  # 위쪽으로 이동

        # 막대들도 새로운 스케일에 맞게 조정
        new_bars = VGroup()
        for x in range(1, 11):
            start_point = new_axes.c2p(x, 0)
            end_point = new_axes.c2p(x, x)
            
            bar = Rectangle(
                height=abs(end_point[1] - start_point[1]),
                width=0.3,
                fill_opacity=1.0,
                fill_color="#2EAEFF",
                stroke_width=1.5,
                stroke_color=WHITE
            ).move_to(start_point, aligned_edge=DOWN)
            new_bars.add(bar)

        # 5.5 막대도  
        new_mean_bar = Rectangle(
            height=abs(new_axes.c2p(0, 5.5)[1] - new_axes.c2p(0, 0)[1]),
            width=0.3,
            fill_opacity=1.0,
            fill_color="#FF6B6B",
            stroke_width=2,
            stroke_color=WHITE
        ).move_to(new_axes.c2p(5.5, 0), aligned_edge=DOWN)

        # 기존 요소들을 새로운 요소들로 변환
        self.play(
            ReplacementTransform(graph_group, new_graph_group),
            ReplacementTransform(bars, new_bars),
            ReplacementTransform(mean_bar_copy, new_mean_bar),
            run_time=1.5
        )
        self.wait()

        # 아래쪽 좌표평면 생성 (12까지)
        bottom_plane = NumberPlane(
            x_range=[0, 12],
            y_range=[0, 12],
            x_length=12,
            y_length=6,
            background_line_style={
                "stroke_opacity": 0.6,
                "stroke_width": 1.2
            }
        )
        
        bottom_axes = Axes(
            x_range=[0, 12],
            y_range=[0, 12],
            x_length=12,
            y_length=6,
            tips=True,
            axis_config={
                "include_numbers": True,
                "stroke_width": 2,
                "font_size": 24,
                "numbers_to_exclude": []
            }
        )

        bottom_graph_group = VGroup(bottom_plane, bottom_axes)
        bottom_graph_group.scale(0.575)
        bottom_graph_group.to_edge(DOWN, buff=0.2)
        bottom_graph_group.shift(LEFT * 3)

        # 아래쪽 좌표평면 복제
        self.play(
            TransformFromCopy(new_graph_group, bottom_graph_group),
            run_time=1
        )

        # 5.5 막대를 아래쪽 좌표평면의 x=1 위치로 이동
        first_position = bottom_axes.c2p(1, 0)
        
        # z-index 설정
        new_mean_bar.set_z_index(1)
        bottom_graph_group.set_z_index(0)
        
        self.play(
            new_mean_bar.animate.move_to(first_position, aligned_edge=DOWN),
            run_time=1
        )
        self.wait()

        # 나머지 9개의 막대 생성 및 배치
        mean_bars = VGroup()
        mean_bars.add(new_mean_bar)  # 첫 번째 막대 추가

        for x in range(2, 11):  # 2부터 10까지
            bar_copy = new_mean_bar.copy()
            bar_copy.move_to(bottom_axes.c2p(x, 0), aligned_edge=DOWN)
            mean_bars.add(bar_copy)
            self.play(
                TransformFromCopy(new_mean_bar, bar_copy),
                run_time=0.3
            )
        self.wait()

        # 이제 x축 확장을 위한 새운 좌표평면과 막대들 생성
        expanded_top_plane = NumberPlane(
            x_range=[0, 56],
            y_range=[0, 12],
            x_length=24,
            y_length=6,
            background_line_style={
                "stroke_opacity": 0.6,
                "stroke_width": 1.2
            }
        )
        
        expanded_top_axes = Axes(
            x_range=[0, 56],
            y_range=[0, 12],
            x_length=24,
            y_length=6,
            tips=True,
            axis_config={
                "include_numbers": True,
                "stroke_width": 2,
                "font_size": 24,
                "numbers_to_exclude": []
            }
        )

        expanded_top_group = VGroup(expanded_top_plane, expanded_top_axes)
        expanded_top_group.scale(0.575)
        expanded_top_group.to_edge(LEFT, buff=0.1)
        expanded_top_group.shift(UP * 2)

        # 확장된 상단 막대들 생성
        expanded_top_bars = VGroup()
        for x in range(1, 11):
            start_point = expanded_top_axes.c2p(x, 0)
            end_point = expanded_top_axes.c2p(x, x)
            
            bar = Rectangle(
                height=abs(end_point[1] - start_point[1]),
                width=0.15,
                fill_opacity=1.0,
                fill_color="#2EAEFF",
                stroke_width=1.5,
                stroke_color=WHITE
            ).move_to(start_point, aligned_edge=DOWN)
            expanded_top_bars.add(bar)

        # 확장된 상단 5.5 막대
        expanded_top_mean_bar = Rectangle(
            height=abs(expanded_top_axes.c2p(0, 5.5)[1] - expanded_top_axes.c2p(0, 0)[1]),
            width=0.15,
            fill_opacity=1.0,
            fill_color="#FF6B6B",
            stroke_width=2,
            stroke_color=WHITE
        ).move_to(expanded_top_axes.c2p(5.5, 0), aligned_edge=DOWN)

        # 하단 좌표평면과 막대들 복제
        expanded_bottom_group = expanded_top_group.copy()
        expanded_bottom_group.to_edge(LEFT, buff=0.1)
        expanded_bottom_group.shift(DOWN * 3.75)

        # expanded_bottom_axes 정의
        expanded_bottom_axes = expanded_bottom_group[1]  # group의 두 번째 요소가 axes

        # 하단 5.5 막대들 생성 (1~10 위치에)
        expanded_bottom_bars = VGroup()
        for x in range(1, 11):
            start_point = expanded_bottom_axes.c2p(x, 0)
            bar = Rectangle(
                height=abs(expanded_bottom_axes.c2p(0, 5.5)[1] - expanded_bottom_axes.c2p(0, 0)[1]),
                width=0.15,
                fill_opacity=1.0,
                fill_color="#FF6B6B",
                stroke_width=2,
                stroke_color=WHITE
            ).move_to(start_point, aligned_edge=DOWN)
            expanded_bottom_bars.add(bar)

        # x축 확장 애니메이션 (막대들도 함께 변환)
        self.play(
            Transform(new_graph_group, expanded_top_group),
            Transform(new_bars, expanded_top_bars),
            Transform(new_mean_bar, expanded_top_mean_bar),
            Transform(bottom_graph_group, expanded_bottom_group),
            Transform(mean_bars, expanded_bottom_bars),
            run_time=1.5
        )
        self.wait()

        # x축 확장 애니메이션 후에 추가

        # 상단 좌표축에서 막대 수평 쌓기
        stacked_bars_top = VGroup()
        current_x = 0  # 시작 x 위치
        
        for i in range(10):  # 1부터 10까지의 막대
            bar_copy = expanded_top_bars[i].copy()
            bar_copy.set_fill("#32CD32", opacity=1.0)
            bar_copy.set_stroke(WHITE, width=2.5)
            bar_copy.set_z_index(2)
            
            # 막대 내부에 표시할 숫자 (흰색에서 검정색으로 변경)
            number = MathTex(f"{i+1}", color=BLACK).scale(0.3)
            number.set_z_index(3)
            
            x_unit = expanded_top_axes.c2p(1, 0)[0] - expanded_top_axes.c2p(0, 0)[0]
            bar_length = x_unit * (i + 1)
            
            target_x = expanded_top_axes.c2p(current_x, 11)[0] + bar_length/2
            target_y = expanded_top_axes.c2p(0, 11)[1]
            
            initial_y = expanded_top_axes.c2p(i+1, 11)[1] - bar_copy.height/2
            self.play(
                bar_copy.animate.move_to([expanded_top_axes.c2p(i+1, 0)[0], initial_y, 0]),
                run_time=0.2
            )
            
            # 회전하면서 최종 위치로 이동
            self.play(
                bar_copy.animate.rotate(PI/2).stretch_to_fit_width(bar_length).move_to([target_x, target_y, 0]),
                run_time=0.3
            )
            
            # 숫자를 막대 중앙에 배치 (애니메이션 없이)
            number.move_to(bar_copy.get_center())
            self.add(number)
            
            stacked_bars_top.add(VGroup(bar_copy, number))
            current_x += i + 1

        # 하단 좌표축에서 막대 수평 쌓기
        stacked_bars_bottom = VGroup()
        current_x = 0
        
        x_unit = expanded_bottom_axes.c2p(1, 0)[0] - expanded_bottom_axes.c2p(0, 0)[0]
        unit_length = x_unit * 5.5
        
        for i in range(10):  # 모든 5.5 막대
            bar_copy = expanded_bottom_bars[i].copy()
            bar_copy.set_fill("#FF69B4", opacity=1.0)
            bar_copy.set_stroke(WHITE, width=2.5)
            bar_copy.set_z_index(2)
            
            # 5.5 텍스트 (흰색에서 검정색으로 변경)
            number = MathTex("5.5", color=BLACK).scale(0.3)
            number.set_z_index(3)
            
            target_x = expanded_bottom_axes.c2p(current_x, 11)[0] + unit_length/2
            target_y = expanded_bottom_axes.c2p(0, 11)[1]
            
            initial_y = expanded_bottom_axes.c2p(i+1, 11)[1] - bar_copy.height/2
            self.play(
                bar_copy.animate.move_to([expanded_bottom_axes.c2p(i+1, 0)[0], initial_y, 0]),
                run_time=0.2
            )
            
            # 회전하면서 최종 위치로 이동
            self.play(
                bar_copy.animate.rotate(PI/2).stretch_to_fit_width(unit_length).move_to([target_x, target_y, 0]),
                run_time=0.3
            )
            
            # 숫자를 막대 중앙에 배치 (애니메이션 없이)
            number.move_to(bar_copy.get_center())
            self.add(number)
            
            stacked_bars_bottom.add(VGroup(bar_copy, number))
            current_x += 5.5

        # 최종 합계 표시 (55)
        top_sum = MathTex("55", color=WHITE).scale(0.8)
        bottom_sum = MathTex("55", color=WHITE).scale(0.8)
        
        top_sum.next_to(stacked_bars_top, RIGHT, buff=0.3)
        bottom_sum.next_to(stacked_bars_bottom, RIGHT, buff=0.3)
        
        self.play(
            Write(top_sum),
            Write(bottom_sum)
        )
        self.wait()

        # 최종 합계 표시 (55) 후에 추가

        # 상단 좌표축에 1+2+3+...+10=55 표시
        top_formula = MathTex(
            "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 = 55",
            color=WHITE
        ).scale(1.0)
        
        # 하단 좌표축에 산술평균 공식 표시
        bottom_formula = MathTex(
            r"\left(\frac{1 + 10}{2}\right) \times 10 = 5.5 \times 10 = 55",
            color=WHITE
        ).scale(1.0)

        # 수식들의 위치 조정 (크기가 커진만큼 x 위치를 더 오른쪽으로)
        top_formula.move_to(
            expanded_top_axes.c2p(35, 6)
        )
        
        bottom_formula.move_to(
            expanded_bottom_axes.c2p(35, 6)
        )

        # 수식 표시
        self.play(
            Write(top_formula),
            Write(bottom_formula),
            run_time=1
        )
        self.wait()

        # 수식 표시 후에 추가
        
        # 상단과 하단의 x축 55 눈금 위치에 강조 원 추가
        top_circle = Circle(
            radius=0.2,  # 0.3에서 0.2로 축소
            color=YELLOW,
            stroke_width=3
        ).move_to(expanded_top_axes.c2p(55, -0.3))  # y=0에서 y=-0.3으로 수정

        bottom_circle = Circle(
            radius=0.2,  # 0.3에서 0.2로 축소
            color=YELLOW,
            stroke_width=3
        ).move_to(expanded_bottom_axes.c2p(55, -0.3))  # y=0에서 y=-0.3으로 수정

        # 원 애니메이션 (깜빡이는 효과)
        self.play(
            Create(top_circle),
            Create(bottom_circle)
        )
        self.play(
            top_circle.animate.scale(1.2).set_stroke(opacity=0.7),
            bottom_circle.animate.scale(1.2).set_stroke(opacity=0.7)
        )
        self.play(
            top_circle.animate.scale(1/1.2).set_stroke(opacity=1),
            bottom_circle.animate.scale(1/1.2).set_stroke(opacity=1)
        )
        self.wait()
