import json
import unittest

import IndigoGirls.dispatch as IndigoGirls


class SwipeTest(unittest.TestCase):
    def setUp(self):
        self.errorKey = "gameStatus"
        self.errorValue = "error:"
        self.initialize="initializeGame"
        self.swipe="swipe"
        self.row="rowCount"
        self.column="columnCount"
        self.board ="board"
        self.grid = "grid"
        self.score="score"
        self.gameStatusKey="gameStatus"
        self.gameStatusValue="underway"
        self.op="op"
        self.direction = "direction"
        self.board = "board"
        self.list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        self.left = "left"
        self.right = "RIGHT"
        self.down = "DoWn"
        self.up="uP"
        # self.right = "right"
        # self.down = "down"
        # self.up = "up"


    def tearDown(self):
        pass

    # -----------------------------------------------------------------------
    # ---- Acceptance Tests
    # 300 operation {'op': '"swipe"}''}
    #   Input-Output Analysis:
    #       direction:    name-value pairs
    #                     value: case-insensitive
    #                            up; down; left; right
    #                     Mandatory
    #
    #       board:        name-value pairs
    #                     Mandatory
    #                       name:  string where name=board
    #                       value: dictionary having the names "rowCount","columnCount", "grid"
    #                                   rowCount:    name-value pair
    #                                                name is "rowCount"
    #                                                value is positive integer where .GT. 1 and .LE. 100
    #                                                Mandatory
    #
    #                                   columnCount: name-value pair
    #                                                name is "columnCount"
    #                                                value is positive integer where .GT. 1 and .LE. 100
    #                                                Mandatory
    #
    #                                   grid:        name-value pair
    #                                                name is "grid"
    #                                                value is python list: represents the tiles on the playing grid
    #                                                                      in row-major order
    #                                                                      Consist rowCount x columnCount items
    #                                                                      List items are integer where .G.E. 0
    #                                                                      .?? No fewer than two items can be .GT. 0 ??.
    #                                                Mandatory
    #
    # Calculation Analysis:
    #  -swipe operation returns a dictionary that contains three-level pairs having the names: board, gameStatus & score
    #       board:        rowCount:    same as input rowCount
    #                     columnCount: same as input columnCount value
    #                     grid:        different from input grid list
    #                                  Calculation:  1. Tiles slides in the chosen direction until they are stopped by
    #                                                   another tile or the edge of the grid
    #                                                   1.1 If two tiles of the same number collide while moving,
    #                                                           then they will merge into a tile with the total value of
    #                                                           the two tiles that collided.
    #                                               2. Resulting tile cann ot merge with another tile again in same move
    #                                               3. Every turn, a new tile randomly appears in an empty spot on the
    #                                                  board with a value of either 2[with .75 prob] or 4[with .25 prob]
    #
    #                                   Mechanics:  value of "1" in grid-> tile = "2"
    #                                               value of "2" in grid-> tile = "4"
    #                                               cell1=2 and cell2=2 --> 1-tile=4 2-tile=4 => merge=4+4=8 --> cell=3
    #
    #      score:       name-value pair
    #                   name: "score"
    #                   value: integer
    #                          sum of (actual values of tiles)
    #
    #      gameStatus:  name-value pair
    #                   name: "gameStatus"
    #                   value: "underway"
    #
    # Sad path analysis:
    #      direction:   missing direction
    #                   invalid direction   direction='out'; direction='unknown'; direction:'2',
    #                   blank direction     direction ="  "
    #                   empty direction     direction = ""
    #
    #      rowCount:    non-integer         rowCount='two'; rowCount='2'
    #                   blank rowCount      rowCount="    "
    #                   empty rowCount      rowCount=""
    #                   out-of-bounds       rowCount=0; rowCount=101
    #                   missing rowCount
    #
    #      columnCount: non-integer         columnCount='nine'; columnCount='9',
    #                   empty columnCount   columnCount=''
    #                   blank columnCount   columnCount="  "
    #                   out-of-bounds       columnCount=0; columnCount=101
    #                   missing columnCount
    #
    #      grid:        missing grid
    #                   invalid grid       when columnCount=4 & rowCount=4, then grid=[1, 2]
    #                   invalid grid no tiles shifted e.g. 'grid': [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]
    #
    #      score:       missing in output
    #      gameStatus:  missing in output
    #                   invalid value
    #
    #   -- return {"gameStatus": "error:  diagnostic"}
    # -----------------------------------------------------------------------

    # Sad Path
    # --------------Sad Path Test for direction------------------------------------------------------------------------#
    def test_300_900_ShouldReturnErrorOnMissingDirection(self):
        msg = {self.op: self.swipe, self.board: {self.column: 4, self.row: 4,
                                                 self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_905_ShouldReturnErrorOnInvalidDirection(self):
        msg = {self.op: self.swipe, self.direction : "unknown", self.board: {self.column: 4, self.row: 4,
                                                 self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_910_ShouldReturnErrorOnInvalidDirection(self):
        msg = {self.op: self.swipe, self.direction : "out", self.board: {self.column: 4, self.row: 4,
                                                 self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_915_ShouldReturnErrorOnBlankDirection(self):
        msg = {self.op: self.swipe, self.direction : "    ", self.board: {self.column: 4, self.row: 4,
                                                 self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_920_ShouldReturnErrorOnEmptyDirection(self):
        msg = {self.op: self.swipe, self.direction : "", self.board: {self.column: 4, self.row: 4,
                                                 self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    # --------------Sad Path Test for board --------------------------------------------------------------------#
    def test_300_925_ShouldReturnErrorOnMissingBoard(self):
        msg = {self.op: self.swipe, self.direction : self.left}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_930_ShouldReturnErrorOnMissingRowCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4,
                                                        self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_935_ShouldReturnErrorOnMissingColumnCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.row: 4,
                                                        self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_940_ShouldReturnErrorOnNonIntegerRowCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: "four",
                                                                     self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_945_ShouldReturnErrorOnNonIntgerRowCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: "4",
                                                                     self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_950_ShouldReturnErrorOnNonIntegerColumnCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: "five", self.row: 4,
                                                                         self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_955_ShouldReturnErrorOnNonIntegerColumnCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: "4", self.row: 4,
                                                                         self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_960_ShouldReturnErrorOnRowCountInBoardLE1(self):
        msg = {self.op: self.swipe, self.direction: self.right, self.board: {self.column: 4, self.row: 1,
                                                                         self.grid: [1,0,2,0]}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_965_ShouldReturnErrorOnColumnCountInBoardLE1(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 1, self.row: 4,
                                                                         self.grid: [1,0,2,1]}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_970_ShouldReturnErrorOnRowCountInBoardGT100(self):
        grid = [0] * (120 * 2)
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 2, self.row: 120,
                                                                         self.grid: grid}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_975_ShouldReturnErrorOnColumnCountInBoardGT100(self):
        grid = [0] * (1200 * 4)
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 1200, self.row: 4,
                                                                         self.grid: grid}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_980_ShouldReturnErrorOnBlankRowCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: "  ",
                                                                         self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_990_ShouldReturnErrorOnBlankColumnCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column:"   ", self.row: 4,
                                                                         self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300_995_ShouldReturnErrorOnEmptyRowCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column:4, self.row: "",
                                                                         self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300__1000_ShouldReturnErrorOnEmptyColumnCountInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column:"", self.row: 4,
                                                                         self.grid: self.list}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    # --------------Sad Path Test for invalid grid --------------------------------------------------------------------#
    def test_300__1005_ShouldReturnErrorOnMissingGridInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: 4}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300__1010_ShouldReturnErrorOnInvalidGridInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: 4, self.grid: ""}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])


    def test_300__1015_ShouldReturnErrorOnInvalidGridInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: 4, self.grid: [1,2]}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300__1020_ShouldReturnErrorOnInvalidGridInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left,
               self.board: {self.column: 4, self.row: 1, self.grid: ["a",0,1,2]}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    def test_300__1025_ShouldReturnErrorOnInvalidGridInBoard(self):
        msg = {self.op: self.swipe, self.direction: self.left,
               self.board: {self.column: 1, self.row: 4, self.grid: [-1, 2,0,0]}}
        messageDictionary = json.dumps(msg)
        self.assertTrue(self.errorValue in json.loads(IndigoGirls.dispatch(messageDictionary))[self.errorKey])

    #--------------Sad Path Test for when no tiles shifted ------------------------------------------------------------#
    def test_300__1030_ShouldReturnErrorOnNoTilesShifted(self):
        msg = {self.op: self.swipe, self.direction: self.left,
               self.board: {self.column: 4, self.row: 4, self.grid: [2,1,0,0,
                                                                     2,0,0,0,
                                                                     1,0,0,0,
                                                                     0,0,0,0]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1035_ShouldReturnErrorOnNoTilesShifted(self):
        msg = {self.op: self.swipe, self.direction: self.right,
               self.board: {self.column: 4, self.row: 4, self.grid: [0, 0, 0, 1,
                                                                     0, 0, 1, 2,
                                                                     0, 0, 0, 2,
                                                                     0, 0, 2, 3]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1040_ShouldReturnErrorOnNoTilesShifted(self):
        msg = {self.op: self.swipe, self.direction: self.down,
               self.board: {self.column: 4, self.row: 4, self.grid: [0, 0, 0, 0,
                                                                     0, 0, 0, 0,
                                                                     0, 0, 0, 2,
                                                                     0, 1, 2, 3]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1045_ShouldReturnErrorOnNoTilesShiftedForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.up,
               self.board: {self.column: 2, self.row: 3, self.grid: [1, 1,
                                                                     0, 2,
                                                                     0, 0]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1050_ShouldReturnErrorOnNoTilesShiftedForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.up,
               self.board: {self.column: 2, self.row: 3, self.grid: [3,1,
                                                                     0,0,
                                                                     0,0]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1055_ShouldReturnErrorOnNoTilesShiftedForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.down,
               self.board: {self.column: 2, self.row: 3, self.grid: [0,0,
                                                                     3,1,
                                                                     1,2]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1065_ShouldReturnErrorOnNoTilesShiftedForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.left,
               self.board: {self.column: 2, self.row: 3, self.grid: [1,0,
                                                                     3,1,
                                                                     1,2]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300__1070_ShouldReturnErrorOnNoTilesShiftedForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.right,
               self.board: {self.column: 2, self.row: 3, self.grid: [0, 3,
                                                                     3, 1,
                                                                     1, 2]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusValue, outputDictionary[self.gameStatusKey])


    # Happy path tests
    def test_300_100_ShouldMoveTilesToLeft(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row: 4,
                                                                         self.grid: [4, 4, 0, 0,
                                                                                     2, 0, 0, 0,
                                                                                     1, 0, 0, 0,
                                                                                     0, 0, 0, 0]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        self.assertEquals(5, grid[0])

    def test_300_105_ShouldMoveTilesRight(self):
        msg = {self.op: self.swipe, self.direction: self.right, self.board: {self.column: 4, self.row: 4,
                                                                         self.grid: [3, 3, 3, 3,
                                                                                     1, 1, 0, 2,
                                                                                     0, 0, 0, 0,
                                                                                     0, 0, 1, 0]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[2], grid[3], grid[6], grid[7], grid[15]]
        self.assertListEqual(changedTiles, [4,4,2,2,1])

    def test_300_110_ShouldMoveTilesUp(self):
        msg = {self.op: self.swipe, self.direction: self.up, self.board: {self.column: 4, self.row: 4,
                                                                         self.grid: [2, 0, 0, 0,
                                                                                     0, 1, 0, 2,
                                                                                     1, 0, 0, 0,
                                                                                     0, 1, 0, 0]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[1], grid[3],grid[4]]
        self.assertListEqual(changedTiles, [2,2,1])

    def test_300_115_ShouldMoveTilesDown(self):
        msg = {self.op: self.swipe, self.direction: self.down, self.board: {self.column: 4, self.row: 4,
                                                                       self.grid: [1, 0, 0, 0,
                                                                                   0, 0, 0, 2,
                                                                                   0, 0, 2, 2,
                                                                                   0, 0, 1, 2]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[10], grid[11], grid[12], grid[14], grid[15]]
        self.assertListEqual(changedTiles, [2,2,1,1,3])

    def test_300_120_ShouldReturnSumOfMergedTiles(self):
        msg = {self.op: self.swipe, self.direction: self.right, self.board: {self.column: 4, self.row: 4,
                                                                         self.grid: [3, 3, 3, 3,
                                                                                     1, 1, 0, 2,
                                                                                     0, 0, 1, 0,
                                                                                     0, 0, 0, 0]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertEquals(36, outputDictionary[self.score])



    def test_300_125_ShouldAssignRandomValuesToOutput(self):
        msg = {self.op: self.swipe, self.direction: self.left, self.board: {self.column: 4, self.row:4,
                                                                         self.grid:[0, 0, 0, 0,
                                                                                    0, 0, 0, 0,
                                                                                    2, 0, 2, 0,
                                                                                    0, 0, 1, 0]}}
        messageDictionary = json.dumps(msg)
        numberOfOnes = 0
        numberOfTwos = 0

        numberOfOnes, numberOfTwos = self.getNumberOfOnesAndTwos(messageDictionary, numberOfOnes, numberOfTwos)

        probOne = float(numberOfOnes) / (float(numberOfTwos) + float(numberOfOnes))
        self.assertAlmostEquals(probOne, 0.75, delta=0.075)


    # Tests for 2x3, 1x4 and 4x1 matrices check for left, right, up and down

    def test_300_130_ShouldReturnGameStatusInOutput(self):
        msg = {self.op: self.swipe, self.direction: self.left,
               self.board: {self.column: 4, self.row: 4, self.grid: [0, 0, 0, 0,
                                                                     0, 0, 0, 0,
                                                                     2, 0, 2, 0,
                                                                     0, 0, 1, 0]}}
        outputDictionary = self.getOutputDictionay(msg)
        self.assertTrue(self.gameStatusKey in outputDictionary)
        self.assertEquals(self.gameStatusValue, outputDictionary[self.gameStatusKey])

    def test_300_135_ShouldMoveTilesLeftForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.left,
               self.board: {self.column: 2, self.row: 3, self.grid: [0,1,
                                                                     1,2,
                                                                     0,2]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[0],grid[2],grid[3], grid[4]]
        expected = [1,1,2,2]
        self.assertListEqual(changedTiles,expected)

    def test_300_140_ShouldMoveTilesRightForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.right,
               self.board: {self.column: 2, self.row: 3, self.grid: [1, 1,
                                                                     2, 2,
                                                                     0, 2]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[1], grid[3], grid[5]]
        self.assertListEqual(changedTiles, [2,3,2])

    def test_300_145_ShouldMoveTilesUpForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.up,
               self.board: {self.column: 2, self.row: 3, self.grid: [0, 1,
                                                                     0, 2,
                                                                     2, 2]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[0], grid[1],grid[3]]
        self.assertListEqual(changedTiles, [2,1,3])

    def test_300_150_ShouldMoveTilesDownForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.down,
               self.board: {self.column: 2, self.row: 3, self.grid: [0, 1,
                                                                     2, 2,
                                                                     0, 2]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        grid = boardDictionary[self.grid]
        changedTiles = [grid[3],grid[4],grid[5]]
        self.assertListEqual(changedTiles, [1,2,3])

    def test_300_155_ShouldReturnRowCountWhenMoveTilesDownForTwoColumn(self):
        msg = {self.op: self.swipe, self.direction: self.down,
               self.board: {self.column: 2, self.row: 3, self.grid: [0,1,
                                                                     1,1,
                                                                     1,0]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        self.assertEquals(3, boardDictionary[self.row])

    def test_300_160_ShouldReturnColumnCountWhenMoveTilesDownForNonSquareGrid(self):
        msg = {self.op: self.swipe, self.direction: self.down,
               self.board: {self.column: 2, self.row: 3, self.grid: [0, 1,
                                                                     2, 2,
                                                                     0, 2]}}
        outputDictionary = self.getOutputDictionay(msg)
        boardDictionary = outputDictionary[self.board]
        self.assertEquals(2, boardDictionary[self.column])

    def getNumberOfOnesAndTwos(self, messageDictionary, numberOfOnes, numberOfTwos):
        for i in range(64):
            outputDictionary = json.loads(IndigoGirls.dispatch(messageDictionary))
            grid = outputDictionary[self.board][self.grid]
            newList = grid
            del newList[8]
            del newList[11]
            numberOfOnes += newList.count(1)
            numberOfTwos += newList.count(2)
        return numberOfOnes, numberOfTwos

    def getOutputDictionay(self, msg):
        messageDictionary = json.dumps(msg)
        outputDictionary = json.loads(IndigoGirls.dispatch(messageDictionary))
        return outputDictionary
