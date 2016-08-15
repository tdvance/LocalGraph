from localgraph.parser import Parser


class Item:
    _instances = dict()

    @classmethod
    def reset(cls):
        cls._instances.clear()

    @classmethod
    def dir(cls):
        for item in cls._instances.values():
            yield item

    # ensure items are saved in the right order, so if i1 contains i2,
    # i2 gets saved before i1.
    _saved = None

    @classmethod
    def _save_item(cls, item, writeable_open_file):
        if item in cls._saved:
            return
        if isinstance(item.loc, Item):
            cls._save_item(item.loc, writeable_open_file)
        cls._saved.add(item)
        item.output_item(writeable_open_file)

    @classmethod
    def save(cls, path):
        cls._saved = set()
        with open(path, 'wt') as f:
            for item in cls.dir():
                cls._save_item(item, f)
        cls._saved.clear()
        cls._saved = None

    @classmethod
    def load(cls, path):
        with open(path, 'rt') as f:
            while cls.input_item(f) is not None:
                pass

    @classmethod
    def nowhere(cls):
        for item in cls._instances.values():
            if item.loc is None:
                yield item

    def __init__(self, name):
        assert str(name).lower() not in Item._instances
        Item._instances[str(name).lower()] = self
        self._name = name
        self._loc = None

    def __contains__(self, obj):
        if isinstance(obj, Item):
            return obj.loc is self

    @property
    def name(self):
        return self._name

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
        return "Item(name=%r, loc=%r)" % (self.name, self.loc)

    def __str__(self):
        return "Item(name=%s, loc=%s)" % (self.name, self.loc)

    def items(self):
        for i in Item.dir():
            if i in self:
                yield i

    def output_item(self, writeable_open_file):
        from localgraph.node import Node
        from localgraph.cursor import Cursor
        if self.loc is None:
            loc_type = 'NoneType'
            loc_name = 'None'
        elif isinstance(self.loc, Node):
            loc_type = 'Node'
            loc_name = self.loc.name
        elif isinstance(self.loc, Item):
            loc_type = 'Item'
            loc_name = self.loc.name
        elif isinstance(self.loc, Cursor):
            loc_type = 'Cursor'
            loc_name = 'cursor'
        else:
            raise AssertionError("Code should not be able to get here")
        print('Item=%s,LocType=%s,LocName=%s' % (
            self.name, loc_type, loc_name),
              file=writeable_open_file)

    @classmethod
    def input_item(cls, readable_open_file):
        from localgraph.node import Node
        from localgraph.cursor import Cursor
        parser = Parser.get_instance()
        if not parser.read_line(readable_open_file):
            return None
        parser.require_key('Item')
        parser.require_key('LocType')
        parser.require_key('LocName')
        item = Item(parser.get_value('Item'))
        loc_type = parser.get_value('LocType')
        loc_name = parser.get_value('LocName')
        parser.no_more_keys()
        if loc_type.lower() == 'nonetype':
            assert loc_name.lower() == 'none'
            item.loc = None
        elif loc_type.lower() == 'node':
            item.loc = Node._instances[loc_name]
        elif loc_type.lower() == 'item':
            item.loc = Item._instances[loc_name]
        elif loc_type.lower() == 'cursor':
            assert loc_name.lower() == 'cursor'
            item.loc = Cursor.get_instance()
        else:
            raise AssertionError("Code should not be able to get here")
        return item
