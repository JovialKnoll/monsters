#If we want to take in arguments, we would use this file.
#This is where we create and run the game.
import sys
from game import *

g = Game()
while g.run():
    #stuff can be put here, in which case pass is not needed
    pass
    
del g
sys.exit()
