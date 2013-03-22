#main python file, runs game, handles arguments if we want, etc.
import sys
from game import *

g = Game()
while g.run():
    #stuff can be put here, in which case pass is not needed
    pass#maybe this should be continue, I don't remember
    
del g
sys.exit()