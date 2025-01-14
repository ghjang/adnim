import sys
import types
import inspect
import ast
import astor
import logging
from typing import Callable, Any, Dict, Union, List, TypeVar, Optional, get_args

T = TypeVar('T')
# 콜백 함수 타입을 더 명확하게 정의
AssignValue = Union[Any, List[Any]]  # 일반 값 또는 리스트 값 전체
# (value: Any | list[Any], source: str) -> None
CallbackFunc = Callable[[AssignValue, str,
                         Dict[str, int]], None]  # location 정보 추가

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FunctionInfo:
    """함수/메서드 정보를 저장하는 클래스"""

    def __init__(self, func: Callable):
        self.func = func
        self.is_class_method = False
        self.is_bound_method = False
        self.is_static_method = False
        self.instance: Optional[Any] = None
        self.cls: Optional[type] = None
        self.source = ""
        self.location = self._get_location()
        self._analyze_function()

    def _analyze_function(self):
        """함수 타입을 분석하고 관련 정보를 설정"""
        try:
            if isinstance(self.func, classmethod):
                self.is_class_method = True
                self.cls = self.func.__get__(None, type)
                self.source = inspect.getsource(self.func.__func__)
            elif inspect.ismethod(self.func) and isinstance(self.func.__self__, type):
                self.is_class_method = True
                self.cls = self.func.__self__
                self.source = inspect.getsource(self.func.__func__)
            else:
                self.is_bound_method = hasattr(self.func, '__self__')
                self.is_static_method = isinstance(self.func, staticmethod)

                if self.is_bound_method:
                    self.instance = getattr(self.func, '__self__', None)
                    self.source = inspect.getsource(self.func.__func__)
                elif self.is_static_method:
                    self.source = inspect.getsource(self.func.__func__)
                else:
                    self.source = inspect.getsource(self.func)
        except OSError:
            # exec으로 생성된 함수의 경우 소스를 직접 생성
            self.source = self._create_simple_function_source()

    def _create_simple_function_source(self) -> str:
        """exec으로 생성된 함수를 위한 기본 소스 코드 생성"""
        func_name = self.get_func_name()
        return f"def {func_name}(*args, **kwargs):\n    return func(*args, **kwargs)"

    def get_func_name(self) -> str:
        """함수의 이름을 반환"""
        return (self.func.__func__.__name__
                if hasattr(self.func, '__func__')
                else self.func.__name__)

    def _get_location(self) -> Dict[str, Any]:
        """함수의 소스 코드 위치 정보를 반환"""
        try:
            # NOTE:
            # 함수가 포함된 소스 '.py' 파일 경로 정보는 별도 상위 '키'에서 저장하기 때문에
            # 이 정보에서는 중복해서 저장할 필요가 없음. 참고를 위해서 코드는 남김.
            source_file = inspect.getsourcefile(self.func)

            lines, start_line = inspect.getsourcelines(self.func)

            # AST를 통해 더 상세한 위치 정보 획득
            tree = ast.parse(''.join(lines))
            func_node = tree.body[0]  # 첫 번째 노드가 함수 정의일 것으로 가정

            return {
                # 'file': source_file,
                'start_line': start_line,
                'end_line': start_line + len(lines) - 1,
                'start_col': func_node.col_offset,
                'end_col': func_node.end_col_offset,
                'source': ''.join(lines)
            }
        except Exception as e:
            logger.exception(f"Could not get function location: {e}")
            return {}


class AssignmentVisitor(ast.NodeTransformer):
    """대입문을 변환하는 AST 방문자"""

    def __init__(self, callback_name: str):
        self.callback_name = callback_name
        self.source_lines: List[str] = []

    def set_source(self, source: str) -> None:
        """소스 코드 설정"""
        self.source_lines = source.splitlines()

    def get_node_source(self, node: ast.AST) -> str:
        """AST 노드의 소스 코드를 추출"""
        if not (hasattr(node, 'lineno') and hasattr(node, 'end_lineno')):
            return ""

        start = node.lineno - 1
        end = node.end_lineno

        lines = self.source_lines[start:end]
        return '\n'.join(line.strip() for line in lines)

    def visit_Assign(self, node):
        self.current_node = node  # 현재 처리 중인 노드 저장
        result = self._create_nodes(node)
        self.current_node = None  # 처리 완료 후 초기화
        return result

    def visit_FunctionDef(self, node):
        # 함수 정의 노드 방문
        self.generic_visit(node)
        return node

    def _get_target_ids(self, target: ast.AST) -> List[str]:
        """대입문의 타겟 변수 이름들을 추출"""
        if isinstance(target, ast.Name):
            return [target.id]
        elif isinstance(target, ast.Tuple):
            ids = []
            for elt in target.elts:
                if isinstance(elt, ast.Name):
                    ids.append(elt.id)
            return ids
        return []

    def _create_nodes(self, node) -> list:
        """노드 변환 로직"""
        result_nodes = [node]
        source_text = self.get_node_source(node)

        # 모든 타겟 변수에 대해 콜백 생성 (리스트도 전체를 한번에 전달)
        for target in node.targets:
            for var_name in self._get_target_ids(target):
                result_nodes.append(
                    self._create_callback_node(var_name, source_text))

        return result_nodes

    def _create_callback_node(self, var_name: str, source_text: str) -> ast.Expr:
        """콜백 함수 호출 노드 생성"""
        # 현재 대입문 노드의 위치 정보
        location = {
            'start_line': self.current_node.lineno,
            'end_line': self.current_node.end_lineno
        }

        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id=self.callback_name, ctx=ast.Load()),
                args=[
                    ast.Name(id=var_name, ctx=ast.Load()),
                    ast.Constant(value=source_text),
                    ast.Dict(
                        keys=[ast.Constant(value=k) for k in location.keys()],
                        values=[ast.Constant(value=v) for v in location.values()]
                    )
                ],
                keywords=[]
            )
        )


class RemoveDecoratorTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # 데코레이터 리스트를 비움
        node.decorator_list = []
        return node


def add_func_call_after_assign(
    func_to_modify: Callable,
    callback_func: CallbackFunc
) -> Callable:
    """
    함수/메서드의 모든 대입문 다음에 콜백 함수를 호출하도록 변환합니다.

    Args:
        func_to_modify: 변환할 함수 또는 메서드
        callback_func: 대입문 다음에 호출될 콜백 함수.
                     시그너처: (value: Union[Any, List[Any]], source: str) -> None

    Returns:
        변환된 함수를 반환합니다.

    Notes:
        - 이 함수는 @staticmethod, @classmethod를 제외한 커스텀 데코레이터를 지원하지 않습니다.
        - 커스텀 데코레이터가 적용된 함수를 변환하면 해당 데코레이터의 기능은 무시됩니다.
        - 대상 함수에 커스텀 데코레이터가 필요한 경우, 변환된 함수를 다시 데코레이터로 감싸서 사용해야 합니다.

    Examples:
        >>> @my_decorator  # 이 데코레이터는 무시됨
        >>> def test_func():
        ...     x = 42
        ...     return x
        ...
        >>> modified = add_func_call_after_assign(test_func, callback)
        >>> # 필요한 경우 다음과 같이 다시 적용
        >>> modified = my_decorator(modified)
    """
    # 함수 분석
    func_info = FunctionInfo(func_to_modify)

    # 소스 코드 들여쓰기 처리
    func_info.source = _normalize_indentation(func_info.source)

    # AST 변환 및 코드 생성
    modified_source = _transform_source(
        func_info.source, callback_func.__name__)

    # 실행 컨텍스트 준비
    namespace = _prepare_namespace(callback_func, func_info, modified_source)

    # 변환된 함수 실행을 위한 래퍼 생성
    return _create_wrapper(func_info, namespace)


def _transform_source(source: str, callback_name: str) -> str:
    """소스 코드 AST 변환"""
    tree = ast.parse(source)

    # 데코레이터 제거
    tree = RemoveDecoratorTransformer().visit(tree)

    # 대입문 변환
    transformer = AssignmentVisitor(callback_name)
    transformer.set_source(source)
    modified_tree = transformer.visit(tree)

    ast.fix_missing_locations(modified_tree)
    return astor.to_source(modified_tree)


def _prepare_namespace(callback_func: Callable, func_info: FunctionInfo, modified_source: str) -> Dict:
    """실행을 위한 네임스페이스 준비"""
    namespace = {
        callback_func.__name__: callback_func,
        callback_func.__qualname__: callback_func,
        'func': func_info.func  # 원본 함수를 네임스페이스에 추가
    }

    if hasattr(func_info.func, '__module__'):
        try:
            module = sys.modules[func_info.func.__module__]
            module_dict = {k: v for k, v in module.__dict__.items()
                           if not k.startswith('_')}
            namespace.update(module_dict)
        except (KeyError, AttributeError):
            pass

    if func_info.is_class_method:
        namespace['cls'] = func_info.cls
    elif func_info.is_bound_method:
        namespace['self'] = func_info.instance

    globals_copy = globals().copy()
    globals_copy.update(namespace)

    exec(modified_source, globals_copy, namespace)
    return namespace


def _normalize_indentation(source: str) -> str:
    """소스 코드의 들여쓰기를 정규화"""
    lines = source.splitlines()
    first_line = lines[0]
    indent = len(first_line) - len(first_line.lstrip())
    return '\n'.join(
        line[indent:] if line[:indent].isspace() else line
        for line in lines
    )


def _create_wrapper(func_info: FunctionInfo, namespace: Dict) -> Callable:
    """함수 타입에 따른 적절한 래퍼 함수 생성"""
    def wrapper(*args, **kwargs):
        func_name = func_info.get_func_name()

        if func_info.is_class_method:
            method = classmethod(namespace[func_name])
            return method.__get__(None, func_info.cls)(*args, **kwargs)
        elif func_info.is_bound_method:
            method = types.MethodType(namespace[func_name], func_info.instance)
            return method(*args, **kwargs)
        elif func_info.is_static_method:
            return namespace[func_name](*args, **kwargs)
        else:
            return namespace[func_name](*args, **kwargs)

    return wrapper
