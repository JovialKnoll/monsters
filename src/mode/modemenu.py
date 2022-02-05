import abc

import shared
from .modeconvo import ModeConvo


class ModeMenu(ModeConvo, abc.ABC):
    def _handleLoad(self):
        if self._convo_key == "0":
            self._text = shared.state.protag_mon.getStatText()
