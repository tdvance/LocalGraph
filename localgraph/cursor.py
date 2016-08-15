from localgraph.node import Node


class Cursor:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls):
        if cls._instance is not None:
            cls._instance._loc = cls._instance._default_loc

    def __init__(self):
        if Cursor._instance is None:
            Cursor._instance = self
            self._default_loc = Node('default home node')
            self._loc = self._default_loc
        else:
            raise PermissionError("Attempt to run constructor on singleton")

    def __contains__(self, item):
        return item.loc == self

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, node):
        assert isinstance(node, Node)
        self._loc = node

    def __repr__(self):
        return "Cursor(loc=%r)" % self.loc

    def __str__(self):
        return "Cursor(loc=%s)" % self.loc

    def items(self):
        from localgraph.item import Item
        for i in Item.dir():
            if i in self:
                yield i

    def go(self, direction):
        node = self.loc[direction]
        assert node is not None
        self.loc = node

    def get(self, item):
        assert item in self.loc
        item.loc = self

    def drop(self, item):
        assert item in self
        item.loc = self.loc

    def save_state(self, path):
        with open(path, 'wt') as f:
            print('CursorLoc=%s' % self.loc.name, file=f)

    def load_state(self, path):
        from localgraph.parser import Parser
        from localgraph.node import Node
        parser = Parser.get_instance()
        with open(path, 'rt') as f:
            assert parser.read_line(f)
            parser.require_key('CursorLoc')
            # TODO fix protected field access
            self.loc = Node._instances[parser.get_value('CursorLoc')]
            parser.no_more_keys()
            assert not parser.read_line(f)
