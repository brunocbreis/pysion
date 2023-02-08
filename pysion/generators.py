from .utils import fusion_coords, fusion_point
from typing import Protocol


class Operator(Protocol):
    @property
    def id(self) -> str:
        pass

    @property
    def name(self) -> str:
        pass


def add_tool(
    tool_id: str, tool_name: str, inputs: str = "", position: tuple[int, int] = (0, 0)
) -> str:
    """Creates a Fusion tool"""
    x, y = fusion_coords(position)
    tool = (
        f"\t\t{tool_name} = {tool_id} {{\n\t\t\tInputs = {{\t\t\t\t{inputs}\n\t\t\t}},"
        f"\n\t\t\tViewInfo = OperatorInfo {{ Pos = {fusion_point(x,y)} }},\n\t\t}},\n"
    )
    return tool


def add_inputs(**inputs: dict[str, float | int | str]) -> str:
    """Creates strings for adding inputs to Fusion tools"""

    result = ""
    for key, value in inputs.items():
        result += f"\n\t\t\t\t{key} = Input {{ Value = {value}, }},"

    return result


def add_source_input(input: str, tool_name: str, tool_output: str = "Output") -> str:
    """
    Creates string for tools that get Inputs from other tools,
    e.g from a Mask or to a Merge
    """

    result = (
        f'\n\t\t\t\t{input} = Input {{\n\t\t\t\t\tSourceOp = "{tool_name}",'
        f'\n\t\t\t\t\tSource = "{tool_output}",\n\t\t\t\t}},'
    )
    return result


def add_mask(mask_name: str) -> str:
    return add_source_input("EffectMask", mask_name, "Mask")
