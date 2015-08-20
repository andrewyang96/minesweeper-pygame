# TO DO: implement difficulties and text box
# TO DO: resize sprites using pygame.sprite
# TO DO: implement menu
# TO DO: sound effects

import pygame, sys, os
from pygame.locals import *  # @UnusedWildImport
import minesweeper

os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
# fonts
pygame.font.init()
smallFont = pygame.font.SysFont('arial', 14)
medFont = pygame.font.SysFont('arial', 24)
bigFont = pygame.font.SysFont('arial', 96, True)

# graphics
pygame.display.init()
pygame.display.set_caption('Minesweeper v0.1')
screen = pygame.display.set_mode((640,640),0,32)
coveredTile = pygame.image.load('sprites/spr_covered_tile.png').convert_alpha()
uncoveredTiles = {}
for num in xrange(9):
    uncoveredTiles[num] = pygame.image.load('sprites/spr_uncovered_tile_' + `num` + '.png').convert_alpha()
flaggedTile = pygame.image.load('sprites/spr_flagged_tile.png').convert_alpha()
minedTile = pygame.image.load('sprites/spr_mined_tile.png').convert_alpha()
selectedMinedTile = pygame.image.load('sprites/spr_selected_mined_tile.png').convert_alpha()
correctTile = pygame.image.load('sprites/spr_correct_tile.png').convert_alpha()

# constants and globals
X_OFFSET = 70
Y_OFFSET = 70
NUM_ROWS_IN_GRID = 10
NUM_COLS_IN_GRID = 10
NUM_MINES = 10
LINE_WIDTH = 3
RECT_SIZE = 50
BG_COLOR = (64,64,64)
notifications = {0:'', 1:'Unflag tile first.', 2:'Flag limit reached.', 3:'Press r to restart or e to exit.'}

# game-specific
def initializeGame():
    global mouseButtonStates, imageReprs, notification, b, gameOver, won, time, timeOffset
    mouseButtonStates = (False, False, False) # left, middle, right
    imageReprs = [[None for col in xrange(10)] for row in xrange(10)]  # @UnusedVariable
    notification = notifications[0]
    b = minesweeper.Board(NUM_ROWS_IN_GRID, NUM_COLS_IN_GRID, NUM_MINES)
    gameOver = False
    won = False
    timeOffset = 0
    pygame.init()

def exitGame():
    pygame.quit()
    sys.exit()

initializeGame()

while True:
    mouseButtonJustPressed = [False, False, False]
        
    for event in pygame.event.get():
        if event.type == QUIT:
            exitGame()
        if event.type == MOUSEBUTTONDOWN:
            mouseButtonStates = pygame.mouse.get_pressed()
            if mouseButtonStates[0]:
                mouseButtonJustPressed[0] = True
            if mouseButtonStates[1]:
                mouseButtonJustPressed[1] = True
            if mouseButtonStates[2]:
                mouseButtonJustPressed[2] = True
        if event.type == KEYDOWN and gameOver:
            if event.key == K_r:
                initializeGame()
                timeOffset = pygame.time.get_ticks()
            if event.key == K_e:
                exitGame()
        
    x,y = pygame.mouse.get_pos()
    # debugLabel = smallFont.render('mouse coords: ' + str(x) + ', ' + str(y), 1, (0,128,255))
    screen.fill(BG_COLOR)
    
    for row in xrange(NUM_ROWS_IN_GRID):
        for col in xrange(NUM_COLS_IN_GRID):
            tile = b.getTileAt(row, col)
            rect = Rect((X_OFFSET+RECT_SIZE*col,Y_OFFSET+RECT_SIZE*row), (RECT_SIZE,RECT_SIZE))
            if not gameOver:
                if rect.collidepoint(x,y) and not tile.isUncovered():
                    if mouseButtonJustPressed[0]: # left mouse: uncover
                        try:
                            gameOver = b.uncoverTileAt(row, col)
                        except minesweeper.UncoverError:
                            notification = notifications[1]
                        else:
                            notification = notifications[0]
                            if b.getNumCoveredTiles() == b.getNumMines(): # check if won
                                gameOver = True
                                won = True
                    elif mouseButtonJustPressed[2]: # right mouse: flag/unflag
                        try:
                            b.flagTileAt(row, col)
                        except minesweeper.FlagError:
                            notification = notifications[2]
                        else:
                            notification = notifications[0]
            if tile.isUncovered():
                if tile.isMined(): # selected mined tile
                    imageReprs[row][col] = selectedMinedTile
                else:
                    imageReprs[row][col] = uncoveredTiles[tile.getNumber()]
            elif tile.isFlagged():
                if gameOver and tile.isMined(): # guessed correctly
                    imageReprs[row][col] = correctTile
                else: # guessed incorrectly or game is not over
                    imageReprs[row][col] = flaggedTile
            else: # tile is unturned
                if gameOver and tile.isMined():
                    if won:
                        imageReprs[row][col] = coveredTile
                    else: # reveal mines when game over and lost
                        imageReprs[row][col] = minedTile
                else:
                    imageReprs[row][col] = coveredTile
            screen.blit(imageReprs[row][col], (rect.x,rect.y))

    if not gameOver:
        rawTime = pygame.time.get_ticks()
    timeLabel = medFont.render('Time: ' + `(rawTime - timeOffset)/1000.`, 1, (0,128,155))
    screen.blit(timeLabel, (10,10))
    
    if gameOver:
        if won:
            resultLabel = bigFont.render('YOU WIN!', 1, (0,128,255))
        else:
            resultLabel = bigFont.render('GAME OVER!', 1, (255,32,0))
        notification = notifications[3]
        screen.blit(resultLabel, (320-resultLabel.get_width()/2,320-resultLabel.get_height()/2))

    if notification != '':
        notificationLabel = medFont.render(notification, 1, (0,128,255))
        screen.blit(notificationLabel, (320-notificationLabel.get_width()/2,600-notificationLabel.get_height()/2))
    
    pygame.display.update()
