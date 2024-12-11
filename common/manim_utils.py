from typing import Optional
from manim import *


def format_number(number, precision=5):
    """
    Formats a number to string with given precision and removes trailing zeros

    Args:
        number: Number to format (float or int)
        precision: Number of decimal places (default: 5)

    Returns:
        Formatted string without trailing zeros
    """
    return f"{float(number):.{precision}f}".rstrip('0').rstrip('.')


def create_vertical_dash(plane, x_value, y_range=None, color=BLUE_C, opacity=0.3, dash_length=0.1):
    """
    Creates a vertical dashed line on a given plane

    Args:
        plane: Manim plane object
        x_value: x-coordinate where the vertical line should be drawn
        y_range: Optional range for y-axis. If None, uses plane's y_range
        color: Color of the dashed line
        opacity: Opacity of the line (0 to 1)
        dash_length: Length of each dash

    Returns:
        DashedLine object
    """
    if y_range is None:
        y_range = plane.y_range
    return DashedLine(
        start=plane.c2p(x_value, y_range[0]),
        end=plane.c2p(x_value, y_range[1]),
        color=color,
        stroke_opacity=opacity,
        dash_length=dash_length
    )


def create_code_block_from_file(
        file_path: str,
        tab_width: int = 4,
        font_size: int = 24,
        background: str = "window",
        language: str = "python",
        style: str = "monokai",
        insert_line_no: bool = True) -> Optional[Code]:
    """
    Utility function to create a Manim Code object from a source file.

    Args:
        file_path: Path to the source code file
        tab_width: Indentation width (default: 4)
        background: Background style (default: "window")
        language: Programming language for syntax highlighting (default: "python")
        style: Code style for syntax highlighting (default: "monokai")
        insert_line_no: Whether to show line numbers (default: True)

    Returns:
        Code: Manim Code object for animation

    Raises:
        FileNotFoundError: If source file does not exist
    """
    try:
        # Read source file content
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()

        # Create and return Code object with syntax highlighting
        return Code(
            code=code_content,
            tab_width=tab_width,
            font_size=font_size,
            background=background,
            language=language,
            font="Monospace",
            style=style,
            insert_line_no=insert_line_no
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file at path: {file_path}")
    except Exception as e:
        print(f"Error creating code block: {str(e)}")
        return None
