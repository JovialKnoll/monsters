import math

import pygame

import shared
from .modemonconvo import ModeMonConvo


class ModeMenu(ModeMonConvo):
    __slots__ = (
    )

    def _textMain(self):
        mon = shared.state.protag_mon
        mon_string = "lvl: " + str(mon.lvl) + "\n"
        mon_string += "_".join(
            [stat + ": " + str(mon.stats[stat]) + self.getSpacing(mon.stats[stat]) for stat in mon.MAIN_STATS]
        )
        mon_string += "\ndrv: " + str(mon.stats['drv']) + self.getSpacing(mon.stats['drv'])
        mon_string += "__hp: " + str(mon.stats['hpc']) + "/" + str(mon.stats['hpm'])
        return mon.name + "\n" + mon_string.upper()

    @staticmethod
    def getSpacing(stat_num: int):
        return (2 - math.ceil(math.log10(stat_num))) * "_"

    def _textButton(self, index):
        if index == 0:
            return "Wanna Talk?"
        elif index == 1:
            return "Look for Trouble"
        elif index == 2:
            # mmm, maybe something else here
            return "Time for a Checkup"
        elif index == 3:
            return "Take a Break"

    def _goButton(self, index):
        if index == 0:
            print("Go to a convo?")
        elif index == 1:
            print("Go to a fight?")
        elif index == 2:
            # uhhhh
            print("Something?")
        elif index == 3:
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
