from pysion import Composition, RGBA
from pysion.animation import Curve

comp = Composition()
xf = comp.add_tool("Transform", "SizeUp")
size = comp.animate(xf, "Size")
size.apply_curve(Curve.ease_in_and_out())

size.add_keyframes([(0, 1), (24, 0)])
size.add_keyframes([(12, 0.3)])

size[32] = 2

size.set_spline_color(RGBA(1, 0.5, 0))

xf["Center"] = (0.25, 0.25)

print(comp)
