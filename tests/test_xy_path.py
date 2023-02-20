from pysion import Composition
from pysion.animation import Curve


comp = Composition()
xf = comp.add_tool("Transform", "Move")
xy = comp.animate_position(
    xf, default_curve_x=Curve.decelerate_out(), default_curve_y=Curve.linear()
)

xy[0] = (0.5, 1)
xy[12] = (None, 0.5)
xy[24] = (0.25, None)

comp.save("XY_Path", "exports")
