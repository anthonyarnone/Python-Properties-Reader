import unittest

import properties

from tempfile import NamedTemporaryFile
import os

class LineOrderTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_LineOrder(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# XXX" + "\n")
        f.write("foo = bar" + "\n")
        f.write("# YYY" + "\n")
        f.write("fools : rush in" + "\n")
        f.write("# ZZZ" + "\n")
        f.write("more = lines" + "\n")
        f.write("space      =       around the separator" + "\n")
        f.write("this-line-has-no-value" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        reader['more'] = 'chocolate!'
        reader['foo'] = 'food'

        f2 = open(f.name, 'w')
        reader.write(f2)
        f2.close()

        f2 = open(f.name, 'r')
        lines = f2.readlines()
        f2.close()

        self.assertTrue(lines.index("# XXX" + "\n") < lines.index("foo = food" + "\n"))
        self.assertTrue(lines.index("foo = food" + "\n") < lines.index("# YYY" + "\n"))
        self.assertTrue(lines.index("# YYY" + "\n") < lines.index("fools = rush in" + "\n"))
        self.assertTrue(lines.index("fools = rush in" + "\n") < lines.index("# ZZZ" + "\n"))
        self.assertTrue(lines.index("# ZZZ" + "\n") < lines.index("more = chocolate!" + "\n"))
        self.assertTrue(lines.index("more = chocolate!" + "\n") < lines.index("space = around the separator" + "\n"))
        self.assertTrue(lines.index("space = around the separator" + "\n") < lines.index("this-line-has-no-value = " + "\n"))

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    def test_LineOrderWithDelete(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# XXX" + "\n")
        f.write("foo = bar" + "\n")
        f.write("# YYY" + "\n")
        f.write("fools : rush in" + "\n")
        f.write("# ZZZ" + "\n")
        f.write("more = lines" + "\n")
        f.write("space      =       around the separator" + "\n")
        f.write("this-line-has-no-value" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        reader['more'] = 'chocolate!'
        reader['foo'] = 'food'
        reader.deleteProperty('space')

        f2 = open(f.name, 'w')
        reader.write(f2)
        f2.close()

        f2 = open(f.name, 'r')
        lines = f2.readlines()
        f2.close()

        self.assertTrue(lines.index("# XXX" + "\n") < lines.index("foo = food" + "\n"))
        self.assertTrue(lines.index("foo = food" + "\n") < lines.index("# YYY" + "\n"))
        self.assertTrue(lines.index("# YYY" + "\n") < lines.index("fools = rush in" + "\n"))
        self.assertTrue(lines.index("fools = rush in" + "\n") < lines.index("# ZZZ" + "\n"))
        self.assertTrue(lines.index("# ZZZ" + "\n") < lines.index("more = chocolate!" + "\n"))
        self.assertTrue(lines.index("more = chocolate!" + "\n") < lines.index("this-line-has-no-value = " + "\n"))

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


