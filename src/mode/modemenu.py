import abc
import math

import shared
from .modeconvo import ModeConvo


class ModeMenu(ModeConvo, abc.ABC):
    @staticmethod
    def _getSpacing(stat_num: int):
        return (2 - math.ceil(math.log10(stat_num))) * "_"

    def _handleLoad(self):
        if self._convo_key == "0":
            mon = shared.state.protag_mon
            mon_string = f"lvl: {mon.lvl}\n"
            mon_string += "_".join(
                [f"{stat}: {mon.stats[stat]}" + self._getSpacing(mon.stats[stat]) for stat in mon.MAIN_STATS]
            )
            mon_string += f"\ndrv: {mon.stats['drv']}/{mon.DRV_MAX}"
            mon_string += f"\n_hp: {mon.stats['hpc']}/{mon.stats['hpm']}"
            self._text = mon.name + "\n" + mon_string.upper()
