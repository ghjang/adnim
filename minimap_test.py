from manim import *

class MinimapDemo(MovingCameraScene):  # Scene 대신 MovingCameraScene 사용
    def construct(self):
        # 카메라 프레임의 종횡비 계산
        camera_width = config.frame_width
        camera_height = config.frame_height
        minimap_size = 2.5  # 미니맵 크기 증가 (0.8 -> 2.5)
        padding = 0.3  # 화면 가장자리로부터의 여백
        
        # 종횡비를 유지하면서 미니맵 크기 계산
        minimap_width = minimap_size
        minimap_height = minimap_size * (camera_height / camera_width)
        
        # 전체 애니메이션 공간 생성
        full_content = VGroup(
            Square(side_length=2),
            Circle(radius=1).shift(RIGHT*3),
            Triangle().shift(LEFT*3+UP*2)
        ).set_stroke(color=BLUE)
        
        # 미니맵용 전체 콘텐츠 복사 및 크기 조정
        minimap_scale = minimap_width / (camera_width * 1.2)  # 미니맵 내부 여백을 위해 1.2로 나눔
        minimap_content = full_content.copy().scale(minimap_scale)
        minimap_frame = Rectangle(
            width=minimap_width,
            height=minimap_height,
            stroke_color=GRAY_C,  # 더 어두운 회색으로 변경
            stroke_width=1  # 선 두께 감소
        ).to_corner(DR, buff=padding)  # 여백 추가
        
        # 미니맵 배경도 같은 크기로 수정
        minimap_bg = Rectangle(
            width=minimap_width,
            height=minimap_height,
            fill_color=BLACK,
            fill_opacity=0.3
        ).to_corner(DR, buff=padding)  # 여백 추가
        
        # 현재 뷰포트 표시
        viewport_indicator = Rectangle(
            width=minimap_width / 1.2,  # 미니맵 내에서의 상대적 크기
            height=minimap_height / 1.2,
            stroke_color=RED,
            stroke_width=1
        )
        
        # 초기 설정
        minimap_content.move_to(minimap_frame)
        self.add(full_content)
        
        # 미니맵 그룹 (배경, 콘텐츠, 프레임)
        minimap_group = VGroup(minimap_bg, minimap_content, minimap_frame)
        
        # 클리핑 영역 설정 (보이지 않는 마스크)
        clip_rect = Rectangle(
            width=minimap_width,
            height=minimap_height,
            stroke_width=0,
            fill_opacity=0
        ).to_corner(DR, buff=padding)
        
        def get_minimap_position():
            pos = (
                self.camera.frame.get_corner(DR) + 
                LEFT * (minimap_width/2 + padding) + 
                UP * (minimap_height/2 + padding)
            )
            clip_rect.move_to(pos)  # 클리핑 마스크도 함께 이동
            return pos
        
        # 미니맵 그룹 업데이터
        minimap_group.add_updater(lambda m: m.move_to(get_minimap_position()))
        
        # viewport indicator 설정 및 업데이터
        def update_viewport(m):
            relative_pos = minimap_frame.get_center() + self.camera.frame.get_center() * minimap_scale
            m.move_to(relative_pos)
            # 클리핑 영역 설정
            m.clip_paths = [clip_rect]
        
        viewport_indicator.add_updater(update_viewport)
        
        # 요소들 추가 (렌더링 순서 중요)
        self.add(minimap_group)
        self.add(viewport_indicator)
        
        # 카메라 이동 애니메이션
        self.play(
            self.camera.frame.animate.shift(RIGHT*3),
            run_time=2
        )
        self.play(
            self.camera.frame.animate.shift(UP*2),
            run_time=2
        )