from pysion.new_generators import *

# red = nt("Red", "Input", {"Value": 1})
# pos = nt("ViewInfo", "OperatorInfo", {"Pos": [1, 1]})
# src = nt("Size", "Input", {"SourceOp": "Transform1", "Source": "Size"})
# empty = nt("Empty", "Emptiness")
# points = ut("Points", dict(Point1=[0, 0.5], Point2=[0.1, 0.3]))

# print(red, pos, src, empty, points, sep="\n")


# # Polyline = Input(
# #     Value = Polyline (
# #         Points = [
# #             dict(PublishID="Point0"),
# #             dict(PublishID="Point1"),
# #         ]
# #     )
# # )


# print(ll([1, 2]))


# red = Table(
#     "Inputs",
#     Table("Red", [Table("Value", 1), Table("Expression", "Blue + .5")], "Input"),
# )

# print(red)

red = nd("Input", Value=1, Expression="Blue or 1")
blue = nd("Input", Value=0)
point = nd("Input", Pos=(0, 1))


bruno = nd("Background", Inputs=ud(Red=red, Blue=blue, Pos=point), force_indent=True)
tool = ud(Background1=bruno, Background2=bruno)
tools = ud(Tools=tool, ActiveTool="Background1")
print(tools)
