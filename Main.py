# TO DO
# Crashes sometimes?
# In Autoplay, input can't tell if what's entered is a number and could crash
# Add Saving
# Add Play Again?

# Import random
from random import *
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


# ------------------------------------ Functions ------------------------------------


def AddLine(Grid,Score):
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
    # Functions must be called as such to properly collapse and add each line
    # I figured I'd make this so I don't forget to use Collapse twice
    Grid = CollapseLine(Grid)
    Grid,Score = AddLine(Grid,Score)
    Grid = CollapseLine(Grid)
    return(Grid,Score)

def GameWon(Grid, PlayerWon):
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
    GridChanged = False
    GridStill += 1
    for y in range(4):
        for x in range(4):
            if Grid[y][x] != LastGrid[y][x]:
                GridChanged = True
                GridStill -= 1
    LastGrid = Grid
    return(GridChanged,LastGrid,GridStill)

def InitGrid(Grid,LastGrid):
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
    # Rotate the whole grid 90deg clockwise
    NewGrid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for y in range(4):
        for x in range(4):
            NewGrid[y][x] = Grid[3 - x][y]
    Grid = NewGrid
    return(Grid) 

def SpawnNumber(Grid):
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
    print()
    print("Welcome to this clone of the game 2048!")
    print()
    time.sleep(3)
    print("The aim of the game is to slide tiles and combine")
    print("them to create tile with the value '2048'")
    print()
    time.sleep(4)
    print("Use the WASD keys to slide the tiles to each side")
    print("or turn on 'Autoplay' to watch the game play itself!")
    print('(maybe you can get some tips from it?)')
    print()
    time.sleep(6)
    print()


# ------------------------------------ Main ------------------------------------

# Might be overkill to put this in a function but it makes it easier
# to comment out and avoid the pauses when testing
Welcome()

Grid,LastGrid = InitGrid(Grid,LastGrid)

# New prettier way to print the grid
PrintGrid(Grid)

AutoMode,AutoTime = StartMenu(AutoMode,ValidMove,AutoTime)

while StillGoing == True:
    
    # For Autoplay
    ValidMove = False
    GridStill = 0
    
    ValidMove = False
    while ValidMove == False:
        # Main difference in Automode is that it provides a move instead 
        # of asking for one, as much original code as possible is re-used
        if AutoMode == False:
            
            Movement = input('Enter your move: ')
            print()
            # Little divider to differentiate turns more visually
            print('----------------')
            print()
            
            Grid,Score,ValidMove = MoveGrid(Grid,Movement,Score,ValidMove)
            GridChanged,LastGrid,GridStill = GridDifferent(Grid,LastGrid,GridChanged,GridStill)
            
            ValidMove = GridChanged
            
        else:

            Movement,AutoCount = AutoPlay(Grid,GridStill,AutoCount,AutoTime)
            print()

            Grid,Score,ValidMove = MoveGrid(Grid,Movement,Score,ValidMove)
            
            GridChanged,LastGrid,GridStill = GridDifferent(Grid,LastGrid,GridChanged,GridStill)
            
            ValidMove = GridChanged

    PlayerWon = GameWon(Grid,PlayerWon)

    StillGoing = not PlayerWon
    
    if StillGoing == True:
        SpawnNumber(Grid)
        PlayerLost = NoMoves(Grid,PlayerLost)
        StillGoing = not PlayerLost
        PrintGrid(Grid)
        if StillGoing == False:
            print()
            print('Sorry, you lose!')
            print('You Scored: ' + str(Score))

