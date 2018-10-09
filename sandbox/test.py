import copy


def calculateScore(originGrid, swipedGrid):
    score = 0
    originGrid = sorted(originGrid, reverse = True)
    swipedGrid = sorted(swipedGrid, reverse = True)
    for i in range(len(swipedGrid)):
        if originGrid[i] < swipedGrid[i]:
            score += 2**swipedGrid[i]
    return score

def swipeAction(direction, grid, columnCount):
    # execute swipe actions
    # initial the merged index
    mergeList = []
    if direction.lower() == "left":
        for i in range(len(grid)):
            j = i
            while j % columnCount != 0:
                if grid[j-1] == 0:
                    grid[j-1] = grid[j]
                    grid[j] = 0
                elif grid[j-1] == grid[j] and j not in mergeList:
                    grid[j-1] += 1
                    grid[j] = 0
                    mergeList.append(j-1)
                    mergeList.append(j)
                j -= 1

    elif direction.lower() == "right":
        for i in range(len(grid) - 1, -1, -1):
            j = i
            while j % columnCount != (columnCount - 1):
                if grid[j+1] == 0:
                    grid[j+1] = grid[j]
                    grid[j] = 0
                elif grid[j+1] == grid[j] and j not in mergeList:
                    grid[j+1] += 1
                    grid[j] = 0
                    mergeList.append(j)
                    mergeList.append(j+1)
                j += 1

    elif direction.lower() == "up":
        for i in range(len(grid)):
            j = i
            while j - columnCount >= 0:
                if grid[j-columnCount] == 0:
                    grid[j-columnCount] = grid[j]
                    grid[j] = 0
                elif grid[j-columnCount] == grid[j] and j not in mergeList:
                    grid[j-columnCount] += 1
                    grid[j] = 0
                    mergeList.append(j-columnCount)
                    mergeList.append(j)
                j -= columnCount

    elif direction.lower() == "down":
        for i in range(len(grid) - 1, -1, -1):
            j = i
            while j + columnCount < len(grid):
                if grid[j+columnCount] == 0:
                    grid[j+columnCount] = grid[j]
                    grid[j] = 0
                elif grid[j+columnCount] == grid[j] and j not in mergeList:
                    grid[j+columnCount] += 1
                    grid[j] = 0
                    mergeList.append(j)
                    mergeList.append(j+columnCount)
                j += columnCount
    return grid


move = 2
swipedGrid = [1,0,0,0,1,0,0,0,3,0,0,0,1,3,0,0]
columnCount = 4
predictGrid = copy.deepcopy(swipedGrid)
minScores = []
maxScores = []
while (move - 1) > 0:
    scoreBoard = []

    for i in range(len(predictGrid)):
        if predictGrid[i] == 0:
            testGrid = copy.deepcopy(predictGrid)
            for testGrid[i] in [1,2]:
                print(testGrid)
                newTestGrid =[[0 for x in range(16)] for y in range(4)]
                scoreList = [0,0,0,0]
                newTestGrid[0] = swipeAction('up', copy.deepcopy(testGrid), columnCount)
                scoreList[0] = calculateScore(testGrid, newTestGrid[0])
                newTestGrid[1] = swipeAction('down', copy.deepcopy(testGrid), columnCount)
                scoreList[1] = calculateScore(testGrid, newTestGrid[1])
                newTestGrid[2] = swipeAction('left', copy.deepcopy(testGrid), columnCount)
                scoreList[2] = calculateScore(testGrid, newTestGrid[2])
                newTestGrid[3] = swipeAction('right', copy.deepcopy(testGrid), columnCount)
                scoreList[3] = calculateScore(testGrid, newTestGrid[3])
                scoreBoard.append(scoreList)
                print(scoreBoard)
    scoreBoard = sum(scoreBoard,[])
    print(scoreBoard)
    minScores.append(min(scoreBoard))
    maxScores.append(max(scoreBoard))

    move -= 1

print(minScores)
print(maxScores)
