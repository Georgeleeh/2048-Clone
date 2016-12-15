# NOTES
# spawnnumber, InitGrid work to complete spec.
# rotategrid could be better and flipgrid might be needed
# LEARN TO USE KEYBOARD INPUT

# Import random and tkinter
from random import *
from tkinter import *

# Initialise the variables
Grid = [[0,2,2,0],[4,0,2,0],[4,0,0,4],[0,8,4,2]]
Score = 0
NoMoves = False
GridChanged = False
Movement = " "

# Functions

def InitGrid(Grid):
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
    CollapseLine(Grid)
    Grid,Score = AddLine(Grid,Score)
    CollapseLine(Grid)
    return(Grid,Score)

def RotateGrid(Grid):
    # Rotate the whole grid 90deg clockwise
    NewGrid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for y in range(4):
        for x in range(4):
            NewGrid[y][x] = Grid[3 - x][y]
    Grid = NewGrid
    return(Grid)

def VFlipGrid(Grid):
    # Flip the grid along a vertical mirror line
    NewGrid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for y in range(4):
        for x in range(4):
            NewGrid[y][x] = Grid[y][3 - x]
    Grid = NewGrid
    return(Grid)

# Main

# must be written in this way to avoid score always being 0
Grid,Score = CondenseGrid(Grid,Score)
