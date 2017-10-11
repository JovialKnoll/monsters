import os
import pygame

from constants import *
from gamemode import *
from boxes import *

class ConvoMode(GameMode):
    class ConvoBoxes(Boxes):
        rects = [
            pygame.Rect(  8,  88,  88,  36),
            pygame.Rect(224,  88,  88,  36),
            pygame.Rect(  8, 132,  88,  36),
            pygame.Rect(224, 132,  88,  36),
        ]

        def keySelect(self, key):
            if key == pygame.K_LEFT:
                return self.changeSelect(-1)
            if key == pygame.K_RIGHT:
                return self.changeSelect(1)

    SCROLL_AMOUNT_MOUSE = 10
    SCROLL_AMOUNT_KEY = 1
    sprite_path = os.path.join(GRAPHICS_DIRECTORY, BACKGROUNDS_DIRECTORY)
    black_box = pygame.image.load(os.path.join(sprite_path, 'blackbox.png'))
    converted = False

    def _textMain(self):
        # return text for main section
        raise NotImplementedError(self.__class__.__name__ + "._textMain(self)")
    def _textButton0(self):
        # return text for button 0
        raise NotImplementedError(self.__class__.__name__ + "._textButton0(self)")
    def _textButton1(self):
        # return text for button 1
        raise NotImplementedError(self.__class__.__name__ + "._textButton1(self)")
    def _textButton2(self):
        # return text for button 2
        raise NotImplementedError(self.__class__.__name__ + "._textButton2(self)")
    def _textButton3(self):
        # return text for button 3
        raise NotImplementedError(self.__class__.__name__ + "._textButton3(self)")
    def _goButton0(self):
        # do stuff for button 0
        raise NotImplementedError(self.__class__.__name__ + "._goButton0(self)")
    def _goButton1(self):
        # do stuff for button 1
        raise NotImplementedError(self.__class__.__name__ + "._goButton1(self)")
    def _goButton2(self):
        # do stuff for button 2
        raise NotImplementedError(self.__class__.__name__ + "._goButton2(self)")
    def _goButton3(self):
        # do stuff for button 3
        raise NotImplementedError(self.__class__.__name__ + "._goButton3(self)")

    def __init__(self):
        super(ConvoMode, self).__init__()
        if not ConvoMode.converted:
            ConvoMode.black_box = ConvoMode.black_box.convert_alpha()
            ConvoMode.converted = True
        self.background = pygame.image.load(os.path.join(ConvoMode.sprite_path, 'layout1boxes.png')).convert_alpha()
        # mainly, make the surfaces based on the text for view and buttons, fitting some criteria
        self.text_rect = pygame.Rect(0, 0, 288, 48)
        self.surf_text = self.shared['font_wrap'].renderInside(288, self._textMain(), False, TEXT_COLOR)
        self.shared['font_wrap'].renderToInside(
            self.background,
            ConvoMode.ConvoBoxes.textStart(0),
            ConvoMode.ConvoBoxes.textWidth(0),
            self._textButton0(),
            False,
            TEXT_COLOR
        )
        self.shared['font_wrap'].renderToInside(
            self.background,
            ConvoMode.ConvoBoxes.textStart(1),
            ConvoMode.ConvoBoxes.textWidth(1),
            self._textButton1(),
            False,
            TEXT_COLOR
        )
        self.shared['font_wrap'].renderToInside(
            self.background,
            ConvoMode.ConvoBoxes.textStart(2),
            ConvoMode.ConvoBoxes.textWidth(2),
            self._textButton2(),
            False,
            TEXT_COLOR
        )
        self.shared['font_wrap'].renderToInside(
            self.background,
            ConvoMode.ConvoBoxes.textStart(3),
            ConvoMode.ConvoBoxes.textWidth(3),
            self._textButton3(),
            False,
            TEXT_COLOR
        )
        self.boxes = ConvoMode.ConvoBoxes()

        self.y_scroll = {'up': 0, 'down': 0}
        # what else do conversations need?

    def _buttonPress(self):
        if self.boxes.select == 0:
            self._goButton0()
        elif self.boxes.select == 1:
            self._goButton1()
        elif self.boxes.select == 2:
            self._goButton2()
        elif self.boxes.select == 3:
            self._goButton3()

    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                self.boxes.posSelect(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.boxes.posSelect(event.pos) != None:
                        self._buttonPress()
                elif event.button == 4:
                    self.text_rect.move_ip(0, -ConvoMode.SCROLL_AMOUNT_MOUSE)
                elif event.button == 5:
                    self.text_rect.move_ip(0, ConvoMode.SCROLL_AMOUNT_MOUSE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._buttonPress()
                elif event.key == pygame.K_UP:
                    self.y_scroll['up'] = ConvoMode.SCROLL_AMOUNT_KEY
                elif event.key == pygame.K_DOWN:
                    self.y_scroll['down'] = ConvoMode.SCROLL_AMOUNT_KEY
                else:
                    self.boxes.keySelect(event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.y_scroll['up'] = 0
                elif event.key == pygame.K_DOWN:
                    self.y_scroll['down'] = 0

    def update(self):
        self.text_rect.move_ip(0, self.y_scroll['down'] - self.y_scroll['up'])
        self.text_rect.clamp_ip(self.surf_text.get_rect())

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.background, (0,0))
        screen.blit(self.surf_text, (16,16), self.text_rect)
        screen.blit(ConvoMode.black_box, self.boxes.getSelectRect())
