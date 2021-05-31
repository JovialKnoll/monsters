import csv

import mode


class ConvoChoice(object):
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
            return mode_cls
        return None


class ConvoPart(object):
    __slots__ = (
        'style',
        'text',
        'choices',
    )

    def __init__(self, style: set[str], text: str, choices: list[ConvoChoice]):
        self.style = style
        self.text = text
        self.choices = choices

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
                style = {tag.strip() for tag in next(row_iter).upper().split('|')}
                text = next(row_iter)
                choices = []
                try:
                    for i in range(len(mode.ModeConvo.buttons)):
                        choice_text = next(row_iter)
                        choice_key = next(row_iter)
                        if choice_key:
                            choice = ConvoChoice(choice_text, choice_key)
                            choices.append(choice)
                except StopIteration:
                    pass
                if not choices:
                    raise ValueError(f"The convo file {convo_file} has no choices in the row with key {key}.")
                convo_part = ConvoPart(style, text, choices)
                convo_dict[key] = convo_part
        return convo_dict
