from gamemode import *
import pygame
class QuitMode(GameMode):
    def __init__(self):
        super(QuitMode, self).__init__()
        self.choice = 0#1:Continue, 2:Save & Quit, 3:Quit
        self.just_made = True
        
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
        if self.just_made:
            #pygame.draw.rect(screen, (255, 15, 20), pygame.Rect(144, 36, 32, 18))
            disp_text = "Options: Continue (C), Save & Quit (S), Quit (Q)"
            s_s = self.shared['SCREEN_SIZE']
            d_s = self.shared['font'].size(disp_text)
            screen.blit(self.shared['font'].render(disp_text, False, (255,255,255), (0,0,0)), ((s_s[0] - d_s[0])//2, (s_s[1] - d_s[1])//2))
            
            self.just_made = False
            