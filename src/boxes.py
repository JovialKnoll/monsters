class Boxes(object):
    text_margin = 8

    __slots__ = (
        'rects',
        'backKeys',
        'forwardKeys',
        'select',
    )

    def __init__(self, rects, backKeys, forwardKeys):
        self.rects = rects
        self.backKeys = set(backKeys)
        self.forwardKeys = set(forwardKeys)
        self.select = 0

    def getSelectRect(self):
        return self.rects[self.select]

    def changeSelect(self, change):
        self.select += change
        self.select %= len(self.rects)
        return self.select

    def keySelect(self, key):
        if key in self.backKeys:
            return self.changeSelect(-1)
        elif key in self.forwardKeys:
            return self.changeSelect(1)

    def posSelect(self, pos):
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                self.select = index
                return self.select
        return None

    def numberSelect(self, num):
        if num >= 0 and num < len(self.rects):
            self.select = num
            return self.select
        return None

    def textStart(self, index):
        return (
            self.rects[index].x + self.__class__.text_margin,
            self.rects[index].y + self.__class__.text_margin,
        )

    def textWidth(self, index):
        return self.rects[index].w - (self.__class__.text_margin * 2)
