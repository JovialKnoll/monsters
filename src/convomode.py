from gamemode import *
class ConvoMode(GameMode):
    class ConvoBoxes(object):
        top_left = pygame.Rect(8,88,88,36)
        top_right = pygame.Rect(224,88,88,36)
        bottom_left = pygame.Rect(8,132,88,36)
        bottom_right = pygame.Rect(224,132,88,36)
        elsewhere = pygame.Rect(0,0,320,180)
        
        @classmethod
        def boxIn(cls, pos):
            """Return a rectangle containing the position."""
            if top_left.collidepoint(pos):
                return cls.top_left
                #return top_left
            if top_right.collidepoint(pos):
                return cls.top_right
                #return top_right
            if bottom_left.collidepoint(pos):
                return cls.bottom_left
                #return bottom_left
            if bottom_right.collidepoint(pos):
                return cls.bottom_right
                #return bottom_right
            return elsewhere
            #return cls.elsewhere
            
        @classmethod
        def boxKey(cls, box, key):
            """Return a rectangle based on the current rectangle and the key pressed."""
            if key == pygame.K_LEFT or key == pygame.K_RIGHT:
                k = "lr"
            elif key == pygame.K_UP or key == pygame.K_DOWN:
                k = "ud"
            else:
                return box
            
            if (box == cls.top_right and k == "lr") or (box == cls.bottom_left and k == "ud"):
                return cls.top_left
            if (box == cls.top_left and k == "lr") or (box == cls.bottom_right and k == "ud"):
                return cls.top_right
            if (box == cls.bottom_right and k == "lr") or (box == cls.top_left and k == "ud"):
                return cls.bottom_left
            if (box == cls.bottom_left and k == "lr") or (box == cls.top_right and k == "ud"):
                return cls.bottom_right
            return cls.elsewhere
            
    def _setText(self):
        #should probably list out the things that need to be implemented here.
        #mainly, make the surfaces based on the text for view and buttons, fitting some criteria
        raise NotImplementedError("Implement: ConvoMode._setText.")
        
    def __init__(self):
        super(ConvoMode, self).__init__()
        self._setText()
        #hopefully I don't have to do anything funky to access the child classes versin of this function
        #here: make surface for copying parts of main text surface onto, for scrolling text... scroll bar / buttons? maybe continous scoll?
        self.background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout1boxes.png')).convert_alpha()
        #convert_alpha for now, allows for transparency
        self.box_selected = ConvoBoxes.elsewhere
        #what else do conversations need?
        
    def input(self, event_list):
        #for this sort of function, maybe should be abstract for the convos themselves to do?
        #or have sections that call other things that are abstract
        
        #switch around self.box_selected with mouse movements and arrow keys and stuff
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                self.box_selected = ConvoBoxes.boxIn(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.box_selected = ConvoBoxes.boxKey(self.box_selected, event.key)
                
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill((255,255,255))
        screen.blit(self.background, (0,0))
        #blit selection
        #blit text
        #highlight the selected box, if any
        #then draw stuff probs
        