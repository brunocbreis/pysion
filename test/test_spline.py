from pysion import Composition
from pysion.animation import Curve

comp = Composition()
xf = comp.add_tool("Transform", "SizeUp")
size_spline = comp.animate(xf, "Size")
size_spline.add_keyframes([(0, 1), (24, 0)], Curve.ease_in_and_out())
size_spline.add_keyframes([(12, 0.3)], Curve.ease_in_and_out())

print(comp)
