import pygame


class Boxes(object):
    TEXT_MARGIN = 4

    __slots__ = (
        'rects',
        '_backKeys',
        '_forwardKeys',
        'select',
    )

    def __init__(self, rects: tuple[pygame.Rect, ...], back_keys, forward_keys):
        self.rects = rects
        self._backKeys = set(back_keys)
        self._forwardKeys = set(forward_keys)
        self.select = 0

    def getSelectRect(self):
        return self.rects[self.select]

    def keySelect(self, key, selectable_buttons=None):
        if key in self._backKeys:
            self.select -= 1
        elif key in self._forwardKeys:
            self.select += 1
        if selectable_buttons is None:
            self.select %= len(self.rects)
        else:
            self.select %= selectable_buttons
        return self.select

    def posSelect(self, pos: tuple[int], selectable_buttons=None):
        for index, rect in enumerate(self.rects):
            if selectable_buttons and index >= selectable_buttons:
                return None
            elif rect.collidepoint(pos):
                self.select = index
                return self.select
        return None

    def numberSelect(self, num: int):
        if 0 <= num < len(self.rects):
            self.select = num
            return self.select
        return None

    def textStart(self, index: int):
        return (
            self.rects[index].x + self.TEXT_MARGIN,
            self.rects[index].y + self.TEXT_MARGIN,
        )

    def textWidth(self, index: int):
        return self.rects[index].w - (self.TEXT_MARGIN * 2)
