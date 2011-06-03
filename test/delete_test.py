import unittest

import properties

from tempfile import NamedTemporaryFile
import os

class DeleteTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_SimpleDelete(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader.setProperty('water', 'chestnut')
        reader.setProperty('slick', 'willie')

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader.getProperty('something'), 'else')
        self.assertEqual(reader['water'], 'chestnut')

        reader.deleteProperty('water')

        self.assertEqual(reader.getProperty('water'), None)
        self.assertEqual(reader['water'], None)


    def test_DeleteWithFile(self):
        f = NamedTemporaryFile(delete=False)
        f.write("foo = bar" + "\n")
        f.write("fools : rush in" + "\n")
        f.write("more = lines" + "\n")
        f.write("this-line-has-no-value" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['fools'], 'rush in')
        self.assertEqual(reader['more'], 'lines')
        self.assertEqual(reader['this-line-has-no-value'], '')

        reader.deleteProperty('foo')
        reader.deleteProperty('this-line-has-no-value')

        f2 = open(f.name, 'w')
        reader.write(f2)
        f2.close()

        reader.read(f.name)

        self.assertEqual(reader['foo'], None)
        self.assertEqual(reader['fools'], 'rush in')
        self.assertEqual(reader['more'], 'lines')
        self.assertEqual(reader['this-line-has-no-value'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


