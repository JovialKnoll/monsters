import jovialengine

from monster import Monster
from .modefight import ModeFight
from .modetalkwin3 import ModeTalkWin3
from .modetalkelse3 import ModeTalkElse3
from .modemenu import ModeMenu


class ModeMenu3(ModeMenu):
    def _handle_button(self, prev_convo_key, index):
        if prev_convo_key == "3aa":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_state().protag_mon,
                Monster.at_level(3),
                lambda: ModeTalkWin3() if jovialengine.get_state().fight_results[-1] == 1 else ModeTalkElse3()
            )
            return True
        return False
