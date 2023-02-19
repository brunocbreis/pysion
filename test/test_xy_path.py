from pysion import Composition
from pysion.animation import Curve


comp = Composition()
xf = comp.add_tool("Transform", "Move")
x, y = comp.animate_position(xf, default_curve=Curve.ease_in_and_out())
x[0], x[24] = 0.5, 1.5
y[0], y[12] = 1, 0.5

comp.copy()
