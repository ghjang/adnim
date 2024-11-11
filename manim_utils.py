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