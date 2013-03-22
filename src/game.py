#game stuff
import pygame
#I forget if this needs to inherit from object, I think it's a pygame thing?
class Game(object):
    def __init__(self):
        pygame.init()
        self.running = 1
        self.screen = pygame.display.set_mode((128, 128))
        
    def __del__(self):
        pygame.quit()
        
    def run(self):
        return self.running and self.input() and self.update() and self.draw()
        
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_q:
                    self.running = 0#setting running to 0 will end the next run
        return 1
        
    def update(self):
        return 1
        
    def draw(self):
        #draw stuff
        pygame.display.flip()
        return 1