'''
Modified on Oct 18 2017
@author: Xiaopu Peng
'''
import json
import random
import copy
#from numpy import *

def dispatch(messageJson):
    """
        dispatch is the microservice dispatcher for IndigoGirls, a 2048-like game.  It routes
        requests for game state transformations to the appropriate functions
        :param
            messageJson: JSON string that describes the state of the game needed for the
                        requested transformation
            :return:    A JSON string that describes the state of the game after the requested transformation
                        has taken place.
    """
    def initializeGame(messageJson):
        # check rowCount
        if 'rowCount' not in messageJson:
            rowCount = 4
        else:
            if type(messageJson['rowCount']) is not int:
                resultDictionary = json.dumps(buildErrorString('rowCount is not an integer'))
                return resultDictionary
            if messageJson['rowCount'] <= 1 or messageJson['rowCount'] > 100:
                resultDictionary = json.dumps(buildErrorString('rowCount is out of bounds'))
                return resultDictionary
            rowCount = messageJson['rowCount']

        # check columnCount
        if 'columnCount' not in messageJson:
            columnCount = 4
        else:
            if type(messageJson['columnCount']) is not int:
                resultDictionary = json.dumps(buildErrorString('columnCount is not an integer'))
                return resultDictionary
            if messageJson['columnCount'] <= 1 or messageJson['columnCount'] > 100:
                resultDictionary = json.dumps(buildErrorString('columnCount is out of bounds'))
                return resultDictionary
            columnCount = messageJson['columnCount']

        #initialize grid
        grid = [0] * (rowCount * columnCount)

        # randomly pick 2 positions for the 2 tiles
        positionList = random.sample(range(len(grid)),2)

        # assign selected random two tiles with 1 or 2
        weightedChoicePool = [1, 1, 1, 2]
        grid[positionList[0]] = random.choice(weightedChoicePool)
        grid[positionList[1]] = random.choice(weightedChoicePool)

        #build result message
        resultMessage = {'score': 0, 'board':{'columnCount':columnCount, 'rowCount':rowCount,
                                                          'grid':grid}, 'gameStatus':'underway'}
        return resultMessage

    def assignValues(messageJson):
        grid = messageJson['board']['grid']
        rowCount = messageJson['board']['rowCount']
        columnCount = messageJson['board']['columnCount']
        return grid, rowCount, columnCount

    def checkBoard(messageJson):
        if("board" not in messageJson):
            resultDictionary = json.dumps(buildErrorString('board is missing'))
            return resultDictionary

        # check rowCount
        if "rowCount" not in messageJson['board']:
            resultDictionary = json.dumps(buildErrorString('rowCount is missing'))
            return resultDictionary
        else:
            if type(messageJson['board']['rowCount']) is not int:
                resultDictionary = json.dumps(buildErrorString('rowCount is not an integer'))
                return resultDictionary
            if messageJson['board']['rowCount'] <= 1 or messageJson['board']['rowCount'] > 100:
                resultDictionary = json.dumps(buildErrorString('rowCount is out of bounds'))
                return resultDictionary

        # check columnCount
        if"columnCount" not in messageJson['board']:
            resultDictionary = json.dumps(buildErrorString('columnCount is missing'))
            return resultDictionary
        else:
            if type(messageJson['board']['columnCount']) is not int:
                resultDictionary = json.dumps(buildErrorString('columnCount is not an integer'))
                return resultDictionary
            if messageJson['board']['columnCount'] <= 1 or messageJson['board']['columnCount'] > 100:
                resultDictionary = json.dumps(buildErrorString('columnCount is out of bounds'))
                return resultDictionary

        #check grid
        if("grid" not in messageJson):
            resultDictionary = json.dumps(buildErrorString('grid is missing'))
            return resultDictionary
        else:
            if len(messageJson['board']['grid']) != \
                            messageJson['board']['rowCount'] * messageJson['board']['columnCount']:
                resultDictionary = json.dumps(buildErrorString('invalid grid of board'))
                return resultDictionary
            for i in range(len(messageJson['board']['grid'])):
                if messageJson['board']['grid'][i] < 0 or messageJson['board']['grid'][i] > \
                        messageJson['board']['rowCount'] * messageJson['board']['columnCount']:
                    resultDictionary = json.dumps(buildErrorString('invalid grid value'))
                    return resultDictionary
            if messageJson['board']['grid'].count(0) > len(messageJson['board']['grid']) - 2:
                resultDictionary = json.dumps(buildErrorString('not enough non 0 tiles'))
                return resultDictionary

    def swipePlayGrid(messageJson):
        #checkBoard
        checkBoard(messageJson)

        # initialize everything
        grid,rowCount,columnCount = assignValues(messageJson)

        # deepcopy grid to compare after swipe
        originalGrid = copy.deepcopy(grid)

        # validate presence of 'direction'
        if "direction" not in messageJson:
            resultDictionary = json.dumps(buildErrorString('missing direction'))
            return resultDictionary

        direction = messageJson['direction']

        # validate swipe command
        if direction.lower() not in ['up', 'down', 'left', 'right']:
            resultDictionary = json.dumps(buildErrorString('invalid direction'))
            return resultDictionary

        # execute swipe action
        swipedGrid = swipeAction(direction, grid, columnCount)

        # check if swipe able
        if swipedGrid == originalGrid:
            resultDictionary = json.dumps(buildErrorString('no tiles can be shifted'))
            return resultDictionary

        # randomly pick a tile and assign a value of 1 or 2
        finalGrid = insertRandomTile(swipedGrid)

        # initialize returnMessage
        resultMessage = {'score':2**max(finalGrid), 'board':{'columnCount':columnCount, 'rowCount':rowCount,
                                                          'grid':finalGrid}, 'gameStatus':'underway'}
        return resultMessage

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

    def insertRandomTile(swipedGrid):
        # insert 1 or 2 to random tile with 0
        zeroTile = []
        for i in range(len(swipedGrid)):
            if swipedGrid[i] == 0:
                zeroTile.append(i)
        randomZeroTileIndex = random.choice(zeroTile)
        weightedChoicePool = [1, 1, 1, 2]
        swipedGrid[randomZeroTileIndex] = random.choice(weightedChoicePool)
        return swipedGrid

    def recommendMove(messageJson):
        #checkBoard
        checkBoard(messageJson)

        # initialize everything
        grid,rowCount,columnCount = assignValues(messageJson)

        # assign move value, default as 0 if missing
        if 'moves' not in messageJson:
            move = 0
        else:
            move = messageJson['moves']

        # error message
        if type(move) is not int or move < 0:
            resultDictionary = json.dumps(buildErrorString('invalid move value'))
            return resultDictionary
        if loseOrNot(grid,rowCount,columnCount) == 0:
            resultDictionary = json.dumps(buildErrorString('no tiles can be shifted in 1 move'))
            return resultDictionary

        # execute moves
        if move == 0:
            direction = random.choice(['up','down','left','right'])
            swipedGrid = swipeAction(direction, copy.deepcopy(grid), columnCount)
            finalGrid = insertRandomTile(swipedGrid)
            maxScore = calculateScore(grid, swipedGrid)
        else:
            lastStepGrid = [copy.deepcopy(grid)]
            scoreBoard = [[0,0,0,0]]
            while move > 0:
                # print("last step grid = ", lastStepGrid)
                nextStepGridList = [[0 for x in range(4)] for y in range(len(lastStepGrid))]
                # print("nest step grid list = ", nextStepGridList)
                scoreBoard = sum(scoreBoard, [])
                # print(scoreBoard)
                nextLevelScoreList = [[scoreBoard[y] for x in range(4)] for y in range(len(lastStepGrid))]
                # print(nextLevelScoreList)
                scoreBoard = []
                for i in range(len(lastStepGrid)):
                    for possibleDirection in ['up', 'down', 'left', 'right']:
                        if possibleDirection == 'up':
                            nextStepGridList[i][0] = swipeAction(possibleDirection, copy.deepcopy(lastStepGrid[i]), columnCount)
                            nextLevelScoreList[i][0] += calculateScore(lastStepGrid[i], nextStepGridList[i][0])
                        elif possibleDirection == 'down':
                            nextStepGridList[i][1] = swipeAction(possibleDirection, copy.deepcopy(lastStepGrid[i]), columnCount)
                            nextLevelScoreList[i][1] += calculateScore(lastStepGrid[i], nextStepGridList[i][1])
                        elif possibleDirection == 'left':
                            nextStepGridList[i][2] = swipeAction(possibleDirection, copy.deepcopy(lastStepGrid[i]), columnCount)
                            nextLevelScoreList[i][2] += calculateScore(lastStepGrid[i], nextStepGridList[i][2])
                        else:
                            nextStepGridList[i][3] = swipeAction(possibleDirection, copy.deepcopy(lastStepGrid[i]), columnCount)
                            nextLevelScoreList[i][3] += calculateScore(lastStepGrid[i], nextStepGridList[i][3])
                    scoreBoard.append(nextLevelScoreList[i])
                # print("next level scores = ", nextLevelScoreList)
                # print("score board = ", scoreBoard)
                lastStepGrid = []
                for i in range(len(nextStepGridList)):
                    for j in range(4):
                        lastStepGrid.append(copy.deepcopy(nextStepGridList[i][j]))
                # print("last step grid for the next round =", lastStepGrid)
                move -= 1

            # find first move index
            maxScore = 0
            firstMoveIndex = 0
            for i in range(len(scoreBoard)):
                for j in range(4):
                    if maxScore < scoreBoard[i][j]:
                        maxScore = scoreBoard[i][j]
                        firstMoveIndex = i
            # print("next move direction = ",firstMoveIndex)
            # print("max score = ", maxScore)

            # find the first step from
            while firstMoveIndex >= 4:
                firstMoveIndex = firstMoveIndex // 4
            if firstMoveIndex == 0:
                firstDirection = 'up'
            elif firstMoveIndex == 1:
                firstDirection = 'down'
            elif firstMoveIndex == 2:
                firstDirection = 'left'
            elif firstMoveIndex == 3:
                firstDirection = 'right'
            else:
                firstDirection = random.choice(['up','down','left','right'])
            # print(firstDirection)

            # execute first step
            swipedGrid = swipeAction(firstDirection, grid, columnCount)
            finalGrid = insertRandomTile(swipedGrid)

        # initialize returnMessage
        resultMessage = {'score': maxScore, 'board':{'columnCount':columnCount, 'rowCount':rowCount,
                                                          'grid':finalGrid}, 'gameStatus':'underway'}
        return resultMessage

    def calculateScore(originGrid, swipedGrid):
        score = 0
        originGrid = sorted(originGrid, reverse = True)
        swipedGrid = sorted(swipedGrid, reverse = True)
        for i in range(len(swipedGrid)):
            if originGrid[i] < swipedGrid[i]:
                score += 2**swipedGrid[i]
        return score

    def updateStatus(messageJson):
        #checkBoard
        checkBoard(messageJson)

        # initialize everything
        grid,rowCount,columnCount = assignValues(messageJson)

        # assign tile value, default as 2048 if missing
        if 'tile' not in messageJson:
            tile = 2**round(rowCount * columnCount * 0.6875)
        else:
            tile = messageJson['tile']

        # error message
        if type(tile) is not int:
            resultDictionary = json.dumps(buildErrorString('invalid tile value'))
            return resultDictionary
        else:
            if tile < 2 or tile > 2**(rowCount * columnCount):
                resultDictionary = json.dumps(buildErrorString('invalid tile value'))
                return resultDictionary
        # win or lose
        if 2**max(grid) >= tile:
            messageJson['gameStatus'] = 'win'
        elif 2**max(grid) < tile and loseOrNot(grid, rowCount, columnCount) == 0:
            messageJson['gameStatus'] = 'lose'
        else:
            messageJson['gameStatus'] = 'underway'
        return messageJson['gameStatus']

    def loseOrNot(grid, rowCount, columnCount):
        if 0 in grid:
            return 1
        else:
            for i in range(rowCount * columnCount):
                if i % columnCount != (columnCount - 1):
                    if grid[i] == grid[i+1]:
                        return 1
                if i < (rowCount - 1) * columnCount:
                    if grid[i] == grid[i + columnCount]:
                        return 1
        return 0

    def predict(messageJson):
        # validate 'direction'
        if "direction" not in messageJson:
            resultDictionary = json.dumps(buildErrorString('missing direction'))
            return resultDictionary
        direction = messageJson['direction']
        if direction.lower() not in ['up', 'down', 'left', 'right']:
            resultDictionary = json.dumps(buildErrorString('invalid direction'))
            return resultDictionary

        # validate 'moves'
        if 'moves' not in messageJson:
            move = 1
        else:
            move = messageJson['moves']
        if type(move) is not int or move < 0:
            resultDictionary = json.dumps(buildErrorString('invalid move value'))
            return resultDictionary
        if move > 4000:
            resultDictionary = json.dumps(buildErrorString('memory exhausted'))
            return resultDictionary
        #validate 'board'
        checkBoard(messageJson)
        # initialize everything
        grid,rowCount,columnCount = assignValues(messageJson)

        #check if no tile can be shifted on next swipe
        if loseOrNot(grid,rowCount,columnCount) == 0:
            resultDictionary = json.dumps(buildErrorString('no tiles can be shifted in 1 move'))
            return resultDictionary


        swipedGrid = swipeAction(direction, copy.deepcopy(grid), columnCount)
        highScore = calculateScore(grid, swipedGrid)
        lowScore = highScore
        averageScore = highScore
        if move == 1:
            pass
        else:
            predictGrid = [copy.deepcopy(swipedGrid)]
            while move - 1 > 0:
                minScores = []
                maxScores = []
                averageScores = []
                curPredictGrid = [[0 for x in range(4)] for y in range(len(predictGrid))]
                #print(curPredictGrid)
                curScoreBoard = [[] for y in range(len(predictGrid))]
                #print(curScoreBoard)
                noSwipeCount = 0
                for j in range(len(predictGrid)):
                    for i in range(len(predictGrid[j])):
                        if predictGrid[j][i]==0:
                            testGrid = copy.deepcopy(predictGrid[j])
                            for testGrid[i] in [1,2]:
                                scoreList = [0,0,0,0]
                                curPredictGrid[j][0] = swipeAction('up', copy.deepcopy(testGrid), columnCount)
                                if curPredictGrid[j][0] == testGrid:
                                    noSwipeCount += 1
                                else:
                                    scoreList[0] = calculateScore(testGrid, curPredictGrid[j][0])
                                curPredictGrid[j][1] = swipeAction('down', copy.deepcopy(testGrid), columnCount)
                                if curPredictGrid[j][1] == testGrid:
                                    noSwipeCount += 1
                                else:
                                    scoreList[1] = calculateScore(testGrid, curPredictGrid[j][1])
                                curPredictGrid[j][2] = swipeAction('left', copy.deepcopy(testGrid), columnCount)
                                if curPredictGrid[j][2] == testGrid:
                                    noSwipeCount += 1
                                else:
                                    scoreList[2] = calculateScore(testGrid, curPredictGrid[j][2])
                                curPredictGrid[j][3] = swipeAction('right', copy.deepcopy(testGrid), columnCount)
                                if curPredictGrid[j][3] == testGrid:
                                    noSwipeCount += 1
                                else:
                                    scoreList[3] = calculateScore(testGrid, curPredictGrid[j][3])
                                curScoreBoard[j].append(scoreList)
                        #print(len(curScoreBoard[j]))
                    #print(curScoreBoard)
                    minmaxScoreboard = copy.deepcopy(curScoreBoard[j])
                    minmaxScoreboard = sum(minmaxScoreboard, [])
                    minScores.append(min(minmaxScoreboard))
                    maxScores.append(max(minmaxScoreboard))
                    #print(len(curScoreBoard[j]))
                    for i in range(len(curScoreBoard[j])):
                        if i % 2 == 0:
                            curScoreBoard[j][i] = [ curScoreBoard[j][i][y] * 3 for y in range(4)]
                    #print(curScoreBoard[j])
                    curScoreBoard[j] = sum(curScoreBoard[j], [])
                    #print(curScoreBoard[j])
                    scoreBoardSum = 0
                    for i in range(len(curScoreBoard[j])):
                        scoreBoardSum += curScoreBoard[j][i] / 4
                    #print(scoreBoardSum)
                    averageScores.append(round(scoreBoardSum / (len(curScoreBoard[j]) - noSwipeCount)))

                curPredictGrid = []
                for i in range(len(curPredictGrid)):
                    for j in range(4):
                        curPredictGrid.append(copy.deepcopy((curPredictGrid[i][j])))
                highScore += max(maxScores)
                lowScore += min(minScores)
                averageSum = 0
                for i in range(len(averageScores)):
                    averageSum += averageScores[i]
                averageScore += averageSum / len(averageScores)
                move -= 1

        resultMessage = {'highScore': highScore, 'lowScore':lowScore, 'averageScore':averageScore, 'GameStatus': 'underway'}
        return resultMessage


    def buildErrorString(diagnostic):
        """
            returns a dictionary containing the specified key and accompanying diagnostic information
            :param
                diagnostic:      A string that describes the error
            :return:    A dictionary that contains the specified error key having a value that
                        consists of the specfied error string followed by a free-form diagnostic message
        """
        ERROR_PROPERTY = 'gameStatus '
        ERROR_PREFIX = 'error: '
        return ERROR_PROPERTY + ERROR_PREFIX + diagnostic

    # Validate JSONness of input be converting the string to an equivalent dictionary
    try:
        messageJson = json.loads(messageJson)
    except:
        resultDictionary = json.dumps(buildErrorString('input JSON string is invalid'))
        return resultDictionary

    if("op" not in messageJson):
        resultDictionary = json.dumps(buildErrorString('op is missing'))
        return resultDictionary

    # Perform the game transformation as directed by the value of the "op" key
    #  input to each function:  a dictionary containing the name-value pairs of the input JSON string
    #  output of each function:  a dictionary containing name-value pairs to be encoded as a JSON string
    if(messageJson["op"] == "initializeGame"):
        resultDictionary = initializeGame(messageJson)
    elif(messageJson["op"] == "swipe"):
        resultDictionary = swipePlayGrid(messageJson)
    elif(messageJson["op"] == "status"):
        resultDictionary = updateStatus(messageJson)
    elif(messageJson['op'] == 'recommend'):
        resultDictionary = recommendMove(messageJson)
    elif(messageJson["op"] == "predict"):
        resultDictionary = predict(messageJson)
    else:
        resultDictionary = buildErrorString('op is invalid')

    # Covert the dictionary back to a string in JSON format
    resultJson = json.dumps(resultDictionary)
    return resultJson
