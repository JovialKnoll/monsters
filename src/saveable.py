import abc


class Saveable(abc.ABC):
    @abc.abstractmethod
    def save(self):
        """Return a serializable object representing all the information that should be saved from this object."""
        raise NotImplementedError(
            type(self).__name__ + ".saveMode(self)"
        )

    @classmethod
    @abc.abstractmethod
    def load(cls, save_data):
        """Take in an object (the result of a call to save()), and return an instance of this object."""
        raise NotImplementedError(
            cls.__name__ + ".loadMode(cls, saveData)"
        )
