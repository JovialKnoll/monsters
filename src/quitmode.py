from gamemode import *
import pygame
class QuitMode(GameMode):
    def __init__(self):
        super(QuitMode, self).__init__()
        self.choice = 0#1:Continue, 2:Save & Quit, 3:Quit
        self.just_made = True
        
    def input(self, event_list):
        #this chould be replaced with actually buttons maybe
        #or could also have actual buttons
        for event in event_list:
            if event.type == pygame.QUIT:
                self.choice = 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.choice = 1
                if event.key == pygame.K_s:
                    self.choice = 2
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.choice = 3
                    
    def update(self):
        pass
        
    def draw(self, screen):
        #just to show that the game is 'paused', in quit mode, something better should be here later
        if self.just_made:
            disp_text = "Options:\nContinue (C),\nSave & Quit (S),\nQuit (Q)"
            self.shared['font_wrap'].renderToInside(screen, (0,0), 16 * 8, disp_text, False, (255,255,255), (0,0,0))
            self.just_made = False
            