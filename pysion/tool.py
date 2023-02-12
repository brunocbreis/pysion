from __future__ import annotations
from .generators import generate_tool
from dataclasses import dataclass
from .input import Input, SourceInput, MaskInput, Polyline, Output
from typing import Literal
from .utils import RGBA


@dataclass
class Tool:
    id: str
    name: str
    position: tuple[int, int] = (0, 0)
    outputs: list[Output] = None

    def __post_init__(self):
        if not self.outputs:
            self.outputs = [Output(self.name)]

        self._inputs: dict[str, Input] = {}
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

    def add_color_input(self, color: RGBA, prefix: str = "", suffix: str = ""):
        """Adds color input from RGBA. Different Prefixes and Suffixes are added to color inputs in Fusion.
        Backgrounds usually default to TopLeft[Color] for solid fills.
        Text+ nodes have [Color]1, [Color]2 etc for different layers.
        """

        self.add_inputs(
            **{
                f"{prefix}Red{suffix}": color.red,
                f"{prefix}Green{suffix}": color.green,
                f"{prefix}Blue{suffix}": color.blue,
                f"{prefix}Alpha{suffix}": color.alpha,
            }
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
        """Creates a Merge tool and automatically sets source inputs to connect other nodes."""

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
        """Creates a Background tool and automatically sets color and resolution inputs."""

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

    @classmethod
    def mask(
        cls,
        name: str,
        type: Literal["Rectangle", "Ellipse", "Polyline", "BSpline"] = "Rectangle",
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        """Creates a Mask tool and automatically sets the correct output name for a mask."""

        return Tool(f"{type}Mask", name, position, [Output(name, "Mask")])

    # Method aliases
    bg = background
    mrg = merge
