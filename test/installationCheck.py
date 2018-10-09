import IndigoGirls.dispatch as dispatch

errorJson = '{"op": "unknown"}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = ''
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = '{}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

validJson = '{"op": "initializeGame"}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

validJson = '{"op": "initializeGame", "rowCount":3}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

validJson = '{"op": "initializeGame", "rowCount":3, "columnCount":5}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

errorJson = '{"op": "initializeGame", "rowCount":"two"}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = '{"op": "initializeGame", "columnCount":"9"}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))

errorJson = '{"op": "initializeGame", "columnCount":1}'
errorResult = dispatch.dispatch(errorJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n\n").format(errorJson, errorResult))



