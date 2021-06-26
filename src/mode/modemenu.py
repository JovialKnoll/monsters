import math

import pygame

import shared
from .modeconvo import ModeConvo


class ModeMenu(ModeConvo):
    def _handleLoad(self):
        if self._convo_key == "0":
            mon = shared.state.protag_mon
            mon_string = "lvl: " + str(mon.lvl) + "\n"
            mon_string += "_".join(
                [stat + ": " + str(mon.stats[stat]) + self._getSpacing(mon.stats[stat]) for stat in mon.MAIN_STATS]
            )
            mon_string += "\ndrv: " + str(mon.stats['drv']) + self._getSpacing(mon.stats['drv'])
            mon_string += "__hp: " + str(mon.stats['hpc']) + "/" + str(mon.stats['hpm'])
            self._text = mon.name + "\n" + mon_string.upper()

    @staticmethod
    def _getSpacing(stat_num: int):
        return (2 - math.ceil(math.log10(stat_num))) * "_"
