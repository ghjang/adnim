import sympy as sp
import json
import logging
from pathlib import Path
from functools import wraps
from typing import Callable, Dict, Any, Union, Optional
import datetime
from json.decoder import JSONDecodeError
import os
from .function_transformer import (
    add_func_call_after_assign,
    FunctionInfo
)
from threading import Lock
from contextlib import contextmanager
from typing import Generator
import inspect
import ast

# Configuration constants
DEFAULT_OUTPUT_DIR = "latex_outputs"
ENV_VAR_NAME = "LATEX_FACTORY_OUTPUT_DIR"
JSON_FILENAME = "latex_factory.json"

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_to_latex(result: Any) -> str:
    """Converts result to LaTeX string safely."""
    try:
        if isinstance(result, sp.Expr):
            return sp.latex(result)
        return str(result)
    except Exception as e:
        logger.error(f"LaTeX conversion failed: {e}")
        return "LaTeX conversion failed"


def load_json_data(json_path: Path) -> Dict[str, Any]:
    """Loads existing JSON data or returns empty dict."""
    try:
        if (json_path.exists()):
            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except JSONDecodeError as e:
                    logger.error(f"Corrupted JSON file: {e}")
    except Exception as e:
        logger.error(f"Failed to read JSON file: {e}")
    return {}


def save_json_data(json_path: Path, data: Dict[str, Any]) -> None:
    """Saves data to JSON file safely."""
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save JSON file: {e}")


class LatexFactory:
    def __init__(self, save_dir: Union[str, Path, None] = None, auto_latex_str: bool = True):
        """
        Args:
            save_dir: Directory path to save JSON file. If None, checks environment variable
                     first, then uses default directory.
            auto_latex_str: If True, returns LaTeX string instead of original function result.
        """
        # 설정값 저장
        self.auto_latex_str = auto_latex_str

        # 저장 디렉토리 결정
        if save_dir is not None:
            self.save_dir = Path(save_dir)
        else:
            env_dir = os.getenv(ENV_VAR_NAME)
            if env_dir:
                self.save_dir = Path(env_dir)
            else:
                self.save_dir = None  # pass-through 모드로 동작하도록 None 설정
                logger.info(
                    f"No save_dir specified and {ENV_VAR_NAME} not set. "
                    "Decorator will pass through function calls without saving outputs."
                )
                return  # 초기화 중단 - pass-through 모드

        # 저장 디렉토리 생성 (pass-through 모드가 아닐 때만)
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create directory: {e}")
            raise RuntimeError(f"Failed to create directory: {self.save_dir}")

        self.file_lock = Lock()
        self.config = self._load_config()

    @contextmanager
    def _file_access(self) -> Generator[None, None, None]:
        """Thread-safe file access context manager"""
        with self.file_lock:
            yield

    def _load_config(self):
        # Configuration loading logic here
        return {}

    def __call__(self, auto_latex_str: bool | None = None) -> Callable:
        """
        데코레이터 호출. auto_latex_str이 None이면 인스턴스의 기본값 사용
        """
        # 실제 사용할 auto_latex_str 값 결정
        effective_auto_latex_str = (
            self.auto_latex_str if auto_latex_str is None else auto_latex_str
        )

        # pass-through 모드 체크
        if self.save_dir is None:
            def simple_decorator(func: Callable) -> Callable:
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    return convert_to_latex(result) if effective_auto_latex_str else result
                return wrapper
            return simple_decorator

        # 정상 데코레이터 로직
        def decorator(func: Callable) -> Callable:
            # 함수 정보 객체 생성 (위치 정보 포함)
            func_info = FunctionInfo(func)
            # 대입문 데이터를 누적할 클로저 변수
            assignment_data = {'assignments': {}}

            def save_assignment_data(var: Any | list[Any], source: str, location: Dict[str, int]) -> None:
                try:
                    sanitized_key = self._sanitize_source_key(source)
                    sanitized_source = self._sanitize_source_code(source)

                    # 대입문 타입에 따라 메모리에 누적
                    location['source'] = sanitized_source
                    assign_entry = {
                        'type': 'list' if isinstance(var, list) else 'single',
                        'relative_location': location
                    }

                    if isinstance(var, list):
                        assign_entry['items'] = [
                            {'index': idx, 'latex': convert_to_latex(item)}
                            for idx, item in enumerate(var)
                        ]
                    else:
                        assign_entry['latex'] = convert_to_latex(var)

                    assignment_data['assignments'][sanitized_key] = assign_entry

                except Exception as e:
                    logger.error(f"Failed to save assignment data: {e}")
                    logger.error(f"Exception details:", exc_info=True)

            transformed_func = add_func_call_after_assign(
                func,
                save_assignment_data
            )

            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # 변환된 함수 호출
                    return_value = transformed_func(*args, **kwargs)

                    json_path = Path(self.save_dir) / \
                        JSON_FILENAME if self.save_dir else None

                    # 리턴값과 대입문 데이터를 함께 저장
                    if json_path:
                        with self._file_access():
                            data = load_json_data(json_path)
                            file_path = os.path.abspath(
                                func.__code__.co_filename)

                            if file_path not in data:
                                data[file_path] = {}

                            # 함수 데이터 준비 (순서 변경)
                            func_data = {
                                'timestamp': datetime.datetime.now().isoformat(),
                                'location': func_info.location,
                                'signature': func_info.get_signature_info(),
                                'arguments': {
                                    'args': [str(arg) for arg in args] if args else [],
                                    'kwargs': {k: str(v) for k, v in kwargs.items()} if kwargs else {}
                                },
                                'assignments': assignment_data.get('assignments', {}),
                                'return_latex': convert_to_latex(return_value)
                            }

                            # Add args and kwargs only if they exist
                            if args:
                                func_data['args'] = str(args)
                            if kwargs:
                                func_data['kwargs'] = str(kwargs)

                            # 전체 데이터 저장
                            data[file_path][func.__name__] = func_data
                            save_json_data(json_path, data)

                            # 다음 호출을 위해 대입문 데이터 초기화
                            assignment_data.clear()
                            assignment_data['assignments'] = {}

                    # 원본 함수의 리턴 타입을 보존하면서 latex 변환
                    if effective_auto_latex_str:
                        if isinstance(return_value, (str, sp.Expr)):
                            return convert_to_latex(return_value)
                        logger.warning(
                            f"Unexpected return type {type(return_value)} from {func.__name__}, "
                            "auto_latex_str will be ignored"
                        )
                    return return_value

                except Exception as e:
                    logger.error(f"Decorator execution failed: {e}")
                    try:
                        # Load existing data for error entry
                        with self._file_access():
                            data = load_json_data(json_path)
                            if file_path not in data:
                                data[file_path] = {}

                            # 오류 정보와 함께 assignments 데이터도 보존
                            data[file_path][func.__name__] = {
                                'timestamp': datetime.datetime.now().isoformat(),
                                'location': func_info.location,  # 오류 시에도 위치 정보 포함
                                'error': str(e),
                                'assignments': assignment_data.get('assignments', {})
                            }
                            save_json_data(json_path, data)
                    except Exception as save_error:
                        logger.error(
                            f"Failed to save error information: {save_error}")
                    raise e

            return wrapper
        return decorator

    def _sanitize_source_key(self, source: str) -> str:
        """소스 코드를 JSON 키로 사용하기 위한 전처리"""
        # 개행 문자를 \\n으로 변환
        source = source.replace('\n', '\\n')
        # 탭을 스페이스로 변환
        source = source.replace('\t', '    ')
        # 연속된 공백을 하나로
        source = ' '.join(source.split())
        return source

    def _sanitize_source_code(self, source: str) -> str:
        """소스 코드의 특수 문자를 JSON 저장에 적합하게 처리"""
        return source.replace('\n', '\\n').replace('\t', '\\t')


class FunctionInfo:
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
        # 순서 변경: _analyze_function을 먼저 호출하여 source 등의 정보를 설정
        self._analyze_function()
        # source 정보가 설정된 후에 location 정보 획득
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

    def _get_signature_location(self, func_node: ast.FunctionDef) -> Dict[str, Any]:
        """함수 시그너처의 위치 정보를 추출"""
        try:
            # 데코레이터가 있는 경우 시작 위치 조정
            if func_node.decorator_list:
                sig_start_line = func_node.decorator_list[-1].end_lineno + 1
            else:
                sig_start_line = func_node.lineno

            # Extract signature text
            sig_source = self._extract_signature_text(func_node)

            # 줄 수 계산
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
            # 전체 소스 코드 가져오기
            source_lines, first_line = inspect.getsourcelines(self.func)

            # 함수 정의 라인 찾기 (def로 시작하는 부분)
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

                    # 괄호가 닫히고 콜론이 나오면 시그너처 끝
                    if paren_count == 0 and line.rstrip().endswith(':'):
                        break

            # 마지막 콜론 제거
            sig_text[-1] = sig_text[-1].rstrip()[:-1]

            return ''.join(sig_text)

        except Exception as e:
            logger.error(f"Failed to extract signature text: {e}")
            return ""

    def get_signature_info(self) -> Dict[str, Any]:
        """함수의 시그너처 정보를 추출"""
        try:
            sig = inspect.signature(self.func)
            # AST를 통해 함수 노드 얻기
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
                # 시그너처 위치 정보 추가
                'relative_location': self._get_signature_location(func_node)
            }
        except Exception as e:
            logger.error(f"Failed to get signature info: {e}")
            return {}


# 전역 싱글톤 인스턴스 - 기본 디렉토리 사용
latex_factory = LatexFactory()
