import inspect
import ast
import logging
from typing import Callable, Dict, Any, Optional

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FunctionInfo:
    """함수/메서드의 기본 정보를 분석하고 저장하는 클래스"""

    def __init__(self, func: Callable):
        """
        Args:
            func: 분석할 함수 객체
        """
        self.func = func
        self.is_class_method = False
        self.is_bound_method = False
        self.is_static_method = False
        self.instance: Optional[Any] = None
        self.cls: Optional[type] = None
        self.source = ""

        # 기본 분석 수행
        self._analyze_function()
        # 위치 정보 설정
        self.location = self._get_location()

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
            source_file = inspect.getsourcefile(self.func)
            lines, start_line = inspect.getsourcelines(self.func)

            return {
                'start_line': start_line,
                'end_line': start_line + len(lines) - 1,
                'source': ''.join(lines)
            }
        except Exception as e:
            logger.error(f"Could not get function location: {e}")
            return {}

    def get_signature_info(self) -> Dict[str, Any]:
        """함수의 시그너처 정보를 추출"""
        try:
            sig = inspect.signature(self.func)
            source = inspect.getsource(self.func)
            tree = ast.parse(source)
            func_node = tree.body[0]  # 첫 번째 노드가 함수 정의일 것으로 가정

            return {
                'parameters': {
                    name: {
                        'kind': str(param.kind),
                        'default': str(param.default) if param.default is not param.empty else None,
                        'annotation': str(param.annotation) if param.annotation is not param.empty else None
                    }
                    for name, param in sig.parameters.items()
                },
                'return_annotation': str(sig.return_annotation) if sig.return_annotation is not inspect.Signature.empty else None,
                'relative_location': self._get_signature_location(func_node)
            }
        except Exception as e:
            logger.error(f"Failed to get signature info: {e}")
            return {}

    def _get_signature_location(self, func_node: ast.FunctionDef) -> Dict[str, Any]:
        """함수 시그너처의 위치 정보를 추출"""
        try:
            if func_node.decorator_list:
                sig_start_line = func_node.decorator_list[-1].end_lineno + 1
            else:
                sig_start_line = func_node.lineno

            sig_source = self._extract_signature_text(func_node)
            sig_lines = sig_source.count('\n') + 1
            sig_end_line = sig_start_line + (sig_lines - 1)

            return {
                'start_line': sig_start_line,
                'end_line': sig_end_line,
                'source': sig_source
            }
        except Exception as e:
            logger.error(f"Failed to get signature location: {e}")
            return {}

    def _extract_signature_text(self, func_node: ast.FunctionDef) -> str:
        """함수 시그너처 텍스트를 추출"""
        try:
            source_lines, first_line = inspect.getsourcelines(self.func)
            sig_text = []
            started = False
            paren_count = 0

            for line in source_lines:
                stripped = line.lstrip()
                if not started and stripped.startswith('def '):
                    started = True

                if started:
                    sig_text.append(line)
                    paren_count += line.count('(') - line.count(')')
                    if paren_count == 0 and line.rstrip().endswith(':'):
                        break

            sig_text[-1] = sig_text[-1].rstrip()[:-1]
            return ''.join(sig_text)
        except Exception as e:
            logger.error(f"Failed to extract signature text: {e}")
            return ""
