import math

import shared
from monster import Monster

from personality import Personality
from .modeconvo import ModeConvo
from .modefight import ModeFight
from .modetalk0 import ModeTalk0


class ModeMenu(ModeConvo):
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
        elif self._convo_key == "3a3":
            if shared.state.protag_mon.personality == Personality.Affectionate:
                self._text = "I'm sure we'll do great."
            elif shared.state.protag_mon.personality == Personality.Aggressive:
                self._text = "Let's go win a fight!"
            elif shared.state.protag_mon.personality == Personality.Careful:
                self._text = "Be careful, okay?"
            elif shared.state.protag_mon.personality == Personality.Energetic:
                self._text = "I'm so excited!"

    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == "3a3":
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(0),
                lambda: ModeTalk0()
            )
            return True
        return False
