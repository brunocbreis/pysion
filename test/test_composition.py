from pysion import Composition, Tool, Macro

comp = Composition()

bg = comp.add_tool("Background", "BG1")


width = comp.animate("BG1", "Width")
width.add_keyframes([(0, 1920), (24, 1080)])


xf = Tool("Transform", "Transform1", (1, 0))

xf_size = comp.animate(xf, "Size")
xf_size[12] = 1
xf_size[24] = 2

comp.connect(bg, xf)

macro = Macro("MyMacro")
macro.add_tools(Tool("Blur", "MyBlur"))


comp["MyMacro"] = macro

print(comp)
