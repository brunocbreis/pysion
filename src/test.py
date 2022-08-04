import pysion
from pysion.generators import add_spline_input, wrap_for_fusion
import pysion.utils
import pysion.animation as anim


xf1 = pysion.add_tool(
    "Transform",
    "Transform1",
    inputs=pysion.add_inputs(Center=pysion.utils.fusion_point(0.25, 0.25))
    + add_spline_input("Transform1", "Size")
    + add_spline_input("Transform1", "Angle"),
)
sizeanim = anim.add_spline("Transform1", "Size", anim.EaseInOut(12, 24, 1, 3, 0.5))
angleanim = anim.add_spline("Transform1", "Angle", anim.EaseInOut(5, 18, 0, 360, 0.75))


print(wrap_for_fusion(xf1 + sizeanim + angleanim))
