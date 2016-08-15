class Parser:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if Parser._instance is None:
            Parser._instance = self
        else:
            raise PermissionError("Attempt to run constructor on singleton")
        self._current_line = None
        self._key_value_list = []

    def read_line(self, readable_open_file):
        try:
            self._current_line = next(readable_open_file)
            fields = self._current_line.split(',')
            self._key_value_list = []
            for field in fields:
                l = field.split('=')
                assert (len(l) == 2)
                l[0] = l[0].strip()
                l[1] = l[1].strip()
                self._key_value_list.append(tuple(l))
            return True
        except StopIteration:
            return False

    def require_key(self, key):
        for k, v in self._key_value_list:
            if k.lower() == key.lower():
                return
        raise KeyError(key)

    def get_value(self, key):
        for i in range(len(self._key_value_list)):
            if key.lower() == self._key_value_list[i][0].lower():
                value = self._key_value_list[i][1]
                del self._key_value_list[i]
                return value
        raise KeyError(key)

    def no_more_keys(self):
        assert not self._key_value_list

    def has_more(self):
        return bool(self._key_value_list)

    def get_next(self):
        return self._key_value_list.pop(0)
