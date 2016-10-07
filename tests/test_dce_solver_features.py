import warnings
import unittest
from winosolver.schema.XMLParser import parse_xml
from winosolver.dce.dce_solver import features

warnings.filterwarnings("ignore")


class TestDceSolverFeatures(unittest.TestCase):

    # TODO as real tests, not only printings

    def test_features(self):
        schemas = parse_xml()
        self.show_features(schemas[0])
        self.show_features(schemas[43])

    @staticmethod
    def show_features(schema):
        print(schema.sentence)
        feature_set = features(schema)
        for feature_name in feature_set:
            print(feature_name + " -> " + str(feature_set[feature_name]))
