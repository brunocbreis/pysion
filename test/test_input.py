from pysion import Input, Polyline, SourceInput
from pysion.new_generators import UnnamedDict

ip = Input("Red", 1)

points = [(0.2, 0.3), (0.3, 0.4)]

pl = Polyline(points)

print(pl.values())
