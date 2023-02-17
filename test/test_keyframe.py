from pysion.animation import Keyframe
from pysion.named_table import UnnamedTable

kfs = [Keyframe(1, 0.5, (8, 0.3)), Keyframe(24, 0.75, left_hand=(18, 0.1))]

table = UnnamedTable()
table["KeyFrames"] = UnnamedTable()

for k in kfs:
    table["KeyFrames"][f"[{k.frame}]"] = k

print(table)
