from pysion.generators import (
    generate,
    ink_table,
    generate_input,
    generate_published_polyline,
)
from pysion.utils import fusion_coords

ply = generate_published_polyline([(0.1, 0.2), (0.3, 0.4)])
print(ply)
