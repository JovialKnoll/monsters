class Boxes(object):
    TEXT_MARGIN = 8

    __slots__ = (
        'rects',
        '_backKeys',
        '_forwardKeys',
        'select',
    )

    def __init__(self, rects, backKeys, forwardKeys):
        self.rects = rects
        self._backKeys = set(backKeys)
        self._forwardKeys = set(forwardKeys)
        self.select = 0

    def getSelectRect(self):
        return self.rects[self.select]

    def changeSelect(self, change):
        self.select += change
        self.select %= len(self.rects)
        return self.select

    def keySelect(self, key):
        if key in self._backKeys:
            return self.changeSelect(-1)
        elif key in self._forwardKeys:
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
            self.rects[index].x + self.__class__.TEXT_MARGIN,
            self.rects[index].y + self.__class__.TEXT_MARGIN,
        )

    def textWidth(self, index):
        return self.rects[index].w - (self.__class__.TEXT_MARGIN * 2)
