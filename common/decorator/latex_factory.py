import sympy as sp
import json
import logging
from pathlib import Path
from functools import wraps
from typing import Callable, Dict, Any, Union
import datetime
from json.decoder import JSONDecodeError
import os
from .function_transformer import add_func_call_after_assign

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


def latex_factory(save_dir: Union[str, Path, None] = None, auto_latex_str: bool = True) -> Callable:
    """
    A decorator that saves LaTeX strings or SymPy expressions to JSON file.
    When save_dir is None and ENV_VAR_NAME is not set, acts as a pass-through decorator.

    Args:
        save_dir: Directory path to save JSON file. If None, checks environment variable
                 first, only passes through if environment variable is also not set.
        auto_latex_str: If True, returns LaTeX string instead of original function result.
    """
    # Determine the save directory
    save_path = None
    if save_dir is not None:
        save_path = Path(save_dir)
    else:
        env_dir = os.getenv(ENV_VAR_NAME)
        if env_dir:
            save_path = Path(env_dir)
        else:
            logger.info(
                f"No save_dir specified and {ENV_VAR_NAME} not set. "
                "Decorator will pass through function calls without saving outputs."
            )

            def simple_decorator(func: Callable) -> Callable:
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    return convert_to_latex(result) if auto_latex_str else result
                return wrapper
            return simple_decorator

    # Ensure save directory exists
    try:
        save_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
        raise RuntimeError(f"Failed to create directory: {save_path}")

    def _sanitize_source_key(source: str) -> str:
        """소스 코드를 JSON 키로 사용하기 위한 전처리"""
        # 개행 문자를 \\n으로 변환
        source = source.replace('\n', '\\n')
        # 탭을 스페이스로 변환
        source = source.replace('\t', '    ')
        # 연속된 공백을 하나로
        source = ' '.join(source.split())
        return source

    def _sanitize_source_code(source: str) -> str:
        """소스 코드의 특수 문자를 JSON 저장에 적합하게 처리"""
        return source.replace('\n', '\\n').replace('\t', '\\t')

    def decorator(func: Callable) -> Callable:
        # 대입문 데이터를 누적할 클로저 변수
        assignment_data = {'assignments': {}}

        def save_assignment_data(var: Any | list[Any], source: str) -> None:
            try:
                sanitized_key = _sanitize_source_key(source)
                sanitized_source = _sanitize_source_code(source)

                # 대입문 타입에 따라 메모리에 누적
                if isinstance(var, list):
                    # 리스트 대입문인 경우
                    assignment_data['assignments'][sanitized_key] = {
                        'type': 'list',
                        'source': sanitized_source,
                        'items': [
                            {'index': idx, 'latex': convert_to_latex(item)}
                            for idx, item in enumerate(var)
                        ]
                    }
                else:
                    # 일반 대입문인 경우
                    assignment_data['assignments'][sanitized_key] = {
                        'type': 'single',
                        'source': sanitized_source,
                        'latex': convert_to_latex(var)
                    }

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

                json_path = save_path / JSON_FILENAME if save_path else None

                # 리턴값과 대입문 데이터를 함께 저장
                if json_path:
                    data = load_json_data(json_path)
                    file_path = os.path.abspath(func.__code__.co_filename)

                    if file_path not in data:
                        data[file_path] = {}

                    # 함수 데이터 준비
                    func_data = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'return_latex': convert_to_latex(return_value)
                    }

                    # 누적된 대입문 데이터 병합
                    func_data.update(assignment_data)

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

                return convert_to_latex(return_value) if auto_latex_str else return_value

            except Exception as e:
                logger.error(f"Decorator execution failed: {e}")
                try:
                    # Load existing data for error entry
                    data = load_json_data(json_path)
                    if file_path not in data:
                        data[file_path] = {}
                    data[file_path][func.__name__] = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'error': str(e)
                    }
                    save_json_data(json_path, data)
                except Exception as save_error:
                    logger.error(
                        f"Failed to save error information: {save_error}")
                raise e

        return wrapper
    return decorator
