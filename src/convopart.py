import csv

import mode


class ConvoButton(object):
    __slots__ = (
        'text',
        'key',
    )

    def __init__(self, text: str, key: str):
        self.text = text
        self.key = key

    def getNextMode(self):
        if hasattr(mode, self.key):
            mode_cls = getattr(mode, self.key)
            # currently only handling modes that can be created with no arguments
            return mode_cls()
        return None

class ConvoPart(object):
    __slots__ = (
        'style',
        'text',
        'buttons',
    )

    def __init__(self, style: set[str], text: str, buttons: list[ConvoButton]):
        self.style = style
        self.text = text
        self.buttons = buttons

    @staticmethod
    def getConvoDict(convo_file: str):
        convo_dict = {}
        with open(convo_file) as convo_data:
            convo_reader = csv.reader(convo_data)
            for row in convo_reader:
                row_iter = iter(row)
                key = next(row_iter)
                if key in convo_dict:
                    raise ValueError(f"The convo file {convo_file} has a duplicate row key {key}.")
                style = {tag.strip() for tag in next(row_iter).split('|')}
                text = bytes(next(row_iter), 'utf-8').decode('unicode_escape')
                buttons = []
                try:
                    for i in range(len(mode.ModeConvo.boxes.rects)):
                        button_text = next(row_iter)
                        button_key = next(row_iter)
                        if button_key:
                            button = ConvoButton(button_text, button_key)
                            buttons.append(button)
                except StopIteration:
                    pass
                if not buttons:
                    raise ValueError(f"The convo file {convo_file} has no buttons in the row with key {key}.")
                convo_part = ConvoPart(style, text, buttons)
                convo_dict[key] = convo_part
        return convo_dict
