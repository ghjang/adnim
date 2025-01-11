import inspect
import ast


def print_ast(node, level=0):
    indent = '  ' * level
    print(f"{indent}{type(node).__name__}")

    # 함수 정의를 처리할 때 반환 타입 확인
    if isinstance(node, ast.FunctionDef):
        if node.returns:
            print(f"{indent}  returns: {ast.unparse(node.returns)}")

    # 필드 출력
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    print(f"{indent}  {field}:")
                    print_ast(item, level + 2)
        elif isinstance(value, ast.AST):
            print(f"{indent}  {field}:")
            print_ast(value, level + 1)
        else:
            print(f"{indent}  {field}: {value}")


def empty_function():
    pass


source = inspect.getsource(empty_function)
tree = ast.parse(source)
print_ast(tree)

print()


def str_function() -> str:
    return "Hello, World!"


source = inspect.getsource(str_function)
tree = ast.parse(source)
print_ast(tree)


def test_expr() -> str:
    f_expr = "f(x) = x^2"
    return f_expr


# # 테스트용 함수 - 타입 어노테이션 포함
# def test_function(x: int, y: str) -> float:
#     result: float = float(x)
#     return result

# # 테스트 실행
# source = inspect.getsource(test_function)
# tree = ast.parse(source)
# print("AST 구조 분석 결과:")
# print_ast(tree)

# def sample_function():
#     numbers = [1, 2, 3, 4, 5]
#     total = 0
#     for num in numbers:
#         total += num
#     return total
