import unittest
from CommonKnowledgeDataBase.WikipediaDatabase import TestWikipediaDatabase
# TODO from CommonKnowledgeDataBase.GoogleSearch import GoogleSearchTest
from DirectClausalEvent.DirectCausalEventClassifier import TestDirectClausalEventClassifier
from DirectClausalEvent.DirectCausalEventSolver import TestDirectCausalEventSolver
# TODO from ToolsForNLP.Serializer import
from ToolsForNLP.Tokenizer import TestTokenizer
from ToolsForNLP.GrammaticalClassification import TestAnalyze
from ToolsForNLP.SemanticalClassification import TestSemanticalClassification
from sources.XMLParser import TestXMLParser
# TODO from Model.Schema import TestSchema
# TODO from NaiveBayesClassifier import


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        print('stp')

    def runTest(self):
        print('stp')


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ConfigTestCase))
    return test_suite

mySuit=suite()

runner = unittest.TextTestRunner()
runner.run(mySuit)

"""suite = unittest.TestSuite()
suite.addTests(TestDirectClausalEventClassifier)
suite.addTests(TestDirectCausalEventSolver)"""