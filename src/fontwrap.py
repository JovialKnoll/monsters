import pygame

class FontWrap(object):
    __slots__ = (
        'font',
    )

    def __init__(self, in_font):
        self.font = in_font

    def renderTo(self, surf, dest, text, antialias, color, background=None):
        surf.blit(self.font.render(text, antialias, color, background), dest)

    def renderToCentered(self, surf, dest, text, antialias, color, background=None):
        text_size = self.font.size(text)
        surf.blit(self.font.render(text, antialias, color, background), (dest[0] - text_size[0]//2, dest[1] - text_size[1]//2))

    def renderWordsInside(self, width, words, antialias, color, background=None):
        """Returns a surface of the width with the words drawn on it.
        If any word is too long to fit, it will be in its own line, and truncated.
        """
        lines = [words[0].replace('_', ' ')]
        for word in words[1:]:
            new_word = word.replace('_', ' ')
            if self.font.size(lines[-1] + " " + new_word)[0] > width:
                lines.append(new_word)
            else:
                lines[-1] += " " + new_word

        height = self.font.get_height()
        if background is None:
            drawn_lines = [self.font.render(line, antialias, color).convert_alpha() for line in lines]
        else:
            drawn_lines = [self.font.render(line, antialias, color, background).convert() for line in lines]
        result = pygame.Surface((width, height * len(drawn_lines)), 0, drawn_lines[0])
        if background is not None:
            result.fill(background)

        for i, line in enumerate(drawn_lines):
            result.blit(line, (0, i * height))
        return result

    def renderToInside(self, surf, dest, width, text, antialias, color, background=None):
        # probably more efficient to do once?
        part_dest = [dest[0], dest[1]]
        for line in [line.split() for line in text.splitlines()]:
            if line == []:
                line = [""]
            if background is None:
                img = self.renderWordsInside(width, line, antialias, color)
            else:
                img = self.renderWordsInside(width, line, antialias, color, background)
            surf.blit(img, part_dest)
            part_dest[1] += img.get_height()

    def renderInside(self, width, text, antialias, color, background=None):
        # probably more efficient if keeping resultant surface and using that to draw over and over?
        height = 0
        imgs = []
        for line in [line.split() for line in text.splitlines()]:
            if line == []:
                line = [""]
            if background is None:
                imgs.append(self.renderWordsInside(width, line, antialias, color))
            else:
                imgs.append(self.renderWordsInside(width, line, antialias, color, background))
            height += imgs[-1].get_height()
        result = pygame.Surface((width, height), 0, imgs[0])
        dest = [0,0]
        for img in imgs:
            result.blit(img, dest)
            dest[1] += img.get_height()
        return result
