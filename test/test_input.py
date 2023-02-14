from pysion import Input, Polyline
from pysion.named_table import UnnamedTable

ip = Input("Red", source_operator="Background", source="Blue")

points = [(0.2, 0.3), (0.3, 0.4)]

pl = Polyline(points)

print(pl)
