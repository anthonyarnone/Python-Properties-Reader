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

