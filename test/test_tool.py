from pysion import Tool
from pysion.utils import RGBA

tool = Tool("sRectangle", "Rect").add_color_input(RGBA(0.2, 0.3, 0.4))

print(tool)
