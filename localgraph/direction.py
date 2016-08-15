class Direction:
    _instances = dict()

    @classmethod
    def reset(cls):
        cls._instances.clear()

    @classmethod
    def dir(cls):
        for direction in cls._instances.values():
            yield direction

    def __init__(self, name):
        assert str(name).lower() not in Direction._instances
        Direction._instances[str(name).lower()] = self
        self._name = name

    def __repr__(self):
        return "Direction(%r)" % self._name

    def __str__(self):
        return self._name.lower()

    @property
    def name(self):
        return self._name
