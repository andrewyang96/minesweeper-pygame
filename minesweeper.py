import random

class Board(object):
    """
    A minesweeper board containing Tiles.
    """
    
    def __init__(self, width, height, numMines):
        """
        Initialize the board of dimensions width X height and with numMines mines.
        """
        self.width = width
        self.height = height
        self.numTiles = width * height
        self.numMines = numMines
        self.numCoveredTiles = self.numTiles
        self.numFlaggedTiles = 0
        self.tiles = [[Tile(row, col) for col in range(width)] for row in range(height)]
        
        # populate board with numMines mines
        mines = random.sample(xrange(self.numTiles), self.numMines)
        for i in mines:
            self.tiles[i / self.width][i % self.width].setMine()
        
        # assign numbers
        for row in self.tiles:
            for mine in row:
                number = 0
                if mine.getRow() > 0: # check above
                    number += self.tiles[mine.getRow()-1][mine.getCol()].isMined()
                    if mine.getCol() > 0: # check upper-left
                        number += self.tiles[mine.getRow()-1][mine.getCol()-1].isMined()
                    if mine.getCol() < self.width-1: # check upper-right
                        number += self.tiles[mine.getRow()-1][mine.getCol()+1].isMined()
                if mine.getRow() < self.height-1: # check below
                    number += self.tiles[mine.getRow()+1][mine.getCol()].isMined()
                    if mine.getCol() > 0: # check lower-left
                        number += self.tiles[mine.getRow()+1][mine.getCol()-1].isMined()
                    if mine.getCol() < self.width-1: # check lower-right
                        number += self.tiles[mine.getRow()+1][mine.getCol()+1].isMined()
                if mine.getCol() > 0: # check left
                    number += self.tiles[mine.getRow()][mine.getCol()-1].isMined()
                if mine.getCol() < self.width-1: # check right
                    number += self.tiles[mine.getRow()][mine.getCol()+1].isMined()
                mine.setNumber(number)

    def uncoverTileAt(self, row, col):
        """
        Uncover a tile at row 'row' and col 'col'.
        Assume row and col are ints.
        Raise an IndexError if row is not within range(self.width) and col not within range(self.height)
        Otherwise raise an UncoverError if tile has already been uncovered.
        Return False if tile is flagged or turned.
        Return True if tile is mined, False if tile is not mined.
        """
        if not row in range(self.width) or not col in range(self.height):
            raise IndexError()
        tile = self.tiles[row][col]
        if tile.isFlagged(): # check if tile is currently flagged
            raise UncoverError('Tile is flagged. Unflag this tile first.')

        if not tile.isUncovered():
            # only decrement number of covered tiles if tile has not been uncovered yet
            self.numCoveredTiles -= 1
        res = tile.uncover()
        canUncoverNumbers = tile.getNumber()==0
        if tile.getNumber() == 0 and not tile.isMined(): # only check adjacent tiles if this tile's number is 0 and this tile isn't mined
            if row > 0: # check above
                above = self.tiles[row-1][col]
                if not above.isUncovered():
                    # print 'Checking above' # DEBUG
                    self.uncoverTile(above, canUncoverNumbers)
            if row < self.height-1: # check below
                below = self.tiles[row+1][col]
                if not below.isUncovered():
                    # print 'Checking below' # DEBUG
                    self.uncoverTile(below, canUncoverNumbers)
            if col > 0: # check left
                left = self.tiles[row][col-1]
                if not left.isUncovered():
                    # print 'Checking left'# DEBUG
                    self.uncoverTile(left, canUncoverNumbers)
            if col < self.width-1: # check right
                right = self.tiles[row][col+1]
                if not right.isUncovered():
                    # print 'Checking right' # DEBUG
                    self.uncoverTile(right, canUncoverNumbers)
        return res

    def uncoverTile(self, tile, canUncoverNumbers):
        """
        Uncover tile if tile's number is 0 or canUncoverNumbers is True.
        The tile cannot be mined if it's to be uncovered.
        Assume tile is a Tile.
        Used as a helper method to call uncoverTileAt recursively.
        """
        # print 'Number:', tile.getNumber() # DEBUG
        if (tile.getNumber() == 0 or canUncoverNumbers) and not tile.isMined() and not tile.isFlagged():
            # only call if tile's number is 0 or canUncoverNumbers is true, and tile isn't mined
            # print 'Uncover' # DEBUG
            self.uncoverTileAt(tile.getRow(), tile.getCol())

    def uncoverAllTiles(self):
        """
        DEPRECATED METHOD
        Uncover all mined tiles when game is over.
        """
        for row in self.tiles:
            for tile in row:
                if tile.isMined():
                    tile.uncover()
    
    def flagTileAt(self, row, col):
        """
        Flag/unflag tile at row 'row' and col 'col'.
        Assume row and col are ints, and checked is a list of Tiles.
        Raise an IndexError if row is not within range(self.width) and col not within range(self.height)
        Otherwise raise a FlagError if self.numFlaggedTiles will exceed self.numMines
        """
        if not row in range(self.width) or not col in range(self.height):
            raise IndexError()
        tile = self.tiles[row][col]
        if not tile.isFlagged() and self.numFlaggedTiles >= self.numMines:
            # if number of flagged tiles will exceed number of mines
            raise FlagError('Too many flags. Max number of flags is ' + str(self.numMines))
        
        tile.changeFlag()
        if tile.isFlagged(): # if tile is now flagged
            self.numFlaggedTiles += 1 # increment number of flagged tiles
        else: # if tile is now not flagged
            self.numFlaggedTiles -= 1 # decrement number of flagged tiles

    def getTileAt(self, row, col):
        """
        Return tile at row 'row' and col 'col'
        """
        return self.tiles[row][col]
    
    def getNumTiles(self):
        return self.numTiles

    def getNumMines(self):
        return self.numMines

    def getNumCoveredTiles(self):
        return self.numCoveredTiles

    def getNumFlaggedTiles(self):
        return self.numFlaggedTiles

    def getMined(self):
        """
        DEBUG METHOD
        Return board with mine states.
        """
        res = 'Mines\n'
        for row in self.tiles:
            for mine in row:
                if mine.isMined():
                    res += 'X'
                else:
                    res += str(mine.getNumber())
            res += '\n'
        return res

    def __str__(self, gameOver = False):
        res = ''
        if gameOver:
            res += 'GAME OVER\n'
        res += '-'*self.width + '\n'
        for row in self.tiles:
            for tile in row:
                res += tile.__str__(gameOver)
            res += '\n'
        return res


class Tile(object):
    """
    A Tile on the Board.
    """
    
    def __init__(self, row, col):
        """
        Initialize the tile at row row and column col.
        """
        self.row = row
        self.col = col
        self.turned = False # has tile been turned over
        self.mined = False # is mine on tile
        self.flagged = False # has tile been flagged
        self.number = None # number of neighboring mines

    def setMine(self):
        """
        Set mine on tile.
        """
        self.mined = True

    def setNumber(self, number):
        """
        Set number of surrounding mines.
        Assume number is an int.
        """
        self.number = number

    def uncover(self):
        """
        Uncover this tile.
        Return True if tile is mined, False if tile isn't mined.
        """
        self.turned = True
        return self.mined

    def changeFlag(self):
        """
        Flag this tile if self.flagged is False.
        Unflag this tile if self.flagged is True.
        """
        self.flagged = not self.flagged
    
    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def isUncovered(self):
        return self.turned
    
    def isMined(self):
        return self.mined

    def isFlagged(self):
        return self.flagged

    def getNumber(self):
        return self.number

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return False
        else:
            if (self.row == other.getRow() and self.col == other.getCol() and 
                self.number == other.getNumber() and self.mined == other.isMined()):
                return True
            else:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self, gameOver = False):
        if self.turned:
            if self.mined:
                return '!'
            else:
                return str(self.number)
        elif self.flagged:
            if gameOver:
                if self.mined: # guessed correctly
                    return 'X'
                else: # guessed incorrectly
                    return 'P'
            else:
                return 'P'
        else: # unturned
            if gameOver and self.mined: # reveal mines when game over
                return '!'
            else:
                return 'Q'
                # return unichr(0x25a0) # Unicode black square


class FlagError(Exception):
    """
    Raise this error when the number of flags exceeds the number of mines on the board.
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


class UncoverError(Exception):
    """
    Raise this error when player tries to uncover a flagged tile.
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


# DEBUG FUNCTIONS
def testBoard1():
    """
    Test a 10x10 board with 10 mines to see if board is being initialized correctly.
    """
    global b
    b = Board(10,10,10)
    print b.getMined()

def testBoard2():
    """
    Test a 10x10 board with 10 mines to see if tiles are being uncovered correctly.
    """
    testBoard1()
    gameOver = b.uncoverTileAt(0,0)
    print b
    
    if gameOver == b.getTileAt(0,0).isMined():
        print 'Game Over:', gameOver
        print 'Success!'
    else:
        print 'Failure.'
    
    if b.getNumCoveredTiles() <= b.getNumTiles()-1:
        print 'Successfully decremented number of covered tiles!', b.getNumCoveredTiles()
    else:
        print 'Failed to decrement number of covered tiles.'
    coveredTiles = b.getNumCoveredTiles()

    b.uncoverTileAt(0,0)
    if b.getNumCoveredTiles() == coveredTiles and b.getTileAt(0,0).isUncovered():
        print 'Success! Tile still remains uncovered.'
    else:
        print 'Failure. Uncovered tile is altered.', b.getNumCoveredTiles()

def testBoard3():
    """
    Test a 10x10 board with 10 mines to see if tiles are being flagged properly.
    """
    testBoard1()
    # flag tile at (0,0), (0,1), etc.
    b.flagTileAt(0,0)
    b.flagTileAt(0,1)
    b.flagTileAt(0,2)
    b.flagTileAt(0,3)
    b.flagTileAt(0,4)
    b.flagTileAt(0,5)
    b.flagTileAt(0,6)
    b.flagTileAt(0,7)
    b.flagTileAt(0,8)
    b.flagTileAt(0,9)
    if b.getNumFlaggedTiles() == 10:
        print 'Successfully flagged 10 tiles!'
    else:
        print 'Failed to flag 10 tiles.'
    
    b.flagTileAt(0,0) # unflag tile at (0,0)
    if not b.getTileAt(0,0).isFlagged():
        print 'Success! Tile is unflagged!'
    else:
        print 'Failure. Tile has not been unflagged.'
    if b.getNumFlaggedTiles() == 9:
        print 'Number of flagged tiles successfully decrements!'
    else:
        print 'Number of flagged tiles fails to decrement.'
    b.flagTileAt(0,0) # reflag tile at (0,0)
    
    try: # should raise FlagError
        b.flagTileAt(1,0)
    except FlagError:
        if not b.getTileAt(1,0).isFlagged():
            print 'FlagError successfully raised and tile is not flagged!'
        else:
            print 'FlagError raised, but tile is not supposed to flag.'
    else:
        print 'FlagError NOT raised.'

    try: # should raise UncoverError
        b.uncoverTileAt(0,0)
    except UncoverError:
        if not b.getTileAt(0,0).isUncovered():
            print 'UncoverError successfully raised and tile is still covered!'
        else:
            print 'UncoverError raised, but tile is not supposed to uncover.'
    else:
        print 'UncoverError NOT raised.'
    
    print b


# GAME LOOP
if __name__ == '__main__':
    b = Board(10,10,10) # change as necessary
    gameOver = False
    won = False
    while not gameOver:
        print b
        try:
            row = int(raw_input('Enter the row of the tile you wish to select. '))
            col = int(raw_input('Enter the column of the tile you wish to select. '))
            action = raw_input('Enter u to uncover and f to flag/unflag. ').lower()
        except ValueError:
            print 'Uh oh. You inputted something wrong.'
        else: # confirm row and col inputs are valid
            if action == 'u': # uncover tile
                try:
                    b.uncoverTileAt(row, col)
                except IndexError:
                    print 'The tile you specified is out of bounds.'
                except UncoverError:
                    print 'The tile you specified is flagged. Please unflag this tile first.'
                else:
                    if b.getTileAt(row, col).isMined(): # if selected tile is mined, game over
                        gameOver = True
                        won = False
                    elif b.getNumCoveredTiles() == b.getNumMines():
                        # if number of remaining tiles == number of mines, player wins
                        gameOver = True
                        won = True
            elif action == 'f': # flag tile
                try:
                    b.flagTileAt(row, col)
                except IndexError:
                    print 'The tile you specified is out of bounds.'
                except FlagError:
                    print 'You cannot flag more tiles. Please unflag a tile first.'
            else:
                print 'Action not understood.'
    print b.__str__(True)
    if won:
        print 'YOU WON!'
    else:
        print 'You lost.'
