import abc

import jovialengine

from .modeconvo import ModeConvo


class ModeMenu(ModeConvo, abc.ABC):
    def _handle_load(self):
        if self._convo_key == "0":
            self._text = jovialengine.get_state().protag_mon.get_stat_text()
