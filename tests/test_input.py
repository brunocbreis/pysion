from pysion import Input, Polyline

ip = Input("Red", source_operator="Background", source="Blue")

points = [(0.2, 0.3), (0.3, 0.4)]

pl = Polyline(points)

ip[2] = 4
