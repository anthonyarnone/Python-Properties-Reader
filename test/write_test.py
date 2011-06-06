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

