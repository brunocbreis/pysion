from .curves import Curve


def add_spline(
    tool_name: str,
    input_name: str,
    animation: Curve,
    spline_color: tuple[int, int, int] = (255, 0, 255),
) -> str:
    """Creates a spline for an input in a tool."""
    r, g, b = spline_color
    keyframes = animation.generate()
    spline = (
        f"\t\t{tool_name}{input_name} = BezierSpline {{\n\t\t\t"
        f"SplineColor = {{ Red = {r}, Green = {g}, Blue = {b} }},"
        f"\n\t\t\tKeyFrames = {{\n{keyframes}\t\t\t}}\n\t\t}},\n"
    )
    return spline


def add_spline_input(tool_name: str, input: str) -> str:

    result = (
        f'\n\t\t\t\t{input} = Input {{\n\t\t\t\t\tSourceOp = "{tool_name + input}",'
        f'\n\t\t\t\t\tSource = "Value", }},'
    )
    return result
