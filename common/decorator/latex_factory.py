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


def print_latex_var(var: Any, source: str):
    """LaTeX 관련 변수 출력을 위한 콜백 함수"""
    print(f"\nLatex Factory Variable:")
    print(f"Value: {var}")
    print(f"Source: {source}")
    if isinstance(var, sp.Basic):
        print(f"LaTeX: {sp.latex(var)}")


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

    def decorator(func: Callable) -> Callable:
        # 변환된 함수 생성
        transformed_func = add_func_call_after_assign(func, print_latex_var)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Initialize data dict
            data = {}
            json_path = save_path / JSON_FILENAME if save_path else None

            try:
                # Get the file path of the decorated function
                file_path = os.path.abspath(func.__code__.co_filename)

                # 변환된 함수 호출
                result = transformed_func(*args, **kwargs)

                # 나머지 로직은 그대로 유지
                if json_path:
                    # Load existing data before modification
                    data = load_json_data(json_path)

                    # Convert result to LaTeX
                    latex_str = convert_to_latex(result)

                    # Prepare entry data
                    entry = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'latex': latex_str
                    }

                    # Add args and kwargs only if they exist
                    if args:
                        entry['args'] = str(args)
                    if kwargs:
                        entry['kwargs'] = str(kwargs)

                    # Initialize file path in data if not exists
                    if file_path not in data:
                        data[file_path] = {}

                    # Update data and save
                    data[file_path][func.__name__] = entry
                    save_json_data(json_path, data)

                return latex_str if auto_latex_str else result

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
