import re


table = """"
{ 
        Tools = { 
                Background1 = Background { 
                        Inputs = { 
                                TopLeftRed = Input { Value = 1, }, 
                                TopLeftGreen = Input { Value = 0.4, }, 
                                TopLeftBlue = Input { Value = 0.1, }, 
                                TopLeftAlpha = Input { Value = 1, }, 
                                UseFrameFormatSettings = Input { Value = 1, }, 
                                EffectMask = Input { 
                                        SourceOp = "Rectangle", 
                                        Source = "Mask", 
                                }, 
                        }, 
                        ViewInfo = OperatorInfo { Pos = { 0, 0 }, }, 
                }, 
                Rectangle = RectangleMask { 
                        ViewInfo = OperatorInfo { Pos = { 0, -33 }, }, 
                }, 
        }, 
        ActiveTool = "Background1", 
}
"""

table = table.replace("\t", "").replace("\n", "")
table = re.sub("\\s{2,}", "", table)
table = re.sub(",(?!\\s)", ", ", table)


def find_tables(table: str, results: list[str] = None) -> list[str]:
    if results is None:
        results = []

    pattern = "(?<=\\{).*(?=\\})"
    result = re.findall(pattern, table)[0]

    if result:
        results += result
        find_tables(result, results)
    else:
        return results


pattern = "(?<=\\{).*(?=\\})"
result = re.findall(pattern, table)

print(result[0])

results = find_tables(table)

print(results)
