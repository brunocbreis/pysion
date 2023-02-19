from .tool import Tool
from .named_table import NamedTable
from .animation import BezierSpline


class Modifier(Tool):
    def __init__(self, id: str, name: str) -> None:
        return super().__init__(id, name, position=None)


class XYPathModifier(Modifier):
    def __init__(
        self,
        name: str,
        x_spline: BezierSpline | None = None,
        y_spline: BezierSpline | None = None,
        /,
        show_key_points=False,
    ) -> None:
        id = "XYPath"

        self.show_key_points: bool = show_key_points

        self.x_spline = x_spline
        self.y_spline = y_spline

        super().__init__(id, name)

        if x_spline is not None:
            self.add_source_input("X", x_spline.name, "Value")
        if y_spline is not None:
            self.add_source_input("Y", y_spline.name, "Value")

    def render(self) -> NamedTable:
        nt = super().render()

        nt.update(ShowKeyPoints=self.show_key_points)

        return nt
