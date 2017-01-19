from random import *
from york_graphics import *
from math import *
import time

# Initialise the variables
LastGrid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
Grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#Grid = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

AutoMode = False
GridChanged = False
PlayerLost = False
PlayerWon = False
StillGoing = True
ValidMove = True

AutoCount = 0
AutoTime = 1
GridStill = 0
Score = 0

AutoInput = ''
GridLine = ''
Movement = ''

CanvasHeight = 600
CanvasWidth = 500
Pad = 10
GridHeight = (3 * CanvasHeight) / 4
GridWidth = CanvasWidth
SpaceHeight = (GridHeight - 5 * Pad) / 4
SpaceWidth = (GridWidth - 5 * Pad) / 4

# Define the colours

CanvasColour = '#FBF8F0'
GridColour = '#BAAD9F'

EmptySpaceColour = '#CDC1B3'
# get space colour from log2(gridnumber). hence, space 0 is empty
SpaceColour = ['','#EBE1D7','#ECE0CA','#F2B179','#F49465','#F47D60','#F65A31','#EFCE6D','#EDCA6C','#ECC84F','#EFC53F','#F2C603']

NewGameButtonColour = '#897763'

DarkTextColour = '#756B61'
LightTextColour = '#FEF0FB'


# ------------------------------------ Functions ------------------------------------


def AddLine(Grid,Score):
    """ Searches the grid from left to right and adds adjacent pairs,
    placing the result in the left hand column.
    
    @param Grid The 4*4 2D array
    @param Score The player's score
    """
    # Check every space in Grid left to right, except the leftmost column in a row
    for r in range(0,4):
        for c in range(1,4):
            # If a space has the same value as the space to it's left,
            # double the one to it's left and make it a 0
            if Grid[r][c] == Grid[r][c-1]:
                Grid[r][c-1] = Grid[r][c-1] * 2
                # resulting number is added to Score
                Score = Score + Grid[r][c-1]
                Grid[r][c] = 0
    return(Grid,Score)

def AutoPlay(Movement,GridStill,AutoCount,AutoTime):
    """ Allows the game to play itself, using the up and left method.
    
    @param Movement The direction in which the tiles will slide
    @param GridStill Holds how many turns the grid has remained unchanged
    @param Autocount Counts the number of turns for the autoplayer
    @param Autotime The interval between autoplayer turns
    """
    AutoCount += 1
    time.sleep(AutoTime)
    if GridStill >= 3:
        Movement = 'a'
    elif AutoCount % 2 == 0:
        Movement = 'd'
    else:
        Movement = 'w'
    return(Movement,AutoCount)

def CollapseLine(Grid):
    """ Moves every tile in the grid as far left as possible.
    
    @param Grid The 4*4 2D array
    """
    # Loop for worst case scenario length ([0,0,0,x] to [x,0,0,0])
    for i in range(3):
        # Check every space in Grid but the rightmost column in a row
        for r in range(0,4):
            for c in range(0,3):
                # if the space is 0, swap it with the value of the space to its right
                if Grid[r][c] == 0:
                    Grid[r][c] = Grid[r][c+1]
                    Grid[r][c+1] = 0
    return(Grid)

def CondenseGrid(Grid,Score):
    """ A combination of CollapseLine() and AddLine().
    
    @param Grid The 4*4 2D array
    @param Score The player's score
    """
    # Functions must be called as such to properly collapse and add each line
    # I figured I'd make this so I don't forget to use Collapse twice
    Grid = CollapseLine(Grid)
    Grid,Score = AddLine(Grid,Score)
    Grid = CollapseLine(Grid)
    return(Grid,Score)

def DrawGrid(Grid,Score):
    """ Draws a graphical representation of the grid in a 2048 style.
    
    @param Grid The 4*4 2D array
    @param Score The player's score
    """
    # Draw the Score Box

    moveTo(CanvasWidth-(SpaceWidth+2*Pad),Pad)
    setFillColour(EmptySpaceColour)
    setLineColour(EmptySpaceColour)
    drawRectangle(SpaceWidth+2*Pad,60)

    moveTo(CanvasWidth-(SpaceWidth+2*Pad) + (SpaceWidth+2*Pad)/2, 2*Pad)
    setLineColour(LightTextColour)
    setTextProperties(style='bold',size=20,anchor='n')
    drawText('SCORE')
    moveTo(CanvasWidth-(SpaceWidth+2*Pad) + (SpaceWidth+2*Pad)/2,4*Pad)
    drawText(Score)
    
    # Draw Grid Spaces

    setTextProperties(size=36,anchor='centre')

    # Loop whole grid
    for j in range(4):
        for i in range(4):
            moveTo((i+1) * Pad + i * SpaceWidth , CanvasHeight/4 + (j+1) * Pad + j * SpaceHeight)
            # Set the appropriate colour for the space
            if Grid[i][j] == 0:
                setFillColour(EmptySpaceColour)
                setLineColour(EmptySpaceColour)
            else:
                setFillColour(SpaceColour[ int(log2(Grid[i][j])) ])
                setLineColour(SpaceColour[ int(log2(Grid[i][j])) ])
            drawRectangle(SpaceWidth,SpaceHeight)
            # Move to the center of the space and enter the text
            moveTo((i+1)*Pad + i*SpaceWidth + SpaceWidth/2, CanvasHeight/4 + (j+1)*Pad + j*SpaceHeight + SpaceHeight/2)
            #setTextProperties()
            if Grid[i][j] < 8:
                setLineColour(DarkTextColour)
            else:
                setLineColour(LightTextColour)

            if Grid[i][j] != 0:
                drawText(str(Grid[i][j]))

    updateCanvas()

def GameWon(Grid, PlayerWon):
    """ Checks if the player has created a '2048' tile.
    
    @param Grid The 4*4 2D array
    @param PlayerWon Boolean to check if the player has won
    """
    # Check for a 2048 tile
    for x in range(4):
        for y in range(4):
            if Grid[x][y] == 2048:
                PlayerWon = True
                PrintGrid(Grid)
                print('Congratulations, you won!')
                print()
                
                return(PlayerWon)

def GridDifferent(Grid,LastGrid,GridChanged,GridStill):
    """ Checks to see if the grid has changed after a move.
    
    @param Grid The 4*4 2D array
    @param LastGrid The Grid after the previous turn
    @param GridChanged Boolean to check if the grid has changed after a move
    @param GridStill Holds how many turns the grid has remained unchanged
    """
    GridChanged = False
    GridStill += 1
    for y in range(4):
        for x in range(4):
            if Grid[y][x] != LastGrid[y][x]:
                GridChanged = True
                GridStill -= 1
    LastGrid = Grid
    return(GridChanged,LastGrid,GridStill)

def InitGraphics(Grid,Score):
    """ Draws a graphical representation of the grid in a 2048 style.
    
    @param Grid The 4*4 2D array
    @param Score The player's score
    """
    openWindow(width=CanvasWidth,height=CanvasHeight,title='2048')
    setCanvasColour(CanvasColour)

    # Draw the title and subtitles

    setLineColour(DarkTextColour)
    setTextProperties(size=36, style='bold', anchor='nw')
    moveTo(2*Pad,2*Pad)
    drawText('2048 - Python')

    setTextProperties(size=20)
    moveTo(Pad,80)
    drawText('Play 2048 Game with Python')

    setTextProperties(style='normal')
    moveTo(Pad,110)
    drawText('Join the numbers and get to the 2048 tile!')

    # Draw the Score Box

    moveTo(CanvasWidth-(SpaceWidth+2*Pad),Pad)
    setFillColour(EmptySpaceColour)
    setLineColour(EmptySpaceColour)
    drawRectangle(SpaceWidth+2*Pad,60)

    moveTo(CanvasWidth-(SpaceWidth+2*Pad) + (SpaceWidth+2*Pad)/2, 2*Pad)
    setLineColour(LightTextColour)
    setTextProperties(style='bold',size=20,anchor='n')
    drawText('SCORE')
    moveTo(CanvasWidth-(SpaceWidth+2*Pad) + (SpaceWidth+2*Pad)/2,4*Pad)
    drawText(Score)

    # Draw the grid background

    moveTo(0,CanvasHeight/4)
    setFillColour(GridColour)
    setLineColour(GridColour)
    drawRectangle(CanvasWidth,3*CanvasHeight/4)

    updateCanvas()

    # Draw Grid Spaces

    setTextProperties(size=36,anchor='centre')

    # Loop whole grid
    for j in range(4):
        for i in range(4):
            moveTo((i+1) * Pad + i * SpaceWidth , CanvasHeight/4 + (j+1) * Pad + j * SpaceHeight)
            # Set the appropriate colour for the space
            if Grid[i][j] == 0:
                setFillColour(EmptySpaceColour)
                setLineColour(EmptySpaceColour)
            else:
                setFillColour(SpaceColour[ int(log2(Grid[i][j])) ])
                setLineColour(SpaceColour[ int(log2(Grid[i][j])) ])
            drawRectangle(SpaceWidth,SpaceHeight)
            # Move to the center of the space and enter the text
            moveTo((i+1)*Pad + i*SpaceWidth + SpaceWidth/2, CanvasHeight/4 + (j+1)*Pad + j*SpaceHeight + SpaceHeight/2)
            #setTextProperties()
            if Grid[i][j] < 8:
                setLineColour(DarkTextColour)
            else:
                setLineColour(LightTextColour)

            if Grid[i][j] != 0:
                drawText(str(Grid[i][j]))

    updateCanvas()

def InitGrid(Grid,LastGrid):
    """ Initialises the grid to full specification.
    
    @param Grid The 4*4 2D array
    @param The Grid after the previous turn
    """
    for i in range(2):
        # Check is true when the random grid space is a 0
        check = False
        # Loop until an empty space is chosen
        while check == False:
            rn1 = randint(0,3)
            rn2 = randint(0,3)
            # If the space is empty, fill it
            if Grid[rn1][rn2] == 0:
                Grid[rn1][rn2] = 2
                check = True
    LastGrid = Grid
    return(Grid,LastGrid)

def MoveGrid(Grid,Movement,Score,ValidMove):
    """ Takes 'Movement' and slides the grid tiles appropriately 
    
    @param Grid The 4*4 2D array
    @param Movement The direction in which the tiles will slide
    @param Score The player's score
    @param ValidMove Boolean to hold whether the last move was valid
    """
    ValidMove = True
    if Movement.lower() == 'w':
        # Loop is pointless, but it seems to fix 'w' always giving 'False' for GridChanged
        for i in range(4):
            Grid = RotateGrid(Grid)
        Grid,Score = CondenseGrid(Grid,Score)
    elif Movement.lower() == 'a':
        for i in range(3):
            Grid = RotateGrid(Grid)
        Grid,Score = CondenseGrid(Grid,Score)
        Grid = RotateGrid(Grid)

    elif Movement.lower() == 's':
        Grid = RotateGrid(Grid)
        Grid = RotateGrid(Grid)
        Grid,Score = CondenseGrid(Grid,Score)
        Grid = RotateGrid(Grid)
        Grid = RotateGrid(Grid)
        
    elif Movement.lower() == 'd':
        Grid = RotateGrid(Grid)
        Grid,Score = CondenseGrid(Grid,Score)
        for i in range(3):
            Grid = RotateGrid(Grid)

    elif Movement.lower() == 'quit' or Movement.lower() == 'q':

        print('Goodbye!')

        sys.exit()

    else:
        print('Please choose a valid move (w,a,s,d or quit)')
        ValidMove = False
        
    return(Grid,Score,ValidMove)

def NoMoves(Grid, PlayerLost):
    """ Checks whether or not the player can make any legal moves. 
    
    @param Grid The 4*4 2D array
    @param PlayerLost Boolean to hold whether the player has lost
    """
    # Set PlayerLost to True as a default
    PlayerLost = True
    # Check for 0s
    for y in range(4):
        for x in range(4):
            if Grid[y][x] == 0:
                PlayerLost = False
                return(PlayerLost)
    # Check Rows for pairs of matching numbers
    for i in range(2):
        # Loop every row, all columns bar the far right
        for y in range(4):
            for x in range(3):
                # Check for adjacent match
                if Grid[y][x] == Grid[y][x+1]:
                    PlayerLost = False
                    StillGoing = True
        # Rotate The Grid to check for vertical pairs
        Grid = RotateGrid(Grid)
    # Rotate 3 more times to get back to normal
    for i in range(3):
        Grid = RotateGrid(Grid)
    return(PlayerLost)

def PrintGrid(Grid):
    """ Print the grid in an easily readable way in the console.
    
    @param Grid The 4*4 2D array
    """
    GridLine = ''
    PrintLine = ''
    GL2 = GridLine
    PL2 = ''
    for y in range(4):
        for x in range(4):
            # Checks how many characters the Grid entry contains 
            # and pads it with spaces to center it
            if len(str(Grid[x][y])) == 1:
                GridLine = GridLine + '  ' + str(Grid[x][y]) + '   ' + '|'
            elif len(str(Grid[x][y])) == 2:
                GridLine = GridLine + '  ' + str(Grid[x][y]) + '  ' + '|'
            elif len(str(Grid[x][y])) == 3:
                GridLine = GridLine + '  ' + str(Grid[x][y]) + ' ' + '|'
            elif len(str(Grid[x][y])) == 4:
                GridLine = GridLine + ' ' + str(Grid[x][y]) + ' ' + '|'

        # Important to save all the dashes into a string before printing.
        # Printing dashes directly is much slower.
        for i in range(len(GridLine)):
            
            PrintLine = PrintLine + '-'

        print(PrintLine)
        print(GridLine)
        GL2 = GridLine
        PL2 = PrintLine
        GridLine = ''
        PrintLine = ''
    print(PL2)
    print()
    print('Current Score: ' + str(Score))

def RotateGrid(Grid):
    """ Rotate the Grid 90 degrees clockwise. 
    
    @param Grid The 4*4 2D array
    """
    # Rotate the whole grid 90deg clockwise
    NewGrid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for y in range(4):
        for x in range(4):
            NewGrid[y][x] = Grid[3 - x][y]
    Grid = NewGrid
    return(Grid) 

def SpawnNumber(Grid):
    """ Spawn a '2' in a random unassigned space. 
    
    @param Grid The 4*4 2D array
    """
    # 'check' is true when the random grid space is a 0
    check = False
    # 'rand' determines whether a 2 or 4 appears
    rand = randint(0,2)
    # Loop until an empty space is chosen
    while check == False:
        rn1 = randint(0,3)
        rn2 = randint(0,3)
        # If the space is empty, fill it
        if Grid[rn1][rn2] == 0:
            # 2/3 chance to fill it with a 2
            if rand == 0 or rand == 1:
                Grid[rn1][rn2] = 2
                check = True
            else:
                Grid[rn1][rn2] = 4
                check = True
    return(Grid)     

def StartMenu(AutoMode,ValidMove,AutoTime):
    """ An initial menu asking how the player would like to play.
    
    @param AutoMode Boolean to hold if the player would like to start Automode
    @param ValidMove Boolean to hold whether the last move was valid
    @param Autotime The interval between autoplayer turns
    """
    ValidMove = False
    while ValidMove == False:

        print()
        AutoInput = input('Would you like me to play myself? (yes/no): ')
        print()
        
        if AutoInput.lower() == 'yes' or AutoInput.lower() == 'y':
            AutoMode = True
            ValidMove = True
        elif AutoInput.lower() == 'no' or AutoInput.lower() == 'n':
            AutoMode = False
            ValidMove = True
        else:
            print("Please enter either 'yes' or 'no'")
            print()

    if AutoMode == True:
        
        ValidMove = False
        while ValidMove == False:

            AutoTime = input('Please enter a speed (in seconds) for the autoplayer: ')

            if 0 < float(AutoTime) < 5:
                print('Speed set to one turn every ' + AutoTime + ' second(s)')
                AutoTime = float(AutoTime)
                ValidMove = True
            else:
                print('Please choose a number between 0 and five seconds (non-inclusive)')
                ValidMove = False
    return(AutoMode,AutoTime)

def Welcome():
    """ A few lines to introduce the game. """
    print()
    print("Welcome to this clone of the game 2048!")
    print()
    time.sleep(2)
    print("The aim of the game is to slide tiles and combine")
    print("them to create tile with the value '2048'")
    print()
    time.sleep(3)
    print("Use the WASD keys to slide the tiles to each side")
    print("or turn on 'Autoplay' to watch the game play itself!")
    print('(maybe you can get some tips from it?)')
    print()
    time.sleep(4)
    print()
