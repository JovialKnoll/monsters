import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin2 import ModeTalkWin2
from .modeconvo import ModeConvo


class ModeTalkElse2(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if prev_convo_key == "2":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_game().state.protag_mon,
                Monster.atLevel(2),
                lambda: ModeTalkWin2() if jovialengine.get_game().state.fight_results[-1] == 1 else ModeTalkElse2()
            )
            return True
        return False
