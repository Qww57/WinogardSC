from winosolver.nlptools.SemanticClassification import *
import unittest


# TODO make it like something


class TestSemanticClassification(unittest.TestCase):

    def test_example(self):
        # Testing to get the semantic field of specific key words
        council = semantic_field('councilman', 0.2)
        demonst = semantic_field('demonstrator', 0.2)
        print("Word: {} semantics: {}".format('councilman', council))
        print("Word: {} semantics: {}".format('demonstrator', demonst))
