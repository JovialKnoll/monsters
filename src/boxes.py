import constants

class Boxes(object):
    text_margin = 8
    rects = []
    # rects should be filled with pygame.Rect

    @classmethod
    def textStart(cls, index):
        return (cls.rects[index].x + cls.text_margin, cls.rects[index].y + cls.text_margin)

    @classmethod
    def textWidth(cls, index):
        return cls.rects[index].w - (cls.text_margin * 2)

    def __init__(self):
        self.select = 0

    def getSelectRect(self):
        return self.__class__.rects[self.select]

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
        if num >= 0 and num < len(self.__class__.rects):
            self.select = num
            return self.select
        return None
