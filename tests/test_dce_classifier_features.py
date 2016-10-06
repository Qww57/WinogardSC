import unittest
from winosolver.schema.XMLParser import parse_xml
from winosolver.dce.dce_classifier import features


class TestDceClassifierFeatures(unittest.TestCase):

    # TODO as real tests, not only printings

    def test_features(self):
        schemas = parse_xml()
        self.show_features(schemas[0])
        self.show_features(schemas[1])
        self.show_features(schemas[42])
        self.show_features(schemas[43])

    @staticmethod
    def show_features(self, schema):
        print(schema.sentence)
        feature_set = features(schema)
        for feature_name in feature_set:
            print(feature_name + " -> " + feature_set[feature_name])
