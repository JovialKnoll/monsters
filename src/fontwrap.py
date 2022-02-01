import pygame

import constants
import shared


class FontWrap(object):
    __slots__ = (
        '_font',
    )

    def __init__(self, font_file, font_size: int):
        self._font = pygame.font.Font(font_file, font_size)

    def renderTo(self, surf: pygame.Surface, dest, text: str,
                 antialias: bool, color, background=None):
        surf.blit(self._font.render(text, antialias, color, background), dest)

    def renderToCentered(self, surf: pygame.Surface, dest, text: str,
                         antialias, color, background=None):
        text_size = self._font.size(text)
        surf.blit(
            self._font.render(text, antialias, color, background),
            (dest[0] - text_size[0] // 2, dest[1] - text_size[1] // 2)
        )

    def renderWordsInside(self, width: int, words: list[str],
                          antialias: bool, color, background=None):
        """Returns a surface of the width with the words drawn on it.
        If any word is too long to fit, it will be in its own line, and truncated.
        """
        lines = [words[0].replace('_', ' ')]
        for word in words[1:]:
            new_word = word.replace('_', ' ')
            if self._font.size(lines[-1] + " " + new_word)[0] > width:
                lines.append(new_word)
            else:
                lines[-1] += " " + new_word

        result = pygame.Surface((width, constants.FONT_HEIGHT * len(lines))).convert(shared.display.screen)
        result.fill(background)
        for i, line in enumerate(lines):
            drawn_line = self._font.render(line, antialias, color, background).convert(result)
            result.blit(drawn_line, (0, i * constants.FONT_HEIGHT))
        return result

    def renderToInside(self, surf: pygame.Surface, dest, width: int, text: str,
                       antialias: bool, color, background=None):
        # probably more efficient to do once?
        part_dest = [dest[0], dest[1]]
        for line in [line.split() for line in text.splitlines()]:
            if not line:
                line = [""]
            if background is None:
                img = self.renderWordsInside(width, line, antialias, color, constants.COLORKEY)
                img.set_colorkey(constants.COLORKEY)
            else:
                img = self.renderWordsInside(width, line, antialias, color, background)
            surf.blit(img, part_dest)
            part_dest[1] += img.get_height()

    def renderInside(self, width: int, text: str,
                     antialias: bool, color, background=None):
        # probably more efficient if keeping resultant surface and using that to draw over and over?
        height = 0
        imgs = []
        for line in [line.split() for line in text.splitlines()]:
            if not line:
                line = [""]
            imgs.append(self.renderWordsInside(width, line, antialias, color, background or constants.COLORKEY))
            height += imgs[-1].get_height()
        result = pygame.Surface((width, height)).convert(shared.display.screen)
        dest = [0, 0]
        for img in imgs:
            result.blit(img, dest)
            dest[1] += img.get_height()
        result.set_colorkey(constants.COLORKEY)
        return result
