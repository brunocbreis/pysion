from pysion import Tool, Composition, Input, Macro
from pysion.utils import RGBA


comp = Composition()
tool = (
    Tool("sRectangle", "Rect")
    .add_color_input(RGBA(0.2, 0.3, 0.4))
    .add_inputs(Width=0.6)
    .add_input(Input("Height", 0.3, expression="Width / 2"))
)
render = (
    Tool("sRender", "Render", (1, 0))
    .add_source_input("Input", source_operator=tool.name, source=tool.output)
    .add_inputs(Width=1920, Height=1080)
)

macro = (
    Macro("Ball", tile_color=RGBA(0.5, 1, 1))
    .add_tools(tool, render)
    .add_input(tool, "Width", "Cool Width")
)

comp.add_tools(macro)

print(comp)
