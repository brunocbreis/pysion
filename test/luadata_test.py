import luadata

pydata = {"Input": dict(Value=4)}

lua = "{Tools = ordered() {}}"

print(luadata.unserialize(lua))

print(luadata.serialize({"Tools": pydata}))
