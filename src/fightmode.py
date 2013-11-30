import os, pygame
from gamemode import *
from boxes import *
from constants import *
class FightMode(GameMode):
    class FightBoxes(Boxes):
        rects = {
            'top'   : pygame.Rect(24,  24,  88,  36),
            'middle': pygame.Rect(24,  76,  88,  36),
            'bottom': pygame.Rect(24, 128,  88,  36),
        }
        
        @classmethod
        def boxKey(cls, box, key):
            """Return a rectangle based on the current rectangle and the key pressed."""
            if (box is cls.rects['middle'] and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.rects['bottom'] and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.rects['top']
            if (box is cls.rects['bottom'] and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is    cls.rects['top'] and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.rects['middle']
            if (box is    cls.rects['top'] and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.rects['middle'] and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.rects['bottom']
            return box
            
    black_box = pygame.image.load(os.path.join('gfx', 'backgrounds', 'blackbox.png'))
    background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout2boxes.png'))
    converted = False
    
    def __init__(self, player_mon, enemy_mon):
        super(FightMode, self).__init__()
        if not FightMode.converted:
            FightMode.black_box = FightMode.black_box.convert_alpha()
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(   FightMode.FightBoxes.rects['top']),
                FightMode.FightBoxes.textWidth(   FightMode.FightBoxes.rects['top']),
                "Attack", False, TEXT_COLOR
            )
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(FightMode.FightBoxes.rects['middle']),
                FightMode.FightBoxes.textWidth(FightMode.FightBoxes.rects['middle']),
                "Defend", False, TEXT_COLOR
            )
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(FightMode.FightBoxes.rects['bottom']),
                FightMode.FightBoxes.textWidth(FightMode.FightBoxes.rects['bottom']),
                "Escape", False, TEXT_COLOR
            )
            FightMode.background = FightMode.background.convert_alpha()
            FightMode.converted = True
        self.box_selected = FightMode.FightBoxes.rects['top']
        
    def _buttonPress(self):
        if self.box_selected == FightMode.FightBoxes.rects['top']:
            print "pressed: top"
        elif self.box_selected == FightMode.FightBoxes.rects['middle']:
            print "pressed: middle"
        elif self.box_selected == FightMode.FightBoxes.rects['bottom']:
            print "pressed: bottom"
            
    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                select = FightMode.FightBoxes.boxIn(event.pos)
                if select != FightMode.FightBoxes.elsewhere:
                    self.box_selected = select
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    select = FightMode.FightBoxes.boxIn(event.pos)
                    if select != FightMode.FightBoxes.elsewhere:
                        self.box_selected = select
                        self._buttonPress()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._buttonPress()
                else:
                    self.box_selected = FightMode.FightBoxes.boxKey(self.box_selected, event.key)
                    
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(FightMode.background, (0,0))
        if self.box_selected != FightMode.FightBoxes.elsewhere:
            screen.blit(FightMode.black_box, self.box_selected)
        #draw some mons and stuff
            