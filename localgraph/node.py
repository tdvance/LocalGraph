class Node:
    _instances = set()

    @classmethod
    def dir(cls):
        for node in cls._instances:
            yield node

    def __init__(self):
        Node._instances.add(self)
        self._connections = dict()
        self._directions = dict()

    def __iter__(self):
        return iter(self._directions.values())

    def __contains__(self, obj):
        from localgraph.cursor import Cursor
        from localgraph.item import Item
        if isinstance(obj, Cursor):
            return obj.loc is self
        if isinstance(obj, Item):
            return obj.loc is self

    def __getitem__(self, direction):
        if str(direction).lower() not in self._connections:
            return None
        return self._connections[str(direction).lower()]

    def __setitem__(self, direction, node):
        assert isinstance(node, Node)
        self._connections[str(direction).lower()] = node
        self._directions[str(direction).lower()] = direction

    def __repr__(self):
        return "Node(directions=%r)" % self._connections

    def __str__(self):
        return "Node(directions=%s)" % self._connections

    def items(self):
        from localgraph.item import Item
        for i in Item.dir():
            if i in self:
                yield i
