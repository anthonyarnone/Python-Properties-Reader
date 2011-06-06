import unittest

import properties

from tempfile import NamedTemporaryFile
import os

class ExceptionTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SetPropertiesException(self):

        reader = properties.Properties()

        self.assertRaises(properties.PropertiesException, reader.setProperty, 3, 'foo')
        self.assertRaises(properties.PropertiesException, reader.setProperty, 'foo', 3)


    def test_WriteToReadableFile(self):
        f = NamedTemporaryFile(delete=False)
        f.close()

        reader = properties.Properties()

        f2 = open(f.name, 'r')
        self.assertRaises(properties.PropertiesException, reader.writeToStream, f2)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_EmptyPropertyKey(self):
        f = NamedTemporaryFile(delete=False)
        f.write(" = " + "\n")
        f.close()

        reader = properties.Properties()

        self.assertRaises(properties.PropertiesException, reader.read, f.name)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


        f = NamedTemporaryFile(delete=False)
        f.write(" = value" + "\n")
        f.close()

        self.assertRaises(properties.PropertiesException, reader.read, f.name)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))



