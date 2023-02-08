from .generators import (
    generate_tool,
    generate_inputs,
    generate_source_input,
    generate_published_polyline,
    generate_instance_input,
)
from dataclasses import dataclass


@dataclass
class Tool:
    id: str
    name: str
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self._inputs: dict[str, int | float | str] = {}
        self._source_inputs: dict[str, tuple[str, str]] = {}
        self._polyline: str = ""

    def __str__(self) -> str:
        source_inputs = ""
        if self.source_inputs:
            for k, v in self.source_inputs.items():
                source_inputs += generate_source_input(k, v[0], v[1])

        return generate_tool(
            self.id,
            self.name,
            generate_inputs(**self.inputs) + source_inputs + self.polyline,
            self.position,
        )

    @property
    def string(self) -> str:
        return self.__str__()

    @property
    def inputs(self):
        return self._inputs

    def add_inputs(self, **kwargs):
        for k, v in kwargs.items():
            self._inputs[k] = v

        return self

    @property
    def source_inputs(self):
        return self._source_inputs

    def add_source_input(self, input: str, tool_name: str, tool_output: str):
        self._source_inputs[input] = (tool_name, tool_output)

        return self

    def add_mask(self, mask_name: str):
        self.add_source_input("EffectMask", mask_name, "Mask")

        return self

    def add_published_polyline(
        self, points: list[tuple[float, float]], point_name: str = "Point"
    ):
        self._polyline += generate_published_polyline(points, point_name)

        return self

    @property
    def polyline(self) -> str:
        return self._polyline


@dataclass
class Macro:
    name: str
    tools: list[Tool]
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self.id: str = "MacroOperator"
        self._instanced_inputs: list[str] = []

    def add_instance_input(
        self,
        instance_name: str,
        source_op: str,
        source_input: str,
        default: str | int | float = "",
        **inputs
    ):
        self._instanced_inputs.append(
            generate_instance_input(
                instance_name, source_op, source_input, default, **inputs
            )
        )
