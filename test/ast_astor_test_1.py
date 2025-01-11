from typing import Union, List, Any
from common.decorator.function_transformer import add_func_call_after_assign


def print_var(var: Union[Any, List[Any]], source: str):
    """
    대입문의 값을 출력하는 콜백 함수

    Args:
        var: 대입된 값 (일반 값 또는 리스트)
        source: 대입문의 소스 코드
    """
    if isinstance(var, list):
        print(f"리스트 대입문 발견!")
        print(f"리스트 참조: {var}")
        print(f"소스 코드: {source}")
        print(f"리스트 요소들: {', '.join(map(str, var))}")
    else:
        print(f"일반 대입문:")
        print(f"변수 값: {var}")
        print(f"소스 코드: {source}")


def test_expr() -> str:
    f_expr = "f(x) = x^2"
    return f_expr


def test_list_expr() -> str:
    exprs = [
        "f(x)",
        "=",
        "x^2"
    ]
    f_expr = " ".join(exprs)
    return f_expr


def test_list_expr_with_arg(exp: int) -> str:
    exprs = [
        "f(x)",
        "=",
        f"x^{exp}"
    ]
    f_expr = " ".join(exprs)
    return f_expr


def test_multiple_args(base: int, power: int, prefix: str = "f", suffix: str = "") -> str:
    exprs = [
        f"{prefix}(x)",
        "=",
        f"x^{power} + {base}",
        suffix
    ]
    f_expr = " ".join(filter(bool, exprs))
    return f_expr


def test_complex_args(
    coefficients: list[float],
    variables: list[str],
    *additional_terms,
    operation: str = "+",
    **named_constants
) -> str:
    terms = []
    for coef, var in zip(coefficients, variables):
        terms.append(f"{coef}{var}")

    terms.extend(additional_terms)

    for name, value in named_constants.items():
        terms.append(f"{name}={value}")

    f_expr = f" {operation} ".join(terms)
    return f_expr


class MathExpression:
    DEFAULT_BASE = 0

    def __init__(self, base: int = 0):
        self.base = base
        self.variables = ['x', 'y', 'z']

    def create_expression(self, power: int) -> str:
        exprs = [
            "f(x)",
            "=",
            f"x^{power} + {self.base}"  # self 참조 사용
        ]
        f_expr = " ".join(exprs)
        return f_expr

    def create_complex(self) -> str:
        exprs = [var for var in self.variables]  # 인스턴스 변수 사용
        return " + ".join(exprs)

    @staticmethod
    def create_power_expr(base: int, power: int) -> str:
        # self 없이 동작하는 정적 메서드
        return f"f(x) = x^{power} + {base}"

    @classmethod
    def create_default_expr(cls, power: int) -> str:
        # cls를 첫 번째 인자로 받는 클래스 메서드
        return cls.create_power_expr(cls.DEFAULT_BASE, power)


if __name__ == "__main__":
    # 리스트 대입문 테스트
    modified_func = add_func_call_after_assign(test_list_expr, print_var)
    result = modified_func()
    print(f"\n최종 반환값: {result}")

    # 인자가 있는 함수 테스트
    modified_func = add_func_call_after_assign(
        test_list_expr_with_arg, print_var)
    result = modified_func(3)  # 인자 전달
    print(f"\n최종 반환값: {result}")

    # 여러 인자를 가진 함수 테스트
    print("\n다중 인자 테스트:")
    modified_func = add_func_call_after_assign(test_multiple_args, print_var)
    result = modified_func(5, 2, prefix="g", suffix="+ c")
    print(f"최종 반환값: {result}")

    # 복잡한 인자 구조를 가진 함수 테스트
    print("\n복잡한 인자 테스트:")
    modified_func = add_func_call_after_assign(test_complex_args, print_var)
    result = modified_func(
        [2, 3],
        ['x', 'y'],
        'z^2',
        'sin(x)',
        operation='*',
        alpha=0.5,
        beta=1.0
    )
    print(f"최종 반환값: {result}")

    # 클래스 메서드 테스트
    print("\n클래스 메서드 테스트:")
    math_exp = MathExpression(base=5)
    try:
        modified_method = add_func_call_after_assign(
            math_exp.create_expression, print_var)
        result = modified_method(2)
        print(f"최종 반환값: {result}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 정적 메서드 테스트
    print("\n정적 메서드 테스트:")
    try:
        modified_method = add_func_call_after_assign(
            MathExpression.create_power_expr, print_var)
        result = modified_method(3, 2)
        print(f"최종 반환값: {result}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 클래스 메서드 테스트
    print("\n클래스 메서드 테스트:")
    try:
        modified_method = add_func_call_after_assign(
            MathExpression.create_default_expr, print_var)
        result = modified_method(2)
        print(f"최종 반환값: {result}")
    except Exception as e:
        print(f"에러 발생: {e}")
