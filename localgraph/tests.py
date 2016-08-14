from unittest import TestCase

from localgraph.cursor import Cursor
from localgraph.direction import Direction
from localgraph.item import Item
from localgraph.node import Node


class TestLocalGraph(TestCase):
    @classmethod
    def setUpClass(cls):
        home = Node()
        first = Node()
        second = Node()
        third = Node()
        forward = Direction('forward')
        diagonal = Direction('diagonal')
        flying_pig = Item()
        flying_piglet = Item()
        ball = Item()
        bat = Item()
        glove = Item()
        batter = Item()
        cap = Item()
        something = Item()
        something.loc = second
        something_else = Item()
        something_else.loc = Cursor.get_instance()
        Cursor.get_instance().loc = second
        ball.loc = glove
        glove.loc = Cursor.get_instance()
        bat.loc = home
        batter.loc = first
        cap.loc = batter
        home[forward] = first
        first[forward] = second
        second[forward] = third
        third[forward] = home
        home[diagonal] = second
        second[diagonal] = home
        first[diagonal] = third
        third[diagonal] = first
        assert Cursor.get_instance().loc == second
        Cursor.get_instance().go(forward)
        assert Cursor.get_instance().loc == third
        Cursor.get_instance().go(diagonal)
        assert Cursor.get_instance().loc == first
        Cursor.get_instance().go(forward)
        assert Cursor.get_instance().loc == second
        assert something_else in Cursor.get_instance()
        assert something in second
        Cursor.get_instance().get(something)
        Cursor.get_instance().drop(something_else)
        assert something in Cursor.get_instance()
        assert something_else in second

    def test_cursor_singleton(self):
        c = Cursor.get_instance()
        c1 = Cursor.get_instance()
        self.assertIsInstance(c, Cursor)
        self.assertIs(c, c1)
        try:
            c = Cursor()
            self.fail("This should have caused an exception")
        except PermissionError:
            pass

    def test_cursor_has_node(self):
        n = None
        c = Cursor.get_instance()
        for node in Node.dir():
            if c in node:
                self.assertIsNone(n)
                n = node
        self.assertIsNotNone(n)
        self.assertEqual(n, c.loc)

    def test_direction(self):
        for direction in Direction.dir():
            for node in Node.dir():
                if node[direction] is not None:
                    unique_m = None
                    for m in Node.dir():
                        if node[direction] == m:
                            self.assertIsNone(unique_m)
                            unique_m = m
                    self.assertIsNotNone(unique_m)

    def test_item_location(self):
        c = Cursor.get_instance()
        for item in Item.dir():
            # print("item=", item)
            # print("item.loc=", item.loc)
            # print("item:", item, " in c:", c, ":", item in c)
            if item.loc == None:
                self.assertFalse(item in c)
                for node in Node.dir():
                    self.assertFalse(item in node)
                for i in Item.dir():
                    self.assertFalse(item in i)
            elif item in c:
                self.assertEqual(c, item.loc)
                for node in Node.dir():
                    self.assertFalse(item in node)
                for i in Item.dir():
                    self.assertFalse(item in i)
            elif isinstance(item.loc, Node):
                n = None
                for node in Node.dir():
                    if item.loc == node:
                        self.assertTrue(item in node)
                    if item in node:
                        self.assertTrue(item.loc == node)
                        self.assertIsNone(n)
                        n = node
                self.assertIsNotNone(n)
                for i in Item.dir():
                    self.assertFalse(item in i)
                self.assertFalse(item in c)
            else:
                self.assertIsInstance(item.loc, Item)
                i = None
                for j in Item.dir():
                    if item.loc == j:
                        self.assertTrue(item in j)
                    if item in j:
                        self.assertTrue(item.loc == j)
                        self.assertIsNone(i)
                        i = j
                self.assertIsNotNone(i)
                self.assertFalse(item in c)
                for node in Node.dir():
                    self.assertFalse(item in node)

    def test_item_not_in_self(self):
        for item in Item.dir():
            self.assertFalse(item in item)

    def test_directions_node(self):
        for node in Node.dir():
            s = set(node)
            s1 = set()
            for direction in Direction.dir():
                if node[direction] is not None:
                    s1.add(direction)
            self.assertEqual(s, s1)

    def test_loc(self):
        for item in Item.dir():
            if item.loc is not None:
                self.assertTrue(item in item.loc)
                self.assertTrue(isinstance(item, (Item, Node, Cursor)))
        c = Cursor.get_instance()
        self.assertTrue(c in c.loc)

    def test_item(self):
        iset = set()

        for i in Item.nowhere():
            self.assertIsNone(i.loc)
            self.assertFalse(i in iset)
            iset.add(i)

        for item in Item.dir():
            for i in item.items():
                self.assertTrue(i in item)
                self.assertFalse(i in iset)
                iset.add(i)

        for node in Node.dir():
            for i in node.items():
                self.assertTrue(i in node)
                self.assertFalse(i in iset)
                iset.add(i)

        for i in Cursor.get_instance().items():
            self.assertTrue(i in Cursor.get_instance())
            self.assertFalse(i in iset)
            iset.add(i)

        jset = set()
        for i in Item.dir():
            jset.add(i)

        self.assertEqual(iset, jset)

    def test_circular(self):
        for item in Item.dir():
            i = item
            while isinstance(i.loc, Item):
                i = i.loc
                assert i != item
