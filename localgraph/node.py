from localgraph.direction import Direction
from localgraph.parser import Parser


class Node:
    _instances = dict()

    @classmethod
    def reset(cls):
        cls._instances.clear()

    @classmethod
    def dir(cls):
        for node in cls._instances.values():
            yield node

    @classmethod
    def save(cls, nodes_path, directions_path):
        with open(nodes_path, 'wt') as f:
            for node in cls.dir():
                node.output_node(f)
        with open(directions_path, 'wt') as f:
            for node in cls.dir():
                node.output_directions(f)

    @classmethod
    def load(cls, nodes_path, directions_path):
        with open(nodes_path, 'rt') as f:
            while cls.input_node(f) is not None:
                pass
        with open(directions_path, 'rt') as f:
            while cls.input_directions(f) is not None:
                pass

    def __init__(self, name):
        if str(name).lower() in Node._instances:
            raise KeyError('Key %r already exists for Node' % name)
        Node._instances[str(name).lower()] = self
        self._name = name
        self._connections = dict()
        self._directions = dict()

    @property
    def name(self):
        return self._name

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
        return "Node(name=%r, directions=%r)" % (self.name,
                                                 self._connections)

    def __str__(self):
        return "Node(name=%s, directions=%s)" % (self.name,
                                                 self._connections)

    def output_node(self, writeable_open_file):
        print('Node=%s' % self.name, file=writeable_open_file)

    def output_directions(self, writeable_open_file):
        print('Node=%s' % self.name, end='', file=writeable_open_file)
        for key in self._connections:
            print(',%s=%s' % (
                self._directions[key].name, self._connections[key].name),
                  end='', file=writeable_open_file)
        print(file=writeable_open_file)

    @classmethod
    def input_node(cls, readable_open_file):
        parser = Parser.get_instance()
        if not parser.read_line(readable_open_file):
            return None
        parser.require_key('Node')
        node = Node(parser.get_value('Node'))
        parser.no_more_keys()
        return node

    @classmethod
    def input_directions(cls, readable_open_file):
        parser = Parser.get_instance()
        if not parser.read_line(readable_open_file):
            return None
        parser.require_key('Node')
        name = parser.get_value('Node')
        node = cls._instances[name.lower()]
        while parser.has_more():
            key, value = parser.get_next()
            value = Node._instances[value.lower()]
            # TODO avoid protected member
            if key.lower() in Direction._instances:
                direction = Direction._instances[key.lower()]
            else:
                direction = Direction(key)
            node[direction] = value
        return node

    def items(self):
        from localgraph.item import Item
        for i in Item.dir():
            if i in self:
                yield i
