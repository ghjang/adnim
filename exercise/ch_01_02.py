from collections import Counter
from typing import List

"""
TODO:
- 'divmod' 함수를 사용하는 등의 방법으로 성능 개선 포인트가 있는지 확인해보기

NOTE:
정리: n의 합성수 인수가 있다면, √n 이하의 소인수가 반드시 존재

증명:
    1. n이 합성수라고 가정 (n = a x b)
    2. a, b 모두 1보다 큰 수
    3. 만약 a, b 모두 √n보다 크다면:
        * a > √n 이고 b > √n 이면
        * n = a x b > √n x √n = n
        * 모순!
    4. 따라서 a, b 중 적어도 하나는 √n 이하

결론:
    - n의 모든 소인수를 찾을 때는 √n까지만 검사하면 충분함.
      위 증명에 의해서 최대 소인수는 √n인 상황임.
      2개의 소인수중에 하나가 √n이면, 다른 소인수 역시 √n이 될 수밖에 없음.
    - √n 이하의 수에서 소인수를 찾지 못했을 경우는 n 자체가 소수인 경우임.
"""


def factorize(n: int) -> List[int]:
    """정수를 소인수분해하여 소인수들의 리스트를 반환

    Args:
        n (int): 소인수분해할 양의 정수

    Returns:
        List[int]: 소인수들의 리스트
    """
    factors = []

    # 1은 소수가 아니므로 2부터 시작
    factor = 2

    # √n 까지만 검사
    while factor * factor <= n:
        while n % factor == 0:
            factors.append(factor)
            n //= factor
        factor += 1

    # 남은 수가 1보다 크면 n 자체가 소수
    if n > 1:
        factors.append(n)

    return factors


def factors_to_latex(factors: List[int]) -> str:
    """소인수분해 결과 리스트를 LaTeX 거듭제곱 표현 문자열로 변환

    Args:
        factors (List[int]): factorize 함수로 구한 소인수 리스트

    Returns:
        str: LaTeX 형식의 거듭제곱 표현 문자열
    """
    if not factors:
        return ''

    factor_counts = Counter(factors)

    # 각 인수를 LaTeX 거듭제곱 형식으로 변환
    latex_terms = []
    for factor, count in sorted(factor_counts.items()):
        if count == 1:
            latex_terms.append(str(factor))
        else:
            latex_terms.append(f'{factor}^{{{count}}}')

    # 모든 항을 \cdot으로 연결
    return r' \cdot '.join(latex_terms)
