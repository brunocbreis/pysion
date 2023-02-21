from pysion import Composition
from pathlib import Path


# Set up path for saving and retrieving expected results
FOLDER = Path("tests") / "expected_results" / "input"


def compare_result(name: str, result: Composition) -> str:
    file_name = f"{name}.setting"

    with open(FOLDER / file_name, "r") as file:
        xp_result = file.read()

    assert repr(result) == xp_result


# TESTS
def test_add_polyline():
    points = [(0, 0), (0.5, 0.5), (0.3, 0.75)]

    comp = Composition()
    poly_mask = comp.add_tool("PolylineMask")
    poly_mask.add_published_polyline(points)

    compare_result("test_add_polyline", comp)
