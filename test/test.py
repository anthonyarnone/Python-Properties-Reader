import unittest

import simple_test
import write_test
import delete_test
import escaping_test
import line_order_test

if __name__ == '__main__':
    
    properties_suite = unittest.TestSuite()


    simple_suite = unittest.TestLoader().loadTestsFromTestCase(simple_test.SimpleTest)
    properties_suite.addTest(simple_suite)

    write_suite = unittest.TestLoader().loadTestsFromTestCase(write_test.WriteTest)
    properties_suite.addTest(write_suite)

    delete_suite = unittest.TestLoader().loadTestsFromTestCase(delete_test.DeleteTest)
    properties_suite.addTest(delete_suite)

    escpaing_suite = unittest.TestLoader().loadTestsFromTestCase(escaping_test.EscapingTest)
    properties_suite.addTest(escpaing_suite)

    line_order_suite = unittest.TestLoader().loadTestsFromTestCase(line_order_test.LineOrderTest)
    properties_suite.addTest(line_order_suite)

    unittest.TextTestRunner(verbosity=2).run(properties_suite)

    """
    import sys
    print "Creating Properties Reader"
    reader = Properties()

    reader['foo'] = 'bar'
    print "----"
    reader.write(sys.stdout)

    reader['foo'] = 'helga'
    reader['bar'] = 'helga'
    reader.setProperty('google', '.com')
    print "----"
    reader.write(sys.stdout)

    reader['google'] = '.org'
    reader.deleteProperty('bar')
    print "----"
    reader.write(sys.stdout)

    print "----"
    print "property 'google' : %s" % (reader['google'])
    print "non-existant prop 'hannibal' : %s" % (reader['hannibal'])




    reader2 = Properties()
    reader2.read('test/sample_1.properties')
    print "Escaped backslash prop: [%s]" % (reader2['windows_path'])
    print "Escaped colon prop: [%s]" % (reader2['escaped_python'])
    print "Escaped equals prop: [%s]" % (reader2['escaped_math'])
    print "Escaped colon key prop: [%s]" % (reader2['C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe'])
    print "Escaped equals key prop: [%s]" % (reader2['3 + 5 = 8'])
 
    print "----"
    reader2.write(sys.stdout)
    print "Done"
    """

