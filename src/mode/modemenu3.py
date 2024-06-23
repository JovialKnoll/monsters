import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin3 import ModeTalkWin3
from .modetalkelse3 import ModeTalkElse3
from .modemenu import ModeMenu


class ModeMenu3(ModeMenu):
    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "3aa":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_game().state.protag_mon,
                Monster.atLevel(3),
                lambda: ModeTalkWin3() if jovialengine.get_game().state.fight_results[-1] == 1 else ModeTalkElse3()
            )
            return True
        return False
