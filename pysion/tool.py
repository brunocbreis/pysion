from __future__ import annotations
from copy import copy
from dataclasses import dataclass
from .input import Input, Polyline
from .user_control import UserControl
from typing import Literal
from .flow import fusion_coords, offset_position
from .color import RGBA
from .named_table import NamedTable, UnnamedTable


@dataclass
class Tool:
    """Represents a Fusion Tool. Outputs a NamedTable, with the tool ID being the name.

    Arguments
    ----------
    - id : str
        An existing Fusion tool id. Examples: "Background", "TextPlus", "Blur"
        Import the ToolID SimpleNamespace for quick input of acceptable tool IDs
    - name : str
        A Fusion compatible name. Should not contain spaces or dashes or start with a number.
    - position : tuple[int,int]
        X, Y Coordinates for positioning the tool in the Flow.
    - inputs : UnnamedTable[str, Input] | None (deprecated)
        Optionally initialize a tool with a table of inputs. Prefer add_input() method.
    """

    id: str
    name: str
    position: tuple[int, int] | None = (0, 0)
    inputs: UnnamedTable[str, Input] | None = None
    output: str = "Output"
    user_controls: UnnamedTable[str, UserControl] | None = None
    source_op: str | None = None
    pass_through: Literal[True, None] = None

    def __post_init__(self):
        self._instances: list[Tool] | None = None

    # Renderers
    def render(self) -> NamedTable:
        inputs, user_controls = None, None

        if self.inputs:
            inputs = UnnamedTable()
            for name, inp in self.inputs.items():
                if isinstance(inp, NamedTable):
                    inputs[name] = inp

                if isinstance(inp, Input):
                    inputs[name] = inp.nt

        if self.user_controls:
            user_controls: UnnamedTable[str, UnnamedTable] = UnnamedTable(
                {name: control.render() for name, control in self.user_controls.items()}
            )

        return NamedTable(
            self.id,
            Inputs=inputs,
            ViewInfo=self.position_nt,
            UserControls=user_controls,
            SourceOp=self.source_op,
            PassThrough=self.pass_through,
            force_indent=True,
        )

    def __repr__(self) -> str:
        return repr(self.render())

    def __getitem__(self, key: str) -> Input:
        return self.inputs[key]

    def __setitem__(
        self, key: str, value: int | float | str | tuple[float, float]
    ) -> None:
        assert isinstance(key, str)

        if key in self.inputs:
            if self.inputs[key].spline:
                raise ValueError(
                    "Input has a Spline. Please assign values to specific keyframes with input[time] = value"
                )

        if isinstance(value, str):
            print(
                f"Warning: assigning {value} as text to {key}. To add an expression, use tool.add_expression_input()"
            )

        self.inputs[key] = Input(key, value)

    def _render_position(self) -> NamedTable | None:
        if self.position is None:
            return None
        return NamedTable("OperatorInfo", Pos=fusion_coords(self.position))

    @property
    def position_nt(self) -> NamedTable | None:
        return self._render_position()

    def _render_output(self) -> NamedTable:
        return NamedTable("InstanceOutput", SourceOp=self.name, Source=self.output)

    def _add_input(self, input: Input) -> None:
        if input is None:
            return

        if self.inputs is None:
            self.inputs = UnnamedTable(force_indent=True)

        self.inputs[input.name] = input

    def _add_user_control(self, user_control: UserControl) -> None:
        if self.user_controls is None:
            self.user_controls = UnnamedTable(force_indent=True)

        self.user_controls[user_control.name] = user_control

    # Inputs
    def add_input(self, input: Input) -> Tool:
        self._add_input(input)

        return self

    def add_inputs(self, *inputs: Input, **names_and_values) -> Tool:
        """Add Inputs as a batch. Takes Input() types as positional args, and/or
        key/value pairs as keyword args that map to Input(Key, value=Value)"""

        if inputs:
            for input in inputs:
                self._add_input(input)

        if names_and_values:
            for k, v in names_and_values.items():
                self._add_input(Input(k, v))

        return self

    def add_source_input(self, name: str, source_operator: str, source: str) -> Tool:
        self.add_input(Input(name, source_operator=source_operator, source=source))

        return self

    def add_expression_input(
        self, name: str, expression: str, value: int | float | str | None = None
    ) -> Tool:
        self.add_input(Input(name, value, expression))

        return self

    def add_published_polyline(self, points: list[tuple[float, float]]) -> Tool:
        poly = Polyline(points).inputs

        for input in poly:
            self.add_input(input)

        return self

    def add_published_polyline_with_expression(
        self,
        points: list[tuple[float, float]],
        expression_x: str,
        expression_y: str,
        replace_value: str = "POINT",
    ) -> Tool:
        """Create a Polyline with an expression for each point. The 'replace_value' argument will
        be replaced with each point value.

        Example: x = POINT+.2, y=.5
        will generate the following expression: Point([x_value]+.2, .5)"""

        poly = Polyline.with_expression(
            points, expression_x, expression_y, replace_value
        )

        for input in poly.inputs:
            self.add_input(input)

        return self

    def add_color_input(self, color: RGBA | None, prefix: str = "", suffix: str = ""):
        """Adds color input from RGBA. Different Prefixes and Suffixes are added to color inputs in Fusion.
        Backgrounds usually default to TopLeft[Color] for solid fills.
        Text+ nodes have [Color]1, [Color]2 etc for different layers.
        """
        if not color:
            return self

        self.add_inputs(
            **{
                f"{prefix}Red{suffix}": color.red,
                f"{prefix}Green{suffix}": color.green,
                f"{prefix}Blue{suffix}": color.blue,
                f"{prefix}Alpha{suffix}": color.alpha,
            }
        )

        return self

    def add_mask(self, mask: Tool) -> Tool:
        mask_input = Input.mask(mask.name, mask.output)
        self.add_input(mask_input)

        return self

    def add_user_control(
        self,
        pretty_name: str,
        input_control: str = "SliderControl",
        data_type: str = "Number",
        preview_control: str | None = None,
        is_integer: bool = False,
        page: str | None = None,
        default: int | float | str | None = None,
        min_scale: int | float | None = None,
        max_scale: int | float | None = None,
        min_allowed: int | float | None = None,
        max_allowed: int | float | None = None,
    ) -> Tool:
        new_user_control = UserControl(
            pretty_name,
            input_control,
            data_type,
            preview_control,
            is_integer,
            page,
            default,
            min_scale,
            max_scale,
            min_allowed,
            max_allowed,
        )
        self._add_user_control(new_user_control)

        return self

    # "Setters" and sorts
    def offset_position(self, offset: tuple[int, int]) -> None:
        self.position = offset_position(self.position, offset)

    # Alternate Constructors
    @classmethod
    def mask(
        cls,
        name: str,
        type: Literal["Rectangle", "Ellipse", "Polyline", "BSpline"] = "Rectangle",
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        """Creates a Mask tool and automatically sets the correct output name for a mask."""

        return Tool(id=f"{type}Mask", name=name, position=position, output="Mask")

    @classmethod
    def background(
        cls,
        name: str,
        top_left: RGBA | None = None,
        top_right: RGBA | None = None,
        bottom_left: RGBA | None = None,
        bottom_right: RGBA | None = None,
        resolution: tuple[int, int] | Literal["auto"] = "auto",
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        """Creates a Background tool and automatically sets color and resolution inputs."""

        bg = (
            Tool("Background", name, position)
            .add_color_input(top_left, "TopLeft")
            .add_color_input(top_right, "TopRight")
            .add_color_input(bottom_left, "BottomLeft")
            .add_color_input(bottom_right, "BottomRight")
        )

        if resolution == "auto":
            return bg.add_inputs(UseFrameFormatSettings=1)

        return bg.add_inputs(
            UseFrameFormatSettings=0, Width=resolution[0], Height=resolution[1]
        )

    @classmethod
    def merge(
        cls,
        name: str,
        background: Tool | None,
        foreground: Tool | None,
        position: tuple[int, int],
    ) -> Tool:
        mrg = Tool("Merge", name, position)

        if background is not None:
            try:
                background.output
                bg_out = background.output
            except AttributeError:
                bg_out = "Output"

            background = Input(
                "Background", source_operator=background.name, source=bg_out
            )
            mrg.add_input(background)

        if foreground is not None:
            try:
                foreground.output
                fg_out = foreground.output
            except AttributeError:
                fg_out = "Output"

            foreground = Input(
                "Foreground", source_operator=foreground.name, source=fg_out
            )
            mrg.add_input(foreground)

        return mrg

    @classmethod
    def text(
        cls,
        name: str,
        text: str,
        font_face: str = "Open Sans",
        font_style: str = "Bold",
        color: RGBA = RGBA(1, 1, 1),
        resolution: tuple[int, int] | Literal["auto"] = "auto",
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        if resolution == "auto":
            width, height = None, None
            use_ff = 1
        else:
            width, height = resolution
            use_ff = 0

        text_plus = Tool("TextPlus", name, position)
        text_plus.add_inputs(
            UseFrameFormatSettings=use_ff,
            Width=width,
            Height=height,
            Font=font_face,
            Style=font_style,
            StyledText=text,
        ).add_color_input(color, suffix="1")

        return text_plus

    @property
    def instances(self) -> list[Tool]:
        if self._instances is None:
            self._instances = []

        return self._instances

    def add_instance(
        self,
        custom_name: str | None = None,
        position: tuple[int, int] = (1, 0),
    ) -> Tool:

        i = len(self.instances) + 1
        name = f"{self.name}Instance{i}" if not custom_name else custom_name

        new_instance = Tool(self.id, name, position, source_op=self.name)

        self.instances.append(new_instance)

        return new_instance
