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
from .new_generators import NamedDict, UnnamedDict


@dataclass
class Input:
    name: str
    value: int | float | str | list[float] | NamedDict
    expression: str | None = None

    @property
    def nd(self) -> NamedDict:
        return NamedDict("Input", Value=self.value, Expression=self.expression)

    def __repr__(self) -> str:
        return repr(self.nd)


@dataclass
class SourceInput:
    name: str
    source_operator: str
    source: str = "Output"

    @property
    def nd(self) -> NamedDict:
        return NamedDict("Input", SourceOp=self.source_operator, Source=self.source)

    def __repr__(self) -> str:
        return repr(self.nd)


@dataclass
class MaskInput(SourceInput):
    source_operator: str

    def __post_init__(self):
        self.name = "EffectMask"
        self.source = "Mask"


@dataclass
class Polyline:
    points: list[tuple[float, float]]

    @property
    def nd(self) -> NamedDict:
        inps: UnnamedDict[str, Input] = UnnamedDict()
        inps["Polyline"] = Input("Polyline", NamedDict("Polyline", force_indent=True))

        points: list[Input] = []
        pub_ids: list[UnnamedDict] = []

        for i, (px, py) in enumerate(self.points):
            pname = f"Point{i}"

            points.append(Input(pname, value=(px, py)))
            pub_ids.append(UnnamedDict(PublishID=pname))

        inps["Polyline"].value["Points"] = pub_ids

        inps.update({p.name: p for p in points})

        return inps

    def __repr__(self) -> str:
        return repr(self.nd)

    def values(self) -> list[Input]:
        return [input for input in self.nd.values()]

# @dataclass
# class Input:
#     name: str
#     value: int | float | str
#     type: Literal["Value", "Expression"] = "Value"

#     def __post_init__(self):
#         self._instance_properties: dict[str, int | float | str] = {}
#         self.default: int | float | str = ""
#         if self.type == "Expression":
#             self.value = fusion_string(self.value)

#     @property
#     def instance_properties(self) -> dict[str, int | float | str]:
#         return self._instance_properties

#     @instance_properties.setter
#     def instance_properties(self, values: dict[str, int | float | str]):
#         for k, v in values.items():
#             self._instance_properties[k] = v

#     @property
#     def string(self) -> str:
#         return generate_inputs(self.type, **{self.name: self.value})

#     @property
#     def instance(self) -> str:
#         return generate_instance_input(
#             f"{self.name}Instance",
#             self.parent,
#             self.name,
#             self.default,
#             **self.instance_properties,
#         )


# @dataclass
# class SourceInput:
#     parent: str
#     name: str
#     source_operator: str
#     source_output: str = "Output"

#     @property
#     def string(self) -> str:
#         return generate_source_input(
#             self.name, self.source_operator, self.source_output
#         )


# class MaskInput(SourceInput):
#     def __init__(self, parent: str, source_operator: str):
#         self.parent = parent
#         self.source_operator = source_operator
#         self.source_output: str = "Mask"
#         self.name: str = "EffectMask"

#     @property
#     def string(self) -> str:
#         return super().string


# @dataclass
# class Polyline:
#     points: list[tuple[float, float]]
#     point_name: str = "Point"

#     @property
#     def string(self) -> str:
#         return generate_published_polyline(self.points)

#     def add_points(self, *points: list[tuple[float, float]]):
#         for p in points:
#             self.points.append(p)


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
