import re

text = "{ Tools = { Background1 = Background { Inputs = { Red = Input { Value = 1 }}}}, ActiveTool =  'Background1' }"

# Regular expression to match named tables and their contents recursively
pattern = r"{\s*([a-zA-Z0-9_]+)\s*=\s*({[^{}]*(\{[^{}]*\}[^{}]*)*})\s*}"

# Function to recursively extract all named tables from the text
def extract_named_tables(text):
    matches = re.findall(pattern, text)
    tables = {}
    for match in matches:
        name, contents = match
        tables[name] = extract_named_tables(contents)
    return tables if tables else None


# Extract all named tables recursively from the text
result = extract_named_tables(text)

# Print the result
print(result)
