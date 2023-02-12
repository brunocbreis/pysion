from pysion.generators import generate, named_table

red = generate("Red", "Input", "Value", 1)
bg = generate("Background1", "Background", "Inputs", red, wrapper=True)


print(bg)

red1 = named_table("Red", "Input", "Value = 1", 1)
bg1 = named_table("Background1", "Background", red1, line_break=True)

print(bg1)
