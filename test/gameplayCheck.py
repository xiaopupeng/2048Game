import IndigoGirls.dispatch as dispatch

validJson = '{"op":"swipe","direction": "left", "board": {"columnCount": 4, "rowCount": 4, "grid": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]}}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

validJson = '{"op":"swipe","direction": "left", "board": {"columnCount": 4, "rowCount": 4, "grid": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]}}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

validJson = '{"op":"swipe","direction": "right", "board": {"columnCount": 4, "rowCount": 4, "grid": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 0]}}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

validJson = '{"op":"swipe","direction": "up", "board": {"columnCount": 4, "rowCount": 4, "grid": [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2]}}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

validJson = '{"op":"swipe","direction": "right", "board": {"columnCount": 4, "rowCount": 4, "grid": [3, 3, 3, 3, 1, 1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0]}}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

errorJson = '{"op":"swipe","direction": "out", "board": {"columnCount": 4, "rowCount": 4, "grid": [3, 3, 3, 3, 1, 1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0]}}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = '{"op":"swipe", "board": {"columnCount": 4, "rowCount": 4, "grid": [3, 3, 3, 3, 1, 1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0]}}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = '{"op":"swipe","direction": "left", "board": {"columnCount": 4, "rowCount": 4, "grid": [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]}}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = '{"op":"swipe","direction": "right", "board": {"columnCount": 4, "rowCount": 4, "grid": [1,2]}}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))