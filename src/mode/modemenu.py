import abc

import jovialengine

from .modeconvo import ModeConvo


class ModeMenu(ModeConvo, abc.ABC):
    def _handleLoad(self):
        if self._convo_key == "0":
            self._text = jovialengine.game.getInstance().state.protag_mon.getStatText()
