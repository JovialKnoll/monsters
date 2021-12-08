import shared
from monster import Monster
from .modefight import ModeFight
from .modetalkwin1 import ModeTalkWin1
from .modeconvo import ModeConvo


class ModeTalkElse1(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == "6":
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(0),
                lambda: ModeTalkWin1() if shared.state.fight_results[-1] == 1 else ModeTalkElse1()
            )
            return True
        return False
