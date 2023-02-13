from .utils import fusion_coords, fusion_point, fusion_string
from typing import Literal


def generate_input(
    name: str,
    value: int | float | str | None = None,
    expression: str | None = None,
    indent_level: int = 4,
) -> str:
    ind = indent_level * "\t"

    if type(value) is str:
        value = fusion_string(value)

    input_content: str = ""

    if value and expression:
        input_content += (
            f"\n"
            f"{ind}\tValue = {value},\n"
            f"{ind}\tExpression = {fusion_string(expression)},\n"
            f"{ind}"
        )
        return f"{ind}{name.capitalize()} = Input {{ {input_content} }},"

    if value and not expression:
        input_content = f"Value = {value},"
        return f"{ind}{name.capitalize()} = Input {{ {input_content} }},"

    if expression:
        return f"{ind}{name.capitalize()} = Input {{ {input_content} }},"

    raise ValueError("Inputs must have at least a value or an expression.")


# Tool
def generate_tool(
    tool_id: str, tool_name: str, inputs: str = "", position: tuple[int, int] = (0, 0)
) -> str:
    """Creates a Fusion tool"""

    tool = (
        f"\t\t{tool_name} = {tool_id} {{\n\t\t\tInputs = {{\t\t\t\t{inputs}\n\t\t\t}},"
        f"\n\t\t\t{_view_info(position)}\n\t\t}},\n"
    )
    return tool


def _view_info(position: tuple[int, int] = (0, 0)) -> str:
    x, y = fusion_coords(position)
    return f"ViewInfo = OperatorInfo {{ Pos = {fusion_point(x,y)} }},"


# Inputs
def generate_inputs(
    type: Literal["Value", "Expression"] = "Value",
    **inputs: dict[str, float | int | str],
) -> str:
    """Creates strings for adding inputs to Fusion tools"""

    result = ""
    for key, value in inputs.items():
        result += f"\n\t\t\t\t{key} = Input {{ {type} = {value}, }},"

    return result


def generate_source_input(
    input: str, tool_name: str, tool_output: str = "Output"
) -> str:
    """
    Creates string for tools that get Inputs from other tools,
    e.g from a Mask or to a Merge
    """

    result = (
        f'\n\t\t\t\t{input} = Input {{\n\t\t\t\t\tSourceOp = "{tool_name}",'
        f'\n\t\t\t\t\tSource = "{tool_output}",\n\t\t\t\t}},'
    )
    return result


def generate_mask(mask_name: str) -> str:
    return generate_source_input("EffectMask", mask_name, "Mask")


# Instances for macros
def generate_instance_input(
    instance_name: str,
    source_op: str,
    source_input: str,
    default: str | int | float = "",
    **inputs,
) -> str:
    if default:
        if type(default) is str:
            default = f'\n\t\t\t\t\tDefault = "{default}",'
        else:
            default = f"\n\t\t\t\t\tDefault = {default},"

    if inputs:
        inps = "".join(
            [
                f'\n\t\t\t\t\t{k} = "{v}",'
                if type(v) is str
                else f"\n\t\t\t\t\t{k} = {v},"
                for (k, v) in inputs.items()
            ]
        )

    else:
        inps = ""

    return (
        f'\n\t\t\t\t{instance_name} = InstanceInput {{\n\t\t\t\t\tSourceOp = "{source_op}",'
        f'\n\t\t\t\t\tSource = "{source_input}",{default}{inps}\n\t\t\t\t}},'
    )


def generate_instance_output(
    source_op: str, source_input: str = "Output", instance_name: str = "Output"
) -> str:
    return (
        f'\n\t\t\t\t{instance_name} = InstanceOutput {{\n\t\t\t\t\tSourceOp = "{source_op}",'
        f'\n\t\t\t\t\tSource = "{source_input}",\n\t\t\t\t}},'
    )


# Polylines
def generate_published_polyline(points: list[tuple[float, float]]) -> str:

    polyline_input = generate_inputs(Polyline=_polyline_value(points))
    point_data = "".join(
        generate_inputs(
            **{f"Point{i}": fusion_point(p[0], p[1]) for i, p in enumerate(points)}
        )
    )

    return polyline_input + point_data


def _polyline_value(points: list[tuple[float, float]]) -> str:
    header = "Polyline {\n\t\t\t\t\t\tPoints = {"
    point_ids = "".join([_point_id(i, "Point") for i, _ in enumerate(points)])
    footer = "\n\t\t\t\t\t\t\t},\n\t\t\t\t\t\t}"

    return header + point_ids + footer


def _point_id(index: int, name: str = "Point") -> str:
    return f'\n\t\t\t\t\t\t\t{{ PublishID = "{name}{index}" }},'
