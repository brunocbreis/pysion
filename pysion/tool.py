from .generators import generate_tool
from dataclasses import dataclass
from .input import Input, SourceInput, MaskInput, Polyline


@dataclass
class Tool:
    id: str
    name: str
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self._inputs: list[Input]
        self._source_inputs: list[SourceInput]
        self._polylines: list[Polyline]

    def __str__(self) -> str:
        inputs = "".join([input.string for input in self.inputs])
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

    def add_inputs(self, **kwargs):
        for k, v in kwargs.items():
            self._inputs.append(Input(self.name, k, v))

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


@dataclass
class Macro:
    name: str
    tools: list[Tool]
    position: tuple[int, int] = (0, 0)

    def __post_init__(self):
        self.id: str = "MacroOperator"
        self._instanced_inputs: list[Input] = []

    @property
    def instanced_inputs(self):
        return self._instanced_inputs

    @property
    def string(self):
        instances = "".join([input.instance for input in self.instanced_inputs])
        pass

    def add_instance_input(
        self, input: Input, default: str | int | float = "", **properties
    ):
        new_instance = input
        new_instance.default = default
        new_instance.instance_properties = properties
        self._instanced_inputs.append(new_instance)
