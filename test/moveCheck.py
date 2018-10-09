import IndigoGirls.dispatch as dispatch

validJson = '{"op":"predict", "moves":1 , "direction": "left", "board": {"columnCount": 4, "rowCount": 4}}'
validResult = dispatch.dispatch(validJson)
print(("Input string:\t{0}\nOutput string:\t{1}\n").format(validJson, validResult))

# def calculateScoreOfTileCombine(originGrid, swipedGrid):
#     score = 0
#     originGrid = sorted(originGrid, reverse = True)
#     print(originGrid)
#     swipedGrid = sorted(swipedGrid, reverse = True)
#     print(swipedGrid)
#     for i in range(len(swipedGrid)):
#         if originGrid[i] < swipedGrid[i]:
#             score += 2**swipedGrid[i]
#     return score
#
#
# originGrid = [0,0,0,1,0,0,0,1,2,2,0,0,1,0,2,2]
# swipedGrid = [3,2,2,2,1,0,0,2,0,0,0,0,0,0,0,0]
# score = calculateScoreOfTileCombine(originGrid, swipedGrid)
# print(score)
