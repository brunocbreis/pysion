from pysion import Composition

comp = Composition()

xf = comp.add_tool("Transform", "Transform1")
text = comp.add_tool("TextPlus", "MyName", (-1, 0))
text.add_inputs(StyledText="i am a text", UseFrameFormatSettings=1)

comp.connect(text, xf)
pub_aspect = comp.publish(xf, "Aspect", 1.5)
comp.publish(text, "StyledText", value="i am a text")
comp.connect_to_published_value(pub_aspect, text, "Size")

print(comp)
