from localgraph.node import Node


class Cursor:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if Cursor._instance is None:
            Cursor._instance = self
            self._loc = Node()
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
