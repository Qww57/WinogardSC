from winosolver.schema.XMLParser import parse_xml, add_labels
import unittest


from winosolver.nlptools.GrammaticalClassification import *

class TestXMLParser(unittest.TestCase):

    def test_parse_XML(self):
        schema_set = parse_xml()
        self.assertEqual(len(schema_set), 273)
        for schema in schema_set:
            self.assertTrue(schema.validate())
        add_labels(schema_set)
        self.assertEqual("DCE", schema_set[6].get_type())
        self.assertEqual("DCE", schema_set[89].get_type())
        self.assertEqual("NONE", schema_set[2].get_type())
