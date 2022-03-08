import random

import pygame
import jovialengine

from personality import Personality


class SkinTone(jovialengine.Saveable):
    __slots__ = (
        'dark',
        'light',
    )

    def __init__(self, in_dark: tuple[int, int, int], in_light: tuple[int, int, int]):
        """Hold onto the darker and lighter colors."""
        self.dark = pygame.Color(in_dark[0], in_dark[1], in_dark[2])
        self.light = pygame.Color(in_light[0], in_light[1], in_light[2])

    def save(self):
        return (self.dark.r, self.dark.g, self.dark.b), (self.light.r, self.light.g, self.light.b)

    @classmethod
    def load(cls, save_data):
        return cls(*save_data)

class Skin(object):
    start_tone = SkinTone((72, 79, 69), (123, 129, 121))
    d1 = (94, 71, 124)
    d2 = (115, 72, 169)
    d3 = (135, 72, 214)
    careful_energetic = (
        (start_tone, SkinTone(d1, (116, 144, 148)), SkinTone(d2, (110, 170, 177)), SkinTone(d3, (105, 195, 205))),
        (start_tone, SkinTone(d1, (132, 141, 163)), SkinTone(d2, (141, 152, 208)), SkinTone(d3, (150, 164, 250))),
        (start_tone, SkinTone(d1, (159, 122, 158)), SkinTone(d2, (197, 115, 196)), SkinTone(d3, (233, 108, 233))),
    )
    d1 = (97, 51, 80)
    d2 = (132, 27, 97)
    d3 = (166, 4, 114)
    affectionate_aggressive = (
        (start_tone, SkinTone(d1, (162, 117, 125)), SkinTone(d2, (201, 105, 130)), SkinTone(d3, (240, 93, 134))),
        (start_tone, SkinTone(d1, (158, 125, 81)), SkinTone(d2, (194, 121, 40)), SkinTone(d3, (229, 117, 0))),
        (start_tone, SkinTone(d1, (161, 141, 81)), SkinTone(d2, (199, 154, 41)), SkinTone(d3, (237, 166, 1))),
    )
    d1 = (27, 79, 51)
    d2 = (29, 102, 63)
    d3 = (30, 125, 75)
    energetic_affectionate = (
        (start_tone, SkinTone(d1, (157, 142, 68)), SkinTone(d2, (186, 163, 35)), SkinTone(d3, (215, 183, 3))),
        (start_tone, SkinTone(d1, (143, 147, 113)), SkinTone(d2, (164, 167, 105)), SkinTone(d3, (184, 185, 97))),
        (start_tone, SkinTone(d1, (132, 160, 86)), SkinTone(d2, (148, 186, 83)), SkinTone(d3, (163, 211, 80))),
    )
    d1 = (22, 55, 62)
    d2 = (25, 78, 87)
    d3 = (27, 100, 112)
    aggressive_careful = (
        (start_tone, SkinTone(d1, (95, 133, 110)), SkinTone(d2, (109, 162, 131)), SkinTone(d3, (122, 190, 152))),
        (start_tone, SkinTone(d1, (85, 135, 147)), SkinTone(d2, (71, 144, 157)), SkinTone(d3, (57, 152, 167))),
        (start_tone, SkinTone(d1, (117, 151, 149)), SkinTone(d2, (111, 173, 177)), SkinTone(d3, (105, 195, 205))),
    )
    del start_tone, d1, d2, d3

    @classmethod
    def random(cls, personality):
        """Return a random list of colors for levels, based on personality."""
        if personality == Personality.Affectionate:
            return random.choice(cls.affectionate_aggressive + cls.energetic_affectionate)
        if personality == Personality.Aggressive:
            return random.choice(cls.aggressive_careful + cls.affectionate_aggressive)
        if personality == Personality.Careful:
            return random.choice(cls.careful_energetic + cls.aggressive_careful)
        if personality == Personality.Energetic:
            return random.choice(cls.energetic_affectionate + cls.careful_energetic)
        return 0
