from pysion import Tool, ToolID, Composition
from pathlib import Path

# Set up path for saving and retrieving expected results
FOLDER = Path("tests") / "expected_results" / "tool"


def compare_result(name: str, result: Composition) -> str:
    file_name = f"{name}.setting"

    with open(FOLDER / file_name, "r") as file:
        xp_result = file.read()

    assert repr(result) == xp_result


def test_add_mask():
    blur = Tool(ToolID.BLUR, "Blur")
    mask = Tool.mask("Mask", "BSpline", (-1, 0))
    blur.add_mask(mask)

    comp = Composition(blur, mask)

    compare_result("test_add_mask", comp)
