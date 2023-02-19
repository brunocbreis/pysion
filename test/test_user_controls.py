from pysion.user_controls import UserControl, UC
from pysion.named_table import UnnamedTable

ucs = [
    UserControl(
        "My Slider", data_type=UC.data_type.number, input_control=UC.input_control.screw
    )
]
table = UnnamedTable(
    UserControls={uc.name: uc.render() for uc in ucs},
    force_indent=True,
)
print(table)
