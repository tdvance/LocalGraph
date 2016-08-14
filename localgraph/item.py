class Item:
    _instances = set()

    @classmethod
    def dir(cls):
        for item in cls._instances:
            yield item

    @classmethod
    def nowhere(cls):
        for item in cls._instances:
            if item.loc is None:
                yield item

    def __init__(self):
        Item._instances.add(self)
        self._loc = None

    def __contains__(self, obj):
        from localgraph.item import Item
        if isinstance(obj, Item):
            return obj.loc is self

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, where):
        from localgraph.cursor import Cursor
        from localgraph.node import Node
        assert where is None or isinstance(where, Node) or isinstance(
            where, Item) or isinstance(where, Cursor)
        self._loc = where

    def __repr__(self):
        return "Item(loc=%r)" % self.loc

    def __str__(self):
        return "Item(loc=%s)" % self.loc

    def items(self):
        for i in Item.dir():
            if i in self:
                yield i
