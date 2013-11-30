import pygame
from constants import *
class Boxes(object):
    rects = {}
    elsewhere = pygame.Rect((0, 0), SCREEN_SIZE)
    
    @staticmethod
    def textStart(box):
        return (box.x + 8, box.y + 8)
        
    @staticmethod
    def textWidth(box):
        return box.w - 16
        
    @classmethod
    def boxIn(cls, pos):
        """Return a rectangle containing the position."""
        for r in cls.rects.itervalues():#for python 3.x, .values()
            if r.collidepoint(pos):
                return r
        return cls.elsewhere
        