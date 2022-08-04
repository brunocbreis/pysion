# helper functions
def fusion_coords(coords: tuple[int, int]) -> tuple[int, int]:
    """Converts x, y coords into Fusion flow scale"""
    x, y = coords
    return x * 110, y * 33


def fusion_point(x: float, y: float) -> str:
    return f"{{ {x}, {y} }}"


# tools and inputs creation
def add_tool(
    tool_id: str, tool_name: str, position: tuple[int, int] = (0, 0), inputs: str = ""
) -> str:
    """Creates a Fusion tool"""
    x, y = fusion_coords(position)
    tool = (
        f"\t\t{tool_name} = {tool_id} {{\n\t\t\tInputs = {{\t\t\t\t{inputs}\n\t\t\t}},"
        f"\n\t\t\tViewInfo = OperatorInfo {{ Pos = {{ {x}, {y} }} }},\n\t\t}},\n"
    )
    return tool


def add_inputs(**inputs: dict[str, float | int | str]) -> str:
    """Creates strings for adding inputs to Fusion tools"""

    result = ""
    for key, value in inputs.items():
        result += f"\n\t\t\t\t{key} = Input {{ Value = {value}, }},"

    return result


def add_source_input(input: str, tool_name: str, tool_output: str) -> str:
    """
    Creates string for tools that get Inputs from other tools,
    e.g from a Mask or a Spline
    """

    result = (
        f'\n\t\t\t\t{input} = Input {{\n\t\t\t\t\tSourceOp = "{tool_name}",'
        f'\n\t\t\t\t\tSource = "{tool_output}", }},'
    )
    return result


# animations
def add_spline(
    tool_name: str,
    input_name: str,
    spline_color: tuple[int, int, int] = (255, 0, 255),
    keyframes: str = "",
) -> str:
    """Creates a spline for an input in a tool."""
    r, g, b = spline_color

    spline = (
        f"\t\t{tool_name}{input_name} = BezierSpline {{\n\t\t\t"
        f"SplineColor = {{ Red = {r}, Green = {g}, Blue = {b} }},"
        f"\n\t\t\tKeyFrames = {{\n{keyframes}\t\t\t}}\n\t\t}},\n"
    )
    return spline


def add_keyframe_manual(
    frame: int,
    value: float,
    left_handle: tuple[float, float] = "",
    right_handle: tuple[float, float] = "",
) -> str:
    if left_handle:
        left_x, left_y = left_handle
        left_handle = f"LH = {{ {left_x}, {left_y} }}, "

    if right_handle:
        right_x, right_y = right_handle
        right_handle = f"RH = {{ {right_x}, {right_y} }} "

    kf = f"\t\t\t\t[{frame}] = {{ {value}, {left_handle}{right_handle}}},\n"

    return kf


def calc_ease_out(
    frames: tuple[int, int],
    values: tuple[float, float],
    intensity: float = 1 / 3,
) -> tuple[float, float]:
    """Returns the right handle coords of the first keyframe as a tuple (x, y)"""

    t0, t1 = frames
    v0, v1 = values

    x_offset = t0
    x_amp = t1 - t0

    x = x_offset + intensity * x_amp
    y = v0
    return x, y


def calc_ease_in(
    frames: tuple[int, int],
    values: tuple[float, float],
    intensity: float = 1 / 3,
) -> tuple[float, float]:
    """Returns the right handle coords of the first keyframe as a tuple (x, y)"""

    t0, t1 = frames
    v0, v1 = values

    x_offset = t0
    x_amp = t1 - t0

    x = t1 - intensity * x_amp
    y = v1
    return x, y


def animate(
    frames: tuple[int, int],
    values: tuple[float, float],
    ease: tuple[float, float] = (1 / 3, 1 / 3),
) -> str:
    """Creates eased keyframes"""
    ease_in = calc_ease_in(frames, values, ease[0])
    ease_out = calc_ease_out(frames, values, ease[1])

    kfs = add_keyframe_manual(
        frames[0], values[0], right_handle=ease_out
    ) + add_keyframe_manual(frames[1], values[1], left_handle=ease_in)

    return kfs


# wrapping
def wrap_for_fusion(tools: str, last_tool_name: str = "") -> str:
    """Adds header and footer to a sequence of tools"""

    header = "{\n\tTools = ordered() {\n"
    footer = f'\t}},\n\tActiveTool = "{last_tool_name}"\n}}'

    return header + tools + footer


# testing area
def test():

    tools = (
        add_tool(
            "RectangleMask", "SquareMask", (1, 0), add_inputs(Width=0.09, Height=0.16)
        )
        + add_tool(
            "Background",
            "PinkBG",
            (0, 2),
            add_inputs(Width=1920, Height=1080, TopLeftRed=1, TopLeftBlue=0.5),
        )
        + add_tool(
            "Background",
            "BlackSquare",
            (1, 1),
            add_inputs(Width=1920, Height=1080)
            + add_source_input("EffectMask", "SquareMask", "Mask"),
        )
        + add_tool(
            "Merge",
            "Merge1",
            (1, 2),
            add_inputs(Size="1.5", Center=fusion_point(0.25, 0.25))
            + add_source_input("Background", "PinkBG", "Output")
            + add_source_input("Foreground", "BlackSquare", "Output")
            + add_source_input("Angle", "Merge1Angle", "Value"),
        )
        + add_spline(
            "Merge1", "Angle", keyframes=animate((0, 24), (180, 360), (0.75, 0.75))
        )
    )

    tools = wrap_for_fusion(tools, "Merge1")

    print(tools)


if __name__ == "__main__":
    test()
