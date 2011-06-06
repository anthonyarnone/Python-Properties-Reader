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


    def test_DeleteByPrefix(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['foo1'] = 'bar'
        reader['foo2'] = 'bar'
        reader['foo3'] = 'bar'
        reader['foo4'] = 'bar'
        reader['foo5'] = 'bar'
        reader['fo'] = 'bar'

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['foo1'], 'bar')
        self.assertEqual(reader['foo2'], 'bar')
        self.assertEqual(reader['foo3'], 'bar')
        self.assertEqual(reader['foo4'], 'bar')
        self.assertEqual(reader['foo5'], 'bar')
        self.assertEqual(reader['fo'], 'bar')

        reader.deletePropertiesByKeyPrefix('foo')

        self.assertEqual(reader['foo'], None)
        self.assertEqual(reader['foo1'], None)
        self.assertEqual(reader['foo2'], None)
        self.assertEqual(reader['foo3'], None)
        self.assertEqual(reader['foo4'], None)
        self.assertEqual(reader['foo5'], None)
        self.assertEqual(reader['fo'], 'bar')


    def test_DeleteEverything(self):
        reader = properties.Properties()

        reader['garble'] = 'warble'
        reader['fo'] = 'bar'
        reader['foo'] = 'bar'
        reader['foofoo foo'] = 'bar'

        self.assertEqual(reader['garble'], 'warble')
        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['foofoo foo'], 'bar')

        reader.deleteProperty('garble')
        reader.deletePropertiesByKeyPrefix('fo')

        self.assertEqual(reader['garble'], None)
        self.assertEqual(reader['foo'], None)
        self.assertEqual(reader['foofoo foo'], None)


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


