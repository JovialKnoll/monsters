import sys
import abc
import json


class Saveable(abc.ABC):
    def jsonSave(self):
        return {
            'MODULE': type(self).__module__,
            'CLASS': type(self).__name__,
            'SAVEABLE': self.save(),
        }

    @abc.abstractmethod
    def save(self):
        """Return an object represented all the information that should be saved from this mode."""
        raise NotImplementedError(
            type(self).__name__ + ".saveMode(self)"
        )

    @classmethod
    @abc.abstractmethod
    def load(cls, save_data):
        """Take in an object equivalent to the result of a call to saveMode(), and return an instance of this mode."""
        raise NotImplementedError(
            cls.__name__ + ".loadMode(cls, saveData)"
        )


class SaveableJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Saveable):
            return o.jsonSave()
        return super().default(o)


def decode_saveable(dct: dict):
    if {'MODULE', 'CLASS', 'SAVEABLE'} == dct.keys():
        saveable_class = getattr(sys.modules[dct['MODULE']], dct['CLASS'])
        return saveable_class.load(dct['SAVEABLE'])
    return dct
