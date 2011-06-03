import unittest

import properties

from tempfile import NamedTemporaryFile
import os

class SimpleTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SimpleProperties(self):
        f = NamedTemporaryFile(delete=False)
        f.write("foo = bar" + "\n")
        f.write("this = is a test of space-containing values" + "\n")
        f.write("fools : rush in" + "\n")
        f.write("more = lines" + "\n")
        f.write("space      =       around the separator" + "\n")
        f.write("this-line-has-no-value" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['this'], 'is a test of space-containing values')
        self.assertEqual(reader['fools'], 'rush in')
        self.assertEqual(reader['more'], 'lines')
        self.assertEqual(reader['space'], 'around the separator')
        self.assertEqual(reader['this-line-has-no-value'], '')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_MissingProperties(self):
        f = NamedTemporaryFile(delete=False)
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['why'], None)
        self.assertEqual(reader['would anything'], None)
        self.assertEqual(reader['be : in'], None)
        self.assertEqual(reader['the = reader'], None)
        self.assertEqual(reader['????'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    def test_SpaceSeparatedProperties(self):
        f = NamedTemporaryFile(delete=False)
        f.write("foo      bar" + "\n")
        f.write("if there isn't a colon or equals, the first space will be the separator" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['if'], 'there isn\'t a colon or equals, the first space will be the separator')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_CommentsAndEmptyLines(self):
        f = NamedTemporaryFile(delete=False)
        f.write("! comment" + "\n")
        f.write("# comment starting with poind sign" + "\n")
        f.write("######   indentation : doesn't matter" + "\n")
        f.write("!!  !!! !!! hello = bozo" + "\n")
        f.write("" + "\n")
        f.write("" + "\n")
        f.write("! hiding = good" + "\n")
        f.write("" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['hello'], None)
        self.assertEqual(reader['indentation'], None)
        self.assertEqual(reader['hiding'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_Indentation(self):
        f = NamedTemporaryFile(delete=False)
        f.write("     ! indented comment" + "\n")
        f.write("     # indented comment starting with poind sign" + "\n")
        f.write("  indentation : doesn't matter" + "\n")
        f.write("     hello = bozo" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['hello'], 'bozo')
        self.assertEqual(reader['indentation'], 'doesn\'t matter')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


