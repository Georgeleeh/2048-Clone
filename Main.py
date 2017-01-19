# TO DO
# Crashes sometimes?
# In Autoplay, input can't tell if what's entered is a number and could crash
# Add Saving
# Add Play Again?

# Import random
from random import *
from york_graphics import *
from math import *
import time
from logic_module import *


# ------------------------------------ Main ------------------------------------

# Might be overkill to put this in a function but it makes it easier
# to comment out and avoid the pauses when testing

Grid,LastGrid = InitGrid(Grid,LastGrid)

# New prettier way to print the grid
InitGraphics(Grid,Score)
#PrintGrid(Grid)

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

            Movement = waitForKeyPress()
            #Movement = input('Enter your move: ')
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
        DrawGrid(Grid,Score)
        #PrintGrid(Grid)
        if StillGoing == False:
            print()
            print('Sorry, you lose!')
            print('You Scored: ' + str(Score))
