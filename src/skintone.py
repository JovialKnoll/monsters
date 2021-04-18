import pygame


class SkinTone(object):
    def __init__(self, in_dark, in_light):
        """Hold onto the darker and lighter colors."""
        self.dark = pygame.Color(in_dark[0], in_dark[1], in_dark[2])
        self.light = pygame.Color(in_light[0], in_light[1], in_light[2])
