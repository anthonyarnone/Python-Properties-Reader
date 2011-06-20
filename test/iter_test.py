import unittest

import properties

import os

class IterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Keys(self):
        reader = properties.Properties()

        test_props ={
                'foo1': 'bar6',
                'foo2': 'bar5',
                'foo3': 'bar4',
                'foo4': 'bar3',
                'foo5': 'bar2',
                'foo6': 'bar1'}

        for (k, v) in test_props.iteritems():
            reader[k] = v
            self.assertTrue(k in reader.keys())

        for k in reader.keys():
            self.assertTrue(k in test_props.keys())
            self.assertEqual(reader[k], test_props[k])


