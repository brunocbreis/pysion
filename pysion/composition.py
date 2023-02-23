from __future__ import annotations
from pathlib import Path

from typing import Protocol, Literal
from .named_table import NamedTable, UnnamedTable
from .tool import Tool
from .modifiers import Modifier, XYPathModifier
from .macro import Macro
from .input import Input
from .animation import BezierSpline, Curve
from .values import FuID
from .color import RGBA

try:
    from pyperclip import copy

    PYPERCLIP_INSTALLED = True
except ImportError:
    PYPERCLIP_INSTALLED = False


class Operator(Protocol):
    @property
    def name(self) -> str:
        pass

    def render(self) -> NamedTable | UnnamedTable:
        pass


class Composition:
    """Represents a Fusion composition. Printing a comp (or better: using built in copy/save methods) will result in Fusion-compatible code.

    Optional Arguments
    ----------------
    - *tools : Tools or Macros
        Optionally initialize a comp with some previously created tools.
    """

    def __init__(self, *tools: Tool | Macro) -> None:
        self.tools: UnnamedTable[str, Tool | Macro] = None
        self._last_added_tool: Tool = None

        if tools:
            self.add_tools(*tools)

        self.active_tool_name: str | None = None
        self.modifiers: UnnamedTable[str, Operator] | None = None

    # Finishing methods
    def render(self) -> UnnamedTable:
        self._auto_set_active_tool()

        operators = self._render_operators()

        if not operators:
            print("Comp is empty.")
            return None

        return UnnamedTable(Tools=operators, ActiveTool=self.active_tool_name)

    def copy(self) -> None:
        """Copies Fusion-compatible code to the clipboard. Requires pyperclip [pip install pyperclip]."""

        if PYPERCLIP_INSTALLED:
            print("Successfully copied node tree to the clipboard.")
            return copy(repr(self))

        print(
            "For comp.copy() support, make sure to install optional dependency pyperclip.\n"
            "Printing comp instead.\n"
        )
        print(self)

    def save(
        self, file_name: str, folder: str | Path, file_extension: str = "setting"
    ) -> None:
        """Saves comp to a Fusion .setting text file."""

        if isinstance(folder, str):
            folder = Path(folder)

        file = folder / f"{file_name}.{file_extension}"

        if file.is_file():
            raise FileExistsError

        with open(file, "w") as f:
            f.write(repr(self))

        return None

    # Dunder methods
    def __repr__(self) -> str:
        return repr(self.render())

    def __getitem__(self, key: str) -> Operator:
        assert isinstance(key, str)

        if self.tools is None and self.modifiers is None:
            raise KeyError

        if self.modifiers is None:
            return self.tools[key]

        try:
            return self.modifiers[key]
        except KeyError:
            return self.tools[key]

    def __setitem__(self, key: str, value: Tool | Macro):
        assert isinstance(key, str)
        assert isinstance(value, Tool | Macro)

        self.add_tools(value)

    def __contains__(self, value: Tool | Macro | Modifier | BezierSpline) -> bool:
        if not (self.tools or self.modifiers):
            return False

        match value:
            case None:
                return False
            case Modifier() | BezierSpline():
                if not self.modifiers:
                    return False
                return value in self.modifiers.values()
            case Tool() | Macro():
                if not self.tools:
                    return False
                return value in self.tools.values()
            case _:
                raise ValueError

    # Private methods
    def _auto_set_active_tool(self) -> None:
        if not self.tools:
            self.active_tool_name = None
            return

        if not self.active_tool_name:
            self.active_tool_name = self._last_added_tool.name

    def _render_operators(self) -> UnnamedTable:
        operators = UnnamedTable(force_indent=True)

        if self.tools:
            operators.update(
                {tool_name: tool.render() for tool_name, tool in self.tools.items()}
            )
        if self.modifiers:
            operators.update(
                {mod_name: mod.render() for mod_name, mod in self.modifiers.items()}
            )

        return operators

    def _add_tool(self, tool: Tool | Macro) -> Operator:
        if self.tools is None:
            self.tools: UnnamedTable[str, Tool | Macro] = UnnamedTable()

        self.tools[tool.name] = tool
        self._last_added_tool = tool

        return tool

    def _auto_name_tool(self, tool_id: str) -> str:

        i = 1
        name = f"{tool_id}{i}"

        if not self.tools:
            return name

        names = self.tools.keys()
        while name in names:
            i += 1
            name = f"{tool_id}{i}"

        return name

    def _add_modifier(self, modifier: Operator) -> Operator:
        if self.modifiers is None:
            self.modifiers: UnnamedTable[str, Operator] = UnnamedTable()

        self.modifiers[modifier.name] = modifier

        return modifier

    # Public methods
    # Tools
    def add_tool(
        self,
        id: str,
        name: str | None = None,
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        """Creates a new Tool and adds it to the comp.

        Arguments
        ----------
        - id : str
            An existing Fusion tool id. Examples: "Background", "TextPlus", "Blur"
            Import the ToolID SimpleNamespace for quick input of acceptable tool IDs
        - name : str
            A Fusion compatible name. Should not contain spaces or dashes or start with a number.
            If not provided, an automatic sequential name will be given.
        - position : tuple[int,int]
            X, Y Coordinates for positioning the tool in the Flow.

        Returns
        ----
        The newly created Tool.

        """
        if not name:
            name = self._auto_name_tool(id)

        new_tool = Tool(id, name, position)

        return self._add_tool(new_tool)

    def add_tools(self, *tools: Operator) -> Composition:
        """Batch add tools, macros or any kind of operator to a comp.

        Arguments
        ----------
        - *tools: Operator (Tool, Macro or Modifier)

        Returns
        ----
        Self.

        """

        if not tools:
            return self

        for tool in tools:
            self._add_tool(tool)

        return self

    # Specific tools
    def add_merge(
        self,
        name: str | None = None,
        background: Tool | Macro | None = None,
        foreground: Tool | Macro | None = None,
        position: tuple[float, float] = (0, 0),
    ) -> Tool:
        """Creates a new Merge Tool and adds it to the comp. Can also automatically connect other tools to the merge's
        Background and Foreground inputs. If the tools are not yet in the comp, they will be added.

        Arguments
        ----------
        - name : str
            A Fusion compatible name. Should not contain spaces or dashes or start with a number.
            If not provided, an automatic sequential name will be given.
        - background : Tool, Macro or None
            The tool's output will be added to the merge's Background input.
        - foreground : Tool, Macro or None
            The tool's output will be added to the merge's Foreground input.
        - position : tuple[int,int]
            X, Y Coordinates for positioning the merge in the Flow.

        Returns
        ----
        The newly created Merge Tool.

        """

        merge = Tool("Merge", name, position)

        match background:
            case Tool():
                bg_output = background.output
            case Macro():
                bg_output = background.outputs[0].name
            case _:
                bg_output = None

        bg_input = (
            Input("Background", source_operator=background.name, source=bg_output)
            if bg_output
            else None
        )

        match foreground:
            case Tool():
                fg_output = foreground.output
            case Macro():
                fg_output = foreground.outputs[0].name
            case _:
                fg_output = None

        fg_input = (
            Input("Foreground", source_operator=foreground.name, source=fg_output)
            if fg_output
            else None
        )

        # Add tools to comp if not already
        if background not in self:
            if background is not None:
                self.add_tools(background)

        if foreground not in self:
            if foreground is not None:
                self.add_tools(foreground)

        if any([bg_input, fg_input]):
            merge.add_inputs(bg_input, fg_input)

        self.add_tools(merge)

        return merge

    def add_text(
        self,
        name: str = None,
        text: str = None,
        font_face: str = "Open Sans",
        font_style: str = "Bold",
        color: RGBA = RGBA(1, 1, 1),
        resolution: tuple[int, int] | Literal["auto"] = "auto",
        position: tuple[int, int] = (0, 0),
    ) -> Tool:
        """Creates a new Text+ Tool with sensible defaults and adds it to the comp.

        Arguments
        ----------
        - name : str
            A Fusion compatible name. Should not contain spaces or dashes or start with a number.
            If not provided, an automatic sequential name will be given.
        - text : str
            Text that will be added as the Value to StyledText input.
        - font_face : str
            Text that will be added as the Value to Font input.
        - font_style : str
            Text that will be added as the Value to Style input.
        - color : RGBA
            Adds values to Text+ main color inputs. Default white.
        - resolution : tuple[int,int]
            Adds value to Text+ UseFrameFormatSettings (if auto) and/or Width/Height.
        - position : tuple[int,int]
            X, Y Coordinates for positioning the merge in the Flow.

        Returns
        ----
        The newly created Text+ Tool.

        """

        text_plus = Tool.text(
            name, text, font_face, font_style, color, resolution, position
        )
        self.add_tools(text_plus)

        return text_plus

    # Modifiers
    def animate(
        self,
        tool: Tool | str,
        input_name: str,
        default_curve: Curve | None = None,
        keyframes: list[tuple[int | float, int | float]] | None = None,
    ) -> BezierSpline:
        """Creates a BezierSpline modifier to animate an input with keyframes. See animate_position for point inputs.

        Arguments
        -----
        - tool : Tool or str (for tool name)
            A Tool or a tool name if the tool already exists in the comp.
        - input_name : str
            Input to be animated. Will be created if doesn't exist yet. Will overwirte existing value if there was any.
        - default_curve : Curve | None
            Optionally add a default curve to be applied to all keyframes.
        - keyframes : list[tuple[int | float, int | float]] | None
            Optionally add keyframes as a list of tuples (frame, value) to animate immediately.

        Returns
        ----
        The newly created BezierSpline. Assign it to a new variable and add keyframes
        by assigning spline[frame] to a value or using the spline.add_keyframe method.

        """
        match tool:
            case Tool():
                if tool not in self:
                    print(f"Adding {tool.name} to the comp.\n")
                    self.add_tools(tool)

                tool_name = tool.name
            case str():
                try:
                    tool_name = tool
                    tool = self[tool]
                except KeyError:
                    raise ValueError(f"{tool} is not one of the tools in this comp.")
            case _:
                raise ValueError("Please add a valid Tool or Tool name.")

        new_spline = BezierSpline(f"{tool_name}{input_name}", default_curve)

        tool.add_source_input(input_name, new_spline.name, "Value")
        tool[input_name].spline = new_spline

        if keyframes:
            new_spline.add_keyframes(keyframes)

        return self._add_modifier(new_spline)

    def animate_position(
        self,
        tool: Tool | str,
        input_name: str = "Center",
        default_curve_x: Curve | None = None,
        default_curve_y: Curve | None = None,
        keyframes: list[tuple[int | float, tuple[float, float]]] | None = None,
        method: Literal["XYPath", "Path"] = "XYPath",
    ) -> XYPathModifier:
        """Creates a XYPathModifier to animate a positional input with keyframes.

        Arguments
        -----
        - tool : Tool or str (for tool name)
            A Tool or a tool name if the tool already exists in the comp.
        - input_name : str default="Center"
            Input to be animated. Will be created if doesn't exist yet. Will overwirte existing value if there was any.
            Should be an input of type Point in Fusion (like Center or Pivot).
        - default_curve_x : Curve | None
            Optionally add a default curve to be applied to all keyframes in X.
        - default_curve_y : Curve | None
            Optionally add a default curve to be applied to all keyframes in Y. Leave as None to apply the default X Curve to Y as well.
        - keyframes : list[tuple[int | float, int | float]] | None
            Optionally add keyframes as a list of tuples (frame, (x, y)) to animate immediately.

        Returns
        ----
        The newly created XYPathModifier. Assign it to a new variable and add keyframes by
        assigning xy_path[frame] to a tuple (x, y) or using the add_keyframe method on xy_path.x_spline or xy_path.y_spline.

        """
        match tool:
            case Tool():
                if tool not in self:
                    print(f"Adding {tool.name} to the comp.\n")
                    self.add_tools(tool)

                tool_name = tool.name
            case str():
                try:
                    tool_name = tool
                    tool = self[tool]
                except KeyError:
                    raise ValueError(f"{tool} is not one of the tools in this comp.")
            case _:
                raise ValueError("Please add a valid Tool or Tool name.")

        if method != "XYPath":
            raise NotImplementedError

        name = f"{tool_name}{input_name}XYPath"

        if default_curve_x and not default_curve_y:
            default_curve_y = default_curve_x

        x_spline = BezierSpline(f"{name}X", default_curve_x, RGBA(1))
        y_spline = BezierSpline(f"{name}Y", default_curve_y, RGBA(0, 1))

        xy_path = XYPathModifier(name, x_spline, y_spline)

        self.connect(xy_path, tool, "Value", input_name)

        for mod in [xy_path, x_spline, y_spline]:
            self._add_modifier(mod)

        if keyframes:
            keyframes_x = [(kf[0], kf[1][0]) for kf in keyframes]
            keyframes_y = [(kf[0], kf[1][1]) for kf in keyframes]

            x_spline.add_keyframes(keyframes_x)
            y_spline.add_keyframes(keyframes_y)

        return xy_path

    def publish(
        self,
        tool: Tool,
        input: str,
        value: int | float | tuple[int | float, int | float] | str | FuID,
    ) -> Modifier:

        id = "Publish"
        match value:
            case int() | float():
                id += "Number"
            case str():
                id += "Text"
            case tuple():
                id += "Point"
            case FuID():
                id += "FuID"
            case _:
                raise ValueError

        name = f"Publish{tool.name}{input}"

        new_published_value = Modifier(id, name)
        new_published_value.add_inputs(Value=value)

        tool.add_source_input(input, name, "Value")

        return self._add_modifier(new_published_value)

    def connect(
        self,
        tool_out: Tool,
        tool_in: Tool,
        source_out: str = "Output",
        source_in: str = "Input",
    ) -> Composition:
        tool_in.add_source_input(source_in, tool_out.name, source_out)

        return self

    def connect_to_published_value(
        self, published_value: Tool, tool_in: Tool, source_in: str
    ) -> Composition:
        return self.connect(published_value, tool_in, "Value", source_in)
