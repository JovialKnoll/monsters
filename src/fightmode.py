import os, pygame
from gamemode import *
class FightMode(GameMode):
    black_box = pygame.image.load(os.path.join('gfx', 'backgrounds', 'blackbox.png'))
    background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout2boxes.png'))
    #put text in background here
    converted = False
    def __init__(self, player_mon, enemy_mon):
        super(FightMode, self).__init__()
        if not FightMode.converted:
            FightMode.black_box = FightMode.black_box.convert_alpha()
            FightMode.background = FightMode.background.convert_alpha()
            FightMode.converted = True
        
    def input(self, event_list):
        pass
        
    def update(self):
        pass
        
    def draw(self, screen):
        pass
        