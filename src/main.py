#If we want to take in arguments, we would use this file.
#This is where we create and run the game.
import sys
from game import *

game = Game()
while game.run():
    #stuff can be put here, in which case pass is not needed
    pass

del game
sys.exit()
