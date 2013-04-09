import pygame
from monster import *
class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = 1
        self.screen = pygame.display.set_mode((256, 256))
        self.clock = pygame.time.Clock()
        
        #test stuff
        self.test_mon = Monster()
        self.fill = [255, 255, 255]
        
    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()
        
    def run(self):
        """Run the game, and check if the game needs to end."""
        return self.running and self.input() and self.update() and self.draw() and self.time()
        
    def input(self):
        """Take inputs as needed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_q:
                    self.running = 0
                #test stuff
                if event.key == pygame.K_SPACE:
                    self.test_mon = Monster()
                if event.key == pygame.K_r:
                    self.fill[0] = 255*(self.fill[0]!=255)
                if event.key == pygame.K_g:
                    self.fill[1] = 255*(self.fill[1]!=255)
                if event.key == pygame.K_b:
                    self.fill[2] = 255*(self.fill[2]!=255)
        return 1
        
    def update(self):
        """Update things as needed."""
        return 1
        
    def draw(self):
        """Draw things as needed."""
        self.screen.fill(self.fill)
        self.test_mon.draw(self.screen)
        pygame.display.flip()
        return 1
        
    def time(self):
        """Take care of time stuff."""
        pygame.display.set_caption(str(self.clock.get_fps()))
        self.clock.tick(60)
        return 1