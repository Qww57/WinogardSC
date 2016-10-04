
import unittest


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        print('stp')

    def runTest(self):
        print('Running test suite')


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ConfigTestCase))
    return test_suite

mySuit = suite()

runner = unittest.TextTestRunner()
runner.run(mySuit)
