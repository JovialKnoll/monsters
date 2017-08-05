import pygame

from constants import *

class Boxes(object):
    text_margin = 8
    rects = {}
    elsewhere = pygame.Rect((0,0), SCREEN_SIZE)

    @classmethod
    def textStart(cls, box):
        return (box.x + cls.text_margin, box.y + cls.text_margin)

    @classmethod
    def textWidth(cls, box):
        return box.w - (2 * cls.text_margin)

    @classmethod
    def boxIn(cls, pos):
        """Return a rectangle containing the position."""
        for r in cls.rects.itervalues():# for python 3.x, .values()
            if r.collidepoint(pos):
                return r
        return cls.elsewhere
