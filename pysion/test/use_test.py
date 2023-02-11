from pysion import Tool, Macro, Output, wrap_for_fusion, Input
from pysion.utils import fusion_point
from pyperclip import copy
from pysion.generators import generate_published_polyline

# bg = Tool("Background", "bg1")
# bg.add_inputs(UseFrameFormatSettings=1)

# xf = Tool("Transform", "xf1", (0, 1))
# xf.add_inputs(Size=1.5)
# xf.add_source_input("Input", bg.name)

# macro = Macro("Test", [bg, xf], (0, 0))
# macro.add_instance_input(Input(xf.name, "Size", 1.5), 1.5, Page="User")
# macro.add_instance_output(Output(xf.name))

# print(wrap_for_fusion([macro]))

points = [(0.1, 0.1), (0.2, 0.25), (0.3, 0.5), (0.4, 0.4), (0.5, 0.7)]

# print(generate_published_polyline(points))
# quit()

mask = (
    Tool("PolylineMask", "GeomLine")
    .add_inputs(BorderWidth=0.003)
    .add_published_polyline(points)
)
color = (
    Tool("Background", "GeomLineColor", (0, -1))
    .add_mask(mask.name)
    .add_inputs(
        TopLeftRed=0.5,
        TopLeftGreen=0.7,
        TopLeftBlue=0.8,
        TopLeftAlpha=1,
        UseFrameFormatSettings=1,
    )
)
geom_line = (
    Macro("LinePlot", [mask, color], (0, -1))
    .add_instance_output(Output(color.name))
    .add_instance_input(color.inputs["TopLeftRed"], ControlGroup=1, Name="Color")
    .add_instance_input(color.inputs["TopLeftGreen"], ControlGroup=1)
    .add_instance_input(color.inputs["TopLeftBlue"], ControlGroup=1)
    .add_instance_input(color.inputs["TopLeftAlpha"], ControlGroup=1)
    .add_instance_input(mask.inputs["BorderWidth"], Name="Thickness")
)

for i, p in enumerate(points):
    p = fusion_point(*p)

    if i > 0:
        geom_line.add_instance_input(Input(mask.name, f"Point{i}", p))
        continue

    geom_line.add_instance_input(Input(mask.name, f"Point{i}", p), Page="Data")

bg = Tool("Background", "Canvas", (-1, 0)).add_inputs(
    TopLeftRed=0.9,
    TopLeftGreen=0.9,
    TopLeftBlue=0.9,
    TopLeftAlpha=1,
    UseFrameFormatSettings=1,
)
mrg = (
    Tool("Merge", "PlotMrg", (0, 0))
    .add_source_input("Background", bg.name)
    .add_source_input("Foreground", geom_line.name)
)

copy(wrap_for_fusion([geom_line, bg, mrg]))


# problems: color control group. too repetitive to add instances...
