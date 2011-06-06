import unittest

import properties

from tempfile import NamedTemporaryFile
import os

class EscapingTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_colonEscaping(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# comment line :  ====  :  dfa" + "\n")
        f.write("this\\:line = has\\:colons" + "\n")
        f.write("so\\:\\:does:this\\:one" + "\n")
        f.write("escaped_python = {'foo' \\: 'bar'}" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['this:line'], 'has:colons')
        self.assertEqual(reader['so::does'], 'this:one')
        self.assertEqual(reader['escaped_python'], '{\'foo\' : \'bar\'}')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    def test_equalsEscaping(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# comment line :  ====  :  dfa" + "\n")
        f.write("this\\=line = has\\=equals" + "\n")
        f.write("so\\=\\=does=this\\=one" + "\n")
        f.write("escaped_math = 3 + 5 \\= 8" + "\n")
        f.write("3 + 5 \\= 8 = still_visible")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['this=line'], 'has=equals')
        self.assertEqual(reader['so==does'], 'this=one')
        self.assertEqual(reader['escaped_math'], '3 + 5 = 8')
        self.assertEqual(reader['3 + 5 = 8'], 'still_visible')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    def test_spaceEscaping(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# comment line :  ====  :  dfa" + "\n")
        f.write("this\\ line = has\\ spaces" + "\n")
        f.write("so\\ \\ does=this\\ one" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['this line'], 'has spaces')
        self.assertEqual(reader['so  does'], 'this one')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    # since we always use a real delimiter, spaces don't need to be escaped
    #  when written to a file
    def test_fixSpaceEscapingInFile(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# comment line :  ====  :  dfa" + "\n")
        f.write("this\\ line has\\ spaces" + "\n")
        f.write("so\\ \\ does this\\ one" + "\n")
        f.close()

        f2 = open(f.name, 'r')
        lines = f2.readlines()
        f2.close()

        self.assertTrue("this\\ line has\\ spaces" + "\n" in lines)
        self.assertTrue("so\\ \\ does this\\ one" + "\n" in lines)
        self.assertFalse("this line = has spaces" + "\n" in lines)
        self.assertFalse("so  does = this one" + "\n" in lines)

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['this line'], 'has spaces')
        self.assertEqual(reader['so  does'], 'this one')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

        del f
        f = NamedTemporaryFile(delete=False)
        f.close()
        reader.write(f.name)

        f2 = open(f.name, 'r')
        lines = f2.readlines()
        f2.close()

        self.assertFalse("this\\ line has\\ spaces" + "\n" in lines)
        self.assertFalse("so\\ \\ does this\\ one" + "\n" in lines)
        self.assertTrue("this line = has spaces" + "\n" in lines)
        self.assertTrue("so  does = this one" + "\n" in lines)

        reader.read(f.name)
        self.assertEqual(reader['this line'], 'has spaces')
        self.assertEqual(reader['so  does'], 'this one')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_multiEscaping(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# comment line :  ====  :  dfa" + "\n")
        f.write("this\\ line = has\\ spaces" + "\n")
        f.write("this\\=line = has\\=equals" + "\n")
        f.write("this\\:line = has\\:colons" + "\n")
        f.write("this\\:line\\=has\\ all = kinds\\:of\\=escaped\\ characters" + "\n")
        f.write("# another comment line :  ====  :  dfa" + "\n")
        f.write("windows_path = C\\:\\\\Program Files\\\\R\\\\R-2.11.1-x64\\\\bin\\\\R.exe" + "\n")
        f.write("C\\:\\\\Program Files\\\\R\\\\R-2.11.1-x64\\\\bin\\\\R.exe = still_visible" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['this:line'], 'has:colons')
        self.assertEqual(reader['this line'], 'has spaces')
        self.assertEqual(reader['this=line'], 'has=equals')
        self.assertEqual(reader['this:line=has all'], 'kinds:of=escaped characters')
        self.assertEqual(reader['windows_path'], 'C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe')
        self.assertEqual(reader['C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe'], 'still_visible')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


    def test_multiEscapingThroughFile(self):
        f = NamedTemporaryFile(delete=False)
        f.write("# comment line :  ====  :  dfa" + "\n")
        f.write("this\\ line = has\\ spaces" + "\n")
        f.write("this\\=line = has\\=equals" + "\n")
        f.write("this\\:line = has\\:colons" + "\n")
        f.write("this\\:line\\=has\\ all = kinds\\:of\\=escaped\\ characters" + "\n")
        f.write("# another comment line :  ====  :  dfa" + "\n")
        f.write("windows_path = C\\:\\\\Program Files\\\\R\\\\R-2.11.1-x64\\\\bin\\\\R.exe" + "\n")
        f.write("C\\:\\\\Program Files\\\\R\\\\R-2.11.1-x64\\\\bin\\\\R.exe = still_visible" + "\n")
        f.close()

        reader = properties.Properties()
        reader.read(f.name)

        self.assertEqual(reader['this:line'], 'has:colons')
        self.assertEqual(reader['this line'], 'has spaces')
        self.assertEqual(reader['this=line'], 'has=equals')
        self.assertEqual(reader['this:line=has all'], 'kinds:of=escaped characters')
        self.assertEqual(reader['windows_path'], 'C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe')
        self.assertEqual(reader['C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe'], 'still_visible')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

        reader['this:requires some='] = 'escaping:for=sure'
        self.assertEqual(reader['this:requires some='], 'escaping:for=sure')

        del f
        f = NamedTemporaryFile(delete=False)
        f.close()
        reader.write(f.name)

        reader2 = properties.Properties()
        reader2.read(f.name)

        self.assertEqual(reader2['this:line'], 'has:colons')
        self.assertEqual(reader2['this line'], 'has spaces')
        self.assertEqual(reader2['this=line'], 'has=equals')
        self.assertEqual(reader2['this:line=has all'], 'kinds:of=escaped characters')
        self.assertEqual(reader2['windows_path'], 'C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe')
        self.assertEqual(reader2['C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe'], 'still_visible')
        self.assertEqual(reader2['this:requires some='], 'escaping:for=sure')

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))


