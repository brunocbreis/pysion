from pysion.new_generators import *


# # red = nt("Red", "Input", {"Value": 1})
# # pos = nt("ViewInfo", "OperatorInfo", {"Pos": [1, 1]})
# # src = nt("Size", "Input", {"SourceOp": "Transform1", "Source": "Size"})
# # empty = nt("Empty", "Emptiness")
# # points = ut("Points", dict(Point1=[0, 0.5], Point2=[0.1, 0.3]))

# # print(red, pos, src, empty, points, sep="\n")


# # # Polyline = Input(
# # #     Value = Polyline (
# # #         Points = [
# # #             dict(PublishID="Point0"),
# # #             dict(PublishID="Point1"),
# # #         ]
# # #     )
# # # )


# # print(ll([1, 2]))


# # red = Table(
# #     "Inputs",
# #     Table("Red", [Table("Value", 1), Table("Expression", "Blue + .5")], "Input"),
# # )

# # print(red)

# red = nt("Input", Value=1, Expression=None)
# blue = nt("Input", Value=0)
# point = nt("Input", Pos=(0, 1))


# bruno = nt("Background", Inputs=ut(Red=red, Blue=blue, Pos=point), force_indent=True)
# tool = ut(Background1=bruno, Background2=bruno)
# tools = ut(Tools=tool, ActiveTool="Background1")
# print(tools)

ut(PublishID="Point1")
poly = NamedTable(
    "Polyline",
    Points=[
        ut(PublishID="Point1"),
        ut(PublishID="Point2"),
        ut(PublishID="Point3"),
    ],
    force_indent=True,
)
print(ut(Polyline=nt("Input", Value=poly, force_indent=True), force_indent=True))
