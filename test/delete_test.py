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


    def test_DeleteWithComments(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# some comments to make sure the" + "\n")
        f.write("group = rate" + "\n")
        f.write("# delete operation doesn't break" + "\n")
        f.write("# and maybe a blank line" + "\n")
        f.write("\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader.setProperty('water', 'chestnut')
        reader.setProperty('slick', 'willie')

        self.assertEqual(reader['group'], 'rate')
        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader.getProperty('something'), 'else')
        self.assertEqual(reader['water'], 'chestnut')

        reader.deleteProperty('water')

        self.assertEqual(reader.getProperty('water'), None)
        self.assertEqual(reader['water'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


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


    def test_DeleteByPrefixWithComments(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# some comments to make sure the" + "\n")
        f.write("group = rate" + "\n")
        f.write("# delete operation doesn't break" + "\n")
        f.write("# and maybe a blank line" + "\n")
        f.write("\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        reader['foo'] = 'bar'
        reader['foo1'] = 'bar'
        reader['foo2'] = 'bar'
        reader['fo'] = 'bar'

        reader['fo__blahdfa_helllo/amber'] = 'bar'
        reader['fo__blahdfa_helllo/blue'] = 'bar'
        reader['fo__blahdfa_helllo/red'] = 'bar'
        reader['fo__blahdfa_helllo__pro/amber'] = 'bar'
        reader['fo__blahdfa_helllo__pro/blue'] = 'bar'
        reader['fo__blahdfa_helllo__pro/red'] = 'bar'

        self.assertEqual(reader['group'], 'rate')
        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['foo1'], 'bar')
        self.assertEqual(reader['foo2'], 'bar')
        self.assertEqual(reader['fo'], 'bar')

        reader.deletePropertiesByKeyPrefix('foo')

        self.assertEqual(reader['group'], 'rate')
        self.assertEqual(reader['foo'], None)
        self.assertEqual(reader['foo1'], None)
        self.assertEqual(reader['foo2'], None)
        self.assertEqual(reader['fo'], 'bar')

        reader.deletePropertiesByKeyPrefix('fo__blahdfa_helllo/')
        self.assertEqual(reader['fo__blahdfa_helllo/amber'], None)

        reader.deletePropertiesByKeyPrefix('fo__blahdfa_helllo__pro/')
        self.assertEqual(reader['fo__blahdfa_helllo__pro/amber'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_DeleteDupKey(self):
        f = NamedTemporaryFile(delete=False)
        f.write("hello = bozo\n")
        f.write("hello = again\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['hello'], 'again')

        reader.deleteProperty('hello')
        self.assertEqual(reader['hello'], None)

        reader.write(f.name)
        reader.read(f.name)

        self.assertEqual(reader['hello'], 'bozo')

        reader.deleteProperty('hello')
        self.assertEqual(reader['hello'], None)

        reader.write(f.name)
        reader.read(f.name)

        self.assertEqual(reader['hello'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_DeleteDupKeyByPrefix(self):
        f = NamedTemporaryFile(delete=False)
        f.write("hello = bozo\n")
        f.write("hello = again\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['hello'], 'again')

        try:
            reader.deletePropertiesByKeyPrefix('hello')
        except Exception as e:
            self.fail("deletePropertiesByKeyPrefix exception: [%s]" % (e))

        self.assertEqual(reader['hello'], None)

        reader.write(f.name)
        reader.read(f.name)

        self.assertEqual(reader['hello'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_DeleteNonexistantByPrefix(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['foo1'] = 'bar'
        reader['foo2'] = 'bar'
        reader['fo'] = 'bar'

        reader['fo__blahdfa_helllo/amber'] = 'bar'
        reader['fo__blahdfa_helllo/blue'] = 'bar'
        reader['fo__blahdfa_helllo/red'] = 'bar'

        reader.deletePropertiesByKeyPrefix('fo__blahd/')
        reader.deletePropertiesByKeyPrefix('asdf')


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

        reader.write(f.name)

        reader.read(f.name)

        self.assertEqual(reader['foo'], None)
        self.assertEqual(reader['fools'], 'rush in')
        self.assertEqual(reader['more'], 'lines')
        self.assertEqual(reader['this-line-has-no-value'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


