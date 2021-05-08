import sys
import abc
import json


class Saveable(abc.ABC):
    def jsonSave(self):
        return {
            'MODULE': type(self).__module__,
            'CLASS': type(self).__qualname__,
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
        if isinstance(o, type):
            return {
                'MODULE': o.__module__,
                'CLASS': o.__qualname__,
            }
            pass
        if isinstance(o, Saveable):
            return o.jsonSave()
        return super().default(o)


def _getClass(dct: dict):
    attr = sys.modules[dct['MODULE']]
    for name in dct['CLASS'].split('.'):
        attr = getattr(attr, name)
    return attr


def decodeSaveable(dct: dict):
    if {'MODULE', 'CLASS'} == dct.keys():
        return _getClass(dct)
    if {'MODULE', 'CLASS', 'SAVEABLE'} == dct.keys():
        saveable_class = _getClass(dct)
        return saveable_class.load(dct['SAVEABLE'])
    return dct
