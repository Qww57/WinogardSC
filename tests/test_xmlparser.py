from winosolver.schema.XMLParser import parse_xml, add_labels
import unittest


class TestXMLParser(unittest.TestCase):

    def test_parse_XML(self):
        schema_set = parse_xml()
        self.assertEqual(len(schema_set), 273)
        [self.assertTrue(schema.validate()) for schema in schema_set]

        add_labels(schema_set)
        self.assertEqual("DCE", schema_set[6].get_type())
        self.assertEqual("DCE", schema_set[89].get_type())
        self.assertEqual("unknown", schema_set[2].get_type())
