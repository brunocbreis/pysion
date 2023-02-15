from pysion.named_table import NamedTable, UnnamedTable
from pysion import fusion_coords

bg = NamedTable(
    "Background",
    Inputs=UnnamedTable(
        Width=NamedTable("Input", Value=1920),
        Height=NamedTable("Input", Value=1080),
        UseFrameFormatSettings=NamedTable("Input", Value=0),
        EffectMask=NamedTable("Input", SourceOp="Mask1", Source="Mask"),
    ),
    ViewInfo=NamedTable("OperatorInfo", Pos=fusion_coords((0, 2))),
)

mask = NamedTable(
    "RectangleMask",
    Inputs=NamedTable(
        "Inputs",
        MaskWidth=NamedTable("Input", Value=1920),
        MaskHeight=NamedTable("Input", Value=1080),
    ),
    ViewInfo=NamedTable("OperatorInfo", Pos=fusion_coords((0, 1))),
)

macro = NamedTable(
    "MacroOperator",
    Tools=UnnamedTable(Background1=bg, Mask1=mask),
    Outputs=UnnamedTable(
        Output=NamedTable("InstanceOutput", SourceOp="Background1", Source="Output")
    ),
    ViewInfo=NamedTable("GroupInfo", Pos=fusion_coords((0, 0))),
)

print(UnnamedTable(Tools=UnnamedTable(SuperMacro=macro), ActiveTool="Background1"))
