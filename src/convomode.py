from gamemode import *

class ConvoMode(GameMode):
    #I really should mess around more with text displaying, methinks
    #make a general-purpose text-displaying function
    #use that to take care of word wrapping and whatnot
    def __init__(self):
        super(ConvoMode, self).__init__()
        #what else do conversations need?
        
    def input(self, event_list):
        pass
        #for this sort of function, maybe should be abstract for the convos themselves to do?
        #or have sections that call other things that are abstract
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill((0,0,0))
        #then draw stuff probs
        