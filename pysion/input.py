from dataclasses import dataclass
from .generators import (
    generate_inputs,
    generate_instance_input,
    generate_source_input,
    generate_published_polyline,
    generate_instance_output,
)
from typing import Literal
from .utils import fusion_string


@dataclass
class Input:
    parent: str
    name: str
    value: int | float | str
    type: Literal["Value", "Expression"] = "Value"

    def __post_init__(self):
        self._instance_properties: dict[str, int | float | str] = {}
        self.default: int | float | str = ""
        if self.type == "Expression":
            self.value = fusion_string(self.value)

    @property
    def instance_properties(self) -> dict[str, int | float | str]:
        return self._instance_properties

    @instance_properties.setter
    def instance_properties(self, values: dict[str, int | float | str]):
        for k, v in values.items():
            self._instance_properties[k] = v

    @property
    def string(self) -> str:
        return generate_inputs(self.type, **{self.name: self.value})

    @property
    def instance(self) -> str:
        return generate_instance_input(
            f"{self.name}Instance",
            self.parent,
            self.name,
            self.default,
            **self.instance_properties,
        )


@dataclass
class SourceInput:
    parent: str
    name: str
    source_operator: str
    source_output: str = "Output"

    @property
    def string(self) -> str:
        return generate_source_input(
            self.name, self.source_operator, self.source_output
        )


class MaskInput(SourceInput):
    def __init__(self, parent: str, source_operator: str):
        self.parent = parent
        self.source_operator = source_operator
        self.source_output: str = "Mask"
        self.name: str = "EffectMask"

    @property
    def string(self) -> str:
        return super().string


@dataclass
class Polyline:
    points: list[tuple[float, float]]
    point_name: str = "Point"

    @property
    def string(self) -> str:
        return generate_published_polyline(self.points)

    def add_points(self, *points: list[tuple[float, float]]):
        for p in points:
            self.points.append(p)


@dataclass
class Output:
    parent: str
    name: str = "Output"
    index: int = 0

    def __post_init__(self):
        if self.index:
            self.instance_name = f"{self.name}{self.index}"
        else:
            self.instance_name = self.name

    @property
    def instance(self) -> str:
        return generate_instance_output(self.parent, self.name, self.instance_name)
