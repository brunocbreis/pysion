from __future__ import annotations
from .generators import generate_tool
from dataclasses import dataclass
from .input import Input, SourceInput, MaskInput, Polyline, Output
from .wrapper import wrap_for_macro
from typing import Literal
from .utils import RGBA
from typing import Literal


@dataclass
class Tool:
    id: str
    name: str
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self._inputs: dict[str, Input] = {}
        self._outputs: list[Output] = [Output(self.name)]
        self._source_inputs: list[SourceInput] = []
        self._polylines: list[Polyline] = []

    def __str__(self) -> str:
        inputs = "".join([input.string for input in self.inputs.values()])
        source_inputs = "".join([input.string for input in self.source_inputs])
        polylines = "".join([pl.string for pl in self.polylines])

        return generate_tool(
            self.id,
            self.name,
            inputs + source_inputs + polylines,
            self.position,
        )

    @property
    def string(self) -> str:
        return self.__str__()

    @property
    def inputs(self):
        return self._inputs

    def add_inputs(self, type: Literal["Value", "Expression"] = "Value", **kwargs):
        for k, v in kwargs.items():
            self._inputs[k] = Input(self.name, k, v, type)

        return self

    @property
    def source_inputs(self):
        return self._source_inputs

    def add_source_input(self, input: str, tool_name: str, tool_output: str = "Output"):
        self._source_inputs.append(
            SourceInput(self.name, input, tool_name, tool_output)
        )

        return self

    def add_mask(self, mask_name: str):
        self._source_inputs.append(MaskInput(self.name, mask_name))

        return self

    def add_published_polyline(
        self, points: list[tuple[float, float]], point_name: str = "Point"
    ):
        self._polylines.append(Polyline(points, point_name))

        return self

    @property
    def polylines(self) -> list[Polyline]:
        return self._polylines

    @classmethod
    def merge(
        cls, name: str, bg: Tool, fg: Tool, position: tuple[int, int] = (0, 0)
    ) -> Tool:
        return (
            Tool("Merge", name, position)
            .add_source_input("Background", bg.name)
            .add_source_input("Foreground", fg.name)
        )

    @classmethod
    def background(
        cls,
        name: str,
        color: RGBA = RGBA(),
        resolution: tuple[int, int] | Literal["auto"] = "auto",
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        bg = Tool("Background", name, position).add_inputs(
            TopLeftRed=color.red,
            TopLeftGreen=color.green,
            TopLeftBlue=color.blue,
            TopLeftAlpha=color.alpha,
        )

        if resolution == "auto":
            bg.add_inputs(UseFrameFormatSettings=1)
            return bg

        return bg.add_inputs(
            UseFrameFormatSettings=0, Width=resolution[0], Height=resolution[1]
        )

    # Method aliases
    bg = background
    mrg = merge


@dataclass
class Macro:
    name: str
    tools: list[Tool]
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self.id: str = "MacroOperator"
        self._instanced_inputs: list[Input] = []
        self._instanced_outputs: list[Output] = []

    @property
    def instanced_inputs(self):
        return self._instanced_inputs

    @property
    def instanced_outputs(self):
        return self._instanced_outputs

    @property
    def string(self):

        instanced_inputs = "".join([ip.instance for ip in self.instanced_inputs])

        instanced_outputs = "".join([op.instance for op in self.instanced_outputs])

        return wrap_for_macro(self, instanced_inputs, instanced_outputs, self.tools)

    def add_instance_input(
        self, input: Input, default: str | int | float = "", **properties
    ):
        new_instance = input
        new_instance.default = default
        new_instance.instance_properties = properties
        self._instanced_inputs.append(new_instance)

        return self

    def add_instance_output(self, output: Output):
        self._instanced_outputs.append(output)

        return self
