from winosolver.dce.features_tools import *
from winosolver.schema.XMLParser import parse_xml
import unittest


class TestFeaturesTools(unittest.TestCase):

    schemas = parse_xml()

    def test_similarity(self):
        # Test of two times the same word
        sim_1 = similarity("score", "score")
        self.assertAlmostEqual(sim_1, 1, places=2)

        # Test of two words that should be highly related
        sim_1, sim_2 = similarity("score", "tennis"), similarity("tennis", "score")
        self.assertGreater(sim_1, 0)
        self.assertGreater(sim_2, 0)
        self.assertEqual(sim_1, sim_2)

        # Test of two words that should be somehow related
        sim_1, sim_2 = similarity("score", "bad"), similarity("bad", "score")
        self.assertGreater(sim_1, 0)
        self.assertGreater(sim_2, 0)
        self.assertEqual(sim_1, sim_2)

        # Test of two words that shouldn't be related
        sim_1, sim_2 = similarity("score", "cloud"), similarity("cloud", "score")
        self.assertEqual(sim_1, 0)
        self.assertEqual(sim_2, 0)
        self.assertEqual(sim_1, sim_2)

    def test_antonym(self):
        # Test of basic adjectives
        self.assertTrue("small" in antonym('large')) # Schema 3
        self.assertTrue("large" in antonym('small')) # Schema 4

        self.assertTrue("slow" in antonym('fast')) # Schema 11
        self.assertTrue("fast" in antonym('slow')) # Schema 12

        self.assertTrue("strong" in antonym('weak'))  # Schema 15
        self.assertTrue("light" in antonym('heavy'))  # Schema 16

        self.assertTrue("tall" in antonym('short')) # Schema 19
        self.assertTrue("short" in antonym('tall')) # Schema 20

        # Test of verbs
        self.assertTrue("question" in antonym('answer'))  # Schema 9
        # self.assertTrue("silence" in self.s.antonym('repeat')) # Schema 10 - doesn't work here

    def test_get_main_prop(self):
        print(get_main_prop(self.schemas[0]))
        print(get_main_prop(self.schemas[1]))
        print(get_main_prop(self.schemas[2]))
        print(get_main_prop(self.schemas[3]))
        print(get_main_prop(self.schemas[6]))
        print(get_main_prop(self.schemas[7]))

    def test_get_link(self):
        self.assertEqual('because', get_link(self.schemas[0]))
        self.assertEqual('because', get_link(self.schemas[1]))
        self.assertEqual('because', get_link(self.schemas[2]))
        self.assertEqual('because', get_link(self.schemas[3]))
        self.assertEqual('but', get_link(self.schemas[6]))
        self.assertEqual('but', get_link(self.schemas[7]))