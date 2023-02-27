from __future__ import annotations
from dataclasses import dataclass
from .named_table import NamedTable, UnnamedTable
from .animation import BezierSpline


@dataclass
class Input:
    """Represents a Fusion Input. Outputs a NamedTable."""

    name: str
    value: int | float | str | list[float] | NamedTable | None = None
    expression: str | None = None
    source_operator: str | None = None
    source: str | None = None
    spline: BezierSpline | None = None

    @property
    def nt(self) -> NamedTable:

        return NamedTable(
            "Input",
            Value=self.value,
            Expression=self.expression,
            SourceOp=self.source_operator,
            Source=self.source,
        )

    # def __repr__(self) -> str:
    #     return repr(self.nt)

    def __setitem__(self, key: int | float, value: int | float) -> None:
        assert (
            self.spline is not None
        ), "Please add a BezierSpline first with comp.animate()"

        self.spline.add_keyframes([(key, value)])

    def __getitem__(self, key: int | float) -> int | float:
        return self.spline.keyframes[key].value

    @classmethod
    def mask(cls, source_operator: str, source: str = "Mask") -> Input:
        return Input("EffectMask", source_operator=source_operator, source=source)


@dataclass
class Polyline:
    """Represents a Published Polyline input. Outputs a list of Inputs and Unnamed tables."""

    points: list[tuple[float, float]]

    def __post_init__(self) -> None:
        self._inputs: list[Input] | None = None
        self.expressions: list[str] | None = None

    def _render(self) -> None:

        polyline = Input("Polyline", value=NamedTable("Polyline", force_indent=True))
        points: list[Input] = []
        pub_ids: list[UnnamedTable] = []

        for i, (px, py) in enumerate(self.points):
            pname = f"Point{i}"

            if not self.expressions:
                points.append(Input(pname, value=(px, py)))
            else:
                points.append(Input(pname, expression=self.expressions[i]))

            pub_ids.append(UnnamedTable(PublishID=pname))

        polyline.value["Points"] = pub_ids

        if not self._inputs:
            self._inputs = []

        self._inputs.append(polyline)
        self._inputs += points

    @property
    def inputs(self) -> list[Input]:
        self._render()
        return self._inputs

    @classmethod
    def with_expression(
        cls, points: list[tuple[float, float]], x: str, y: str, replace: str = "POINT"
    ) -> Polyline:
        """Create a Polyline with an expression for each point. The 'replace' argument value will
        be replaced with each point value.

        Example: x = POINT+.2, y=.5
        will generate the following expression: Point([xvalue]+.2, .5)"""

        new_poly = Polyline(points)

        new_poly.expressions = [
            f"Point({x.replace(replace, p[0])}, {y.replace(replace, p[1])})"
            for p in points
        ]

        return new_poly
