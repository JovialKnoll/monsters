from gamemode import *
import pygame
class QuitMode(GameMode):
    def __init__(self, shared):
        super(QuitMode, self).__init__(shared)
        self.choice = 0#1:Continue, 2:Save & Quit, 3:Quit
        
    def input(self, event_list):
        #this chould be replaced with actually buttons maybe
        #or at least the display should say what buttons to press
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.choice = 1
                if event.key == pygame.K_s:
                    self.choice = 2
                if event.key == pygame.K_q:
                    self.choice = 3
                    
    def update(self):
        pass
        
    def draw(self, screen):
        #just to show that the game is 'paused', in quit mode, something better should be here later
        pygame.draw.rect(screen, (255, 15, 20), pygame.Rect(144, 36, 32, 18))
        