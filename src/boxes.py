import pygame

from constants import *

class Boxes(object):
    text_margin = 8
    rects = []
    # rects should be filled with pygame.Rect

    @classmethod
    def textStart(cls, pos):
        return (cls.rects[pos].x + cls.text_margin, cls.rects[pos].y + cls.text_margin)

    @classmethod
    def textWidth(cls, pos):
        return cls.rects[pos].w - (cls.text_margin * 2)

    def __init__(self):
        self.select = 0

    def changeSelect(self, change):
        self.select += change
        self.select %= len(self.__class__.rects)
        return self.select

    def posSelect(self, pos):
        for index, rect in enumerate(self.__class__.rects):
            if rect.collidepoint(pos):
                self.select = index
                return self.select
        return None

    def numberSelect(self, num):
        self.select = min(len(self.__class__.rects) - 1, num)
        self.select = max(0, self.select)
        return self.select

    def getSelectRect(self):
        return self.__class__.rects[self.select]
