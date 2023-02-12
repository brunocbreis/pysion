from pysion.generators import generate_inputs
from pysion.utils import fusion_string

print(generate_inputs("Expression", Size=fusion_string("Angle * 2")))
