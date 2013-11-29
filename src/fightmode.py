import os, pygame
from gamemode import *
from constants import *
class FightMode(GameMode):
    #class FightBoxes(object):
    #    top = pygame.Rect
    
    black_box = pygame.image.load(os.path.join('gfx', 'backgrounds', 'blackbox.png'))
    background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout2boxes.png'))
    converted = False
    
    def __init__(self, player_mon, enemy_mon):
        super(FightMode, self).__init__()
        if not FightMode.converted:
            FightMode.black_box = FightMode.black_box.convert_alpha()
            FightMode.shared['font_wrap'].renderToInside(FightMode.background, (32,  32), 72, "Attack", False, TEXT_COLOR)
            FightMode.shared['font_wrap'].renderToInside(FightMode.background, (32,  84), 72, "Defend", False, TEXT_COLOR)
            FightMode.shared['font_wrap'].renderToInside(FightMode.background, (32, 136), 72, "Escape", False, TEXT_COLOR)
            FightMode.background = FightMode.background.convert_alpha()
            FightMode.converted = True
        
    def input(self, event_list):
        pass
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(FightMode.background, (0,0))
        