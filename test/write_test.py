import unittest

import properties

from tempfile import NamedTemporaryFile
import os

class WriteTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_SimpleStorage(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader.setProperty('water', 'chestnut')
        reader.setProperty('slick', 'willie')

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader.getProperty('something'), 'else')
        self.assertEqual(reader['water'], 'chestnut')

        reader.setProperty('water', 'fall')

        self.assertEqual(reader.getProperty('water'), 'fall')
        self.assertEqual(reader['water'], 'fall')


    def test_ResetOnRead(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader['water'] = 'chestnut'

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['something'], 'else')
        self.assertEqual(reader['water'], 'chestnut')

        f = NamedTemporaryFile(delete=False)
        f.close()

        reader.read(f.name)

        self.assertEqual(reader['foo'], None)
        self.assertEqual(reader['something'], None)
        self.assertEqual(reader['water'], None)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_FileWriting(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader['water'] = 'chestnut'

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['something'], 'else')
        self.assertEqual(reader['water'], 'chestnut')

        f = NamedTemporaryFile(delete=False)
        f.close()
        reader.write(f.name)

        reader2 = properties.Properties()
        reader2.read(f.name)

        self.assertEqual(reader2['foo'], 'bar')
        self.assertEqual(reader2['something'], 'else')
        self.assertEqual(reader2['water'], 'chestnut')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_FileContents(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader['water'] = 'chestnut'

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['something'], 'else')
        self.assertEqual(reader['water'], 'chestnut')

        f = NamedTemporaryFile(delete=False)
        f.close()
        reader.write(f.name)

        reader2 = properties.Properties()
        reader2.read(f.name)

        self.assertEqual(reader2['foo'], 'bar')
        self.assertEqual(reader2['something'], 'else')
        self.assertEqual(reader2['water'], 'chestnut')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_writeToStream(self):
        reader = properties.Properties()

        reader['foo'] = 'bar'
        reader['something'] = 'else'
        reader['water'] = 'chestnut'

        self.assertEqual(reader['foo'], 'bar')
        self.assertEqual(reader['something'], 'else')
        self.assertEqual(reader['water'], 'chestnut')

        f = NamedTemporaryFile(delete=False)
        reader.writeToStream(f)
        f.close()

        reader2 = properties.Properties()
        reader2.read(f.name)

        self.assertEqual(reader2['foo'], 'bar')
        self.assertEqual(reader2['something'], 'else')
        self.assertEqual(reader2['water'], 'chestnut')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_dupKeyPreservedThroughWrite(self):
        f = NamedTemporaryFile(delete=False)
        f.write("hello = bozo\n")
        f.write("hello = again\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['hello'], 'again')

        reader.write(f.name)
        reader.read(f.name)

        self.assertEqual(reader['hello'], 'again')

        f2 = open(f.name, 'r')
        lines = f2.readlines()
        f2.close()

        self.assertTrue("hello = bozo\n" in lines)
        self.assertTrue("hello = again\n" in lines)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

