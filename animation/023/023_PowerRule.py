from typing import override
from manim import *
from common.decorator.latex_factory import latex_factory
from common.template.proof_sequence.base_proof_scene import (
    BaseProofScene,
    ProofSceneConfig,
    ProofStepItem,
)


class PowerRuleProof(BaseProofScene):
    @override
    def construct(self):
        return super().construct()

    @override
    def configure(self, config: ProofSceneConfig) -> ProofSceneConfig:
        config.start_position += LEFT * 2
        config.font_size = 42
        config.scene_end_pause += 1
        return config

    @override
    def get_title(self) -> str:
        return "Proof of Power Rule"

    @override
    @latex_factory()
    def get_intro_formula(self) -> str:
        return r"\frac{d}{dx}x^n = n \cdot x^{n-1} \quad (n \in \mathbb{N})"

    @override
    @latex_factory()
    def get_proof_steps(self, step_group_index: int) -> list[ProofStepItem]:
        steps = [
            # 1. 미분 정의 사용
            r"\frac{d}{dx}x^n = \lim_{h \to 0} \frac{(x+h)^n - x^n}{h}",
            # 2. 이항 정리 공식 제시 (시그마 표기)
            {
                "text": r"\text{Binomial Theorem:}\quad (x+h)^n = \sum_{k=0}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k",
                "font_size": 32,
                "color": RED,
                "h_offset": RIGHT * 0.7,
            },
            # 3. 이항 정리 대입
            r"= \lim_{h \to 0} \frac{\left\{ \sum\limits_{k=0}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k \right\} - x^n}{h}",
            # 4. k=0 항 분리
            r"= \lim_{h \to 0} \frac{\left\{ \binom{n}{0} \cdot x^{n} \cdot h^0 + \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k \right\} - x^n}{h}",
            # 5. k=0 항 계산 (\binom{n}{0}=1, h^0=1)
            r"= \lim_{h \to 0} \frac{\left\{ 1 \cdot x^{n} \cdot 1 + \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k \right\} - x^n}{h}",
            # 6. k=0 항 정리 (x^n)
            r"= \lim_{h \to 0} \frac{\left\{ x^n + \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k \right\} - x^n}{h}",
            # 7. 중괄호 제거 (분자 정리)
            r"= \lim_{h \to 0} \frac{ x^n + \left\{ \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k \right\} - x^n}{h}",
            # 8. 항 재배열 (소거 준비)
            r"= \lim_{h \to 0} \frac{ x^n - x^n + \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k }{h}",
            # 9. x^n 항 소거
            r"= \lim_{h \to 0} \frac{ 0 + \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k }{h}",
            # 10. 분자 단순화
            r"= \lim_{h \to 0} \frac{\sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^k}{h}",
            # 11. 분자 h 인수분해 준비 (h^k = h * h^(k-1))
            r"= \lim_{h \to 0} \frac{\sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k - 1} \cdot h}{h}",
            # 12. 분자 전체에서 h 인수분해
            r"= \lim_{h \to 0} \frac{h \cdot \left\{ \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}}{h}",
            # 13. h 약분 표시 (h/h = 1)
            r"= \lim_{h \to 0} \frac{1 \cdot \left\{ \sum\limits_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}}{1}",
            # 14. h 약분 완료
            r"= \lim_{h \to 0} \left\{ \sum_{k=1}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 15. k=1 항 분리 (극한 계산 준비)
            r"= \lim_{h \to 0} \left\{ \binom{n}{1} \cdot x^{n-1} \cdot h^{1-1} + \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 16. h 지수 계산 (k=1 항)
            r"= \lim_{h \to 0} \left\{ \binom{n}{1} \cdot x^{n-1} \cdot h^{0} + \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 17. h^0 계산 (k=1 항)
            r"= \lim_{h \to 0} \left\{ \binom{n}{1} \cdot x^{n-1} \cdot 1 + \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 18. 곱셈항 1 제거 (k=1 항)
            r"= \lim_{h \to 0} \left\{ \binom{n}{1} \cdot x^{n-1} + \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 19. 극한 분리 (합의 극한 = 극한의 합)
            r"= \lim_{h \to 0} \left\{ \binom{n}{1} \cdot x^{n-1} \right\} + \lim_{h \to 0} \left\{ \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 20. 첫 번째 항 극한 계산 (h 무관)
            r"= \binom{n}{1} \cdot x^{n-1} + \lim_{h \to 0} \left\{ \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 21. 이항 계수 계산 (\binom{n}{1} = n)
            r"= n \cdot x^{n-1} + \lim_{h \to 0} \left\{ \sum_{k=2}^{n} \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\}",
            # 22. 극한을 유한 합 안으로 이동
            r"= n \cdot x^{n-1} + \sum_{k=2}^{n} \left[ \lim_{h \to 0} \left\{ \binom{n}{k} \cdot x^{n-k} \cdot h^{k-1} \right\} \right]",
            # 23. h와 무관한 항 분리
            r"= n \cdot x^{n-1} + \sum_{k=2}^{n} \left[ \left\{ \binom{n}{k} \cdot x^{n-k} \right\} \cdot \lim_{h \to 0} h^{k-1} \right]",
            # 24. h^(k-1) 극한 계산 (k>=2 이므로 k-1>=1)
            r"= n \cdot x^{n-1} + \sum_{k=2}^{n} \left[ \left\{ \binom{n}{k} \cdot x^{n-k} \right\} \cdot 0 \right]",
            # 25. 합 내부 항 단순화 (0)
            r"= n \cdot x^{n-1} + \sum_{k=2}^{n} 0",
            # 26. 0의 합 계산
            r"= n \cdot x^{n-1} + 0",
            # 27. 최종 결과
            r"= n \cdot x^{n-1}",
        ]

        return steps
