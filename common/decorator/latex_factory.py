import sympy as sp
import json
import logging
from pathlib import Path
from functools import wraps
from typing import Callable, Dict, Any, Union
import datetime
from json.decoder import JSONDecodeError
import os

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
        if json_path.exists():
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


def latex_factory(save_dir: Union[str, Path, None] = None) -> Callable:
    """
    A decorator that saves LaTeX strings or SymPy expressions to JSON file.
    When save_dir is None and ENV_VAR_NAME is not set, acts as a pass-through decorator.

    Args:
        save_dir: Directory path to save JSON file. If None, checks environment variable
                 first, only passes through if environment variable is also not set.
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
                    return func(*args, **kwargs)
                return wrapper
            return simple_decorator

    # Ensure save directory exists
    try:
        save_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
        raise RuntimeError(f"Failed to create directory: {save_path}")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Initialize data dict
            data = {}
            json_path = save_path / JSON_FILENAME

            try:
                # Execute function and convert result
                result = func(*args, **kwargs)

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

                # Update data and save
                data[func.__name__] = entry
                save_json_data(json_path, data)

                return result

            except Exception as e:
                logger.error(f"Decorator execution failed: {e}")
                try:
                    # Load existing data for error entry
                    data = load_json_data(json_path)
                    data[func.__name__] = {
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
