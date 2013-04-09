import pygame
from monster import *
class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = 1
        self.screen = pygame.display.set_mode((256, 256))
        self.test_mon = Monster()
        
    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()
        
    def run(self):
        """Run the game, and check if the game needs to end."""
        return self.running and self.input() and self.update() and self.draw()
        
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
                if event.key == pygame.K_SPACE:
                    self.test_mon = Monster()
        return 1
        
    def update(self):
        """Update things as needed."""
        return 1
        
    def draw(self):
        """Draw things as needed."""
        self.test_mon.draw(self.screen)
        pygame.display.flip()
        return 1