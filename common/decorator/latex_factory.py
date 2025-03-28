import sympy as sp
import json
import logging
from pathlib import Path
from functools import wraps
from typing import Callable, Dict, Any, Union
import datetime
from json.decoder import JSONDecodeError
import os
from threading import Lock
from contextlib import contextmanager
from typing import Generator
from .function_info import FunctionInfo
from .function_transformer import add_func_call_after_assign

# Configuration constants
DEFAULT_OUTPUT_DIR = "latex_outputs"
ENV_VAR_NAME = "LATEX_FACTORY_OUTPUT_DIR"
JSON_FILENAME = "latex_factory.json"

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _escape_latex(s):
    # LaTeX 특수문자 이스케이프
    chars = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
    }
    return "".join(chars.get(c, c) for c in str(s))


def convert_to_latex(result: Any, include_mul_dot_symbol=True) -> str:
    """Converts result to LaTeX string safely."""
    try:
        if isinstance(result, (sp.Basic, sp.matrices.MatrixBase)):
            # mul_symbol='dot'를 사용하여 곱셈을 \cdot으로 표시
            latex_options = {"mul_symbol": "dot"} if include_mul_dot_symbol else {}
            return sp.latex(result, **latex_options)
        elif isinstance(result, (int, float)):
            return str(result)
        elif isinstance(result, bool):
            return r"\texttt{True}" if result else r"\texttt{False}"
        elif result is None:
            return r"\texttt{None}"
        elif isinstance(result, str):
            return result

        # 기타 일반 적인 '객체'등의 경우 처리
        return rf"\texttt{{{_escape_latex(result)}}}"
    except Exception as e:
        logger.error(f"LaTeX conversion failed: {e}")
        return "LaTeX conversion failed"


def load_json_data(json_path: Path) -> Dict[str, Any]:
    """Loads existing JSON data or returns empty dict."""
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
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
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save JSON file: {e}")


class LatexFactory:
    def __init__(self):
        """기본 초기화"""
        self.save_dir = None
        env_dir = os.getenv(ENV_VAR_NAME)
        if env_dir:
            self.save_dir = Path(env_dir)
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

    def __call__(
        self,
        save_dir: Union[str, Path, None] = None,
        auto_latex_str: bool = True,
        show_mul_dot: bool = True,
    ) -> Callable:
        """
        데코레이터 호출

        Args:
            save_dir: JSON 파일을 저장할 디렉토리 경로
            auto_latex_str: True면 LaTeX 문자열로 변환하여 반환
        """
        effective_save_dir = Path(save_dir) if save_dir else self.save_dir
        if effective_save_dir:
            try:
                effective_save_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create directory: {e}")
                effective_save_dir = None

        # pass-through 모드 체크
        if effective_save_dir is None:

            def simple_decorator(func: Callable) -> Callable:
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    return (
                        convert_to_latex(result, show_mul_dot)
                        if auto_latex_str
                        else result
                    )

                return wrapper

            return simple_decorator

        # 정상 데코레이터 로직
        def decorator(func: Callable) -> Callable:
            # 함수 정보 객체 생성 (위치 정보 포함)
            func_info = FunctionInfo(func)
            # 대입문 데이터를 누적할 클로저 변수
            assignment_data = {"assignments": {}}

            def save_assignment_data(
                var: Any | list[Any], source: str, location: Dict[str, int]
            ) -> None:
                try:
                    sanitized_key = self._sanitize_source_key(source)
                    sanitized_source = self._sanitize_source_code(source)

                    # 대입문 타입에 따라 메모리에 누적
                    location["source"] = sanitized_source
                    assign_entry = {
                        "type": "list" if isinstance(var, list) else "single",
                        "relative_location": location,
                    }

                    if isinstance(var, list):
                        assign_entry["items"] = []
                        for idx, item in enumerate(var):
                            if isinstance(item, dict) and "text" in item:
                                # 딕셔너리이고 'text' 키가 있는 경우, 'text' 키의 값만 추출
                                assign_entry["items"].append(
                                    {
                                        "index": idx,
                                        "latex": convert_to_latex(
                                            item["text"], show_mul_dot
                                        ),
                                    }
                                )
                            else:
                                # 일반적인 경우는 기존처럼 처리
                                assign_entry["items"].append(
                                    {
                                        "index": idx,
                                        "latex": convert_to_latex(item, show_mul_dot),
                                    }
                                )
                    else:
                        assign_entry["latex"] = convert_to_latex(var, show_mul_dot)

                    assignment_data["assignments"][sanitized_key] = assign_entry

                except Exception as e:
                    logger.error(f"Failed to save assignment data: {e}")
                    logger.error(f"Exception details:", exc_info=True)

            transformed_func = add_func_call_after_assign(func, save_assignment_data)

            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # 변환된 함수 호출
                    return_value = transformed_func(*args, **kwargs)

                    json_path = (
                        Path(effective_save_dir) / JSON_FILENAME
                        if effective_save_dir
                        else None
                    )

                    # 리턴값과 대입문 데이터를 함께 저장
                    if json_path:
                        with self._file_access():
                            data = load_json_data(json_path)
                            file_path = os.path.abspath(func.__code__.co_filename)

                            if file_path not in data:
                                data[file_path] = {}

                            # 함수 데이터 준비 (순서 변경)
                            func_data = {
                                "timestamp": datetime.datetime.now().isoformat(),
                                "location": func_info.location,
                                "signature": func_info.get_signature_info(),
                                "arguments": {
                                    "args": [str(arg) for arg in args] if args else [],
                                    "kwargs": (
                                        {k: str(v) for k, v in kwargs.items()}
                                        if kwargs
                                        else {}
                                    ),
                                },
                                "assignments": assignment_data.get("assignments", {}),
                                "return_latex": convert_to_latex(
                                    return_value, show_mul_dot
                                ),
                            }

                            # 전체 데이터 저장
                            data[file_path][func.__name__] = func_data
                            save_json_data(json_path, data)

                            # 다음 호출을 위해 대입문 데이터 초기화
                            assignment_data.clear()
                            assignment_data["assignments"] = {}

                    # 원본 함수의 리턴 타입을 보존하면서 latex 변환
                    if auto_latex_str:
                        is_convertible = (
                            isinstance(
                                return_value,
                                (
                                    str,
                                    sp.Basic,
                                    sp.matrices.MatrixBase,
                                    int,
                                    float,
                                    bool,
                                ),
                            )
                            or return_value is None
                        )
                        if is_convertible:
                            return convert_to_latex(return_value, show_mul_dot)
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
                                "timestamp": datetime.datetime.now().isoformat(),
                                "location": func_info.location,  # 오류 시에도 위치 정보 포함
                                "error": str(e),
                                "assignments": assignment_data.get("assignments", {}),
                            }
                            save_json_data(json_path, data)
                    except Exception as save_error:
                        logger.error(f"Failed to save error information: {save_error}")
                    raise e

            return wrapper

        return decorator

    def _sanitize_source_key(self, source: str) -> str:
        """소스 코드를 JSON 키로 사용하기 위한 전처리"""
        # 개행 문자를 \\n으로 변환
        source = source.replace("\n", "\\n")
        # 탭을 스페이스로 변환
        source = source.replace("\t", "    ")
        # 연속된 공백을 하나로
        source = " ".join(source.split())
        return source

    def _sanitize_source_code(self, source: str) -> str:
        """소스 코드의 특수 문자를 JSON 저장에 적합하게 처리"""
        return source.replace("\n", "\\n").replace("\t", "\\t")


# 전역 싱글톤 인스턴스 - 기본 디렉토리 사용
latex_factory = LatexFactory()
