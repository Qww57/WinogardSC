from winosolver.dce.dce_solver import DirectCausalEventSolver
import unittest


class TestDirectCausalEventSolver(unittest.TestCase):

    s = DirectCausalEventSolver()

    def test_similarity(self):
        # Test of two times the same word
        sim_1 = self.s.similarity("score", "score")
        self.assertAlmostEqual(sim_1, 1, places=2)

        # Test of two words that should be highly related
        sim_1, sim_2 = self.s.similarity("score", "tennis"), self.s.similarity("tennis", "score")
        self.assertGreater(sim_1, 0)
        self.assertGreater(sim_2, 0)
        self.assertAlmostEqual(sim_1, sim_2, places=2)

        # Test of two words that should be somehow related
        sim_1, sim_2 = self.s.similarity("score", "bad"), self.s.similarity("bad", "score")
        self.assertGreater(sim_1, 0)
        self.assertGreater(sim_2, 0)
        self.assertAlmostEqual(sim_1, sim_2, places=2)

        # Test of two words that shouldn't be related
        sim_1, sim_2 = self.s.similarity("score", "cloud"), self.s.similarity("cloud", "score")
        self.assertEqual(sim_1, 0)
        self.assertEqual(sim_2, 0)
        self.assertAlmostEqual(sim_1, sim_2, places=2)

    def test_antonym(self):
        # Test of basic adjectives
        self.assertTrue("small" in self.s.antonym('large')) # Schema 3
        self.assertTrue("large" in self.s.antonym('small')) # Schema 4

        self.assertTrue("slow" in self.s.antonym('fast')) # Schema 11
        self.assertTrue("fast" in self.s.antonym('slow')) # Schema 12

        self.assertTrue("strong" in self.s.antonym('weak'))  # Schema 15
        self.assertTrue("light" in self.s.antonym('heavy'))  # Schema 16

        self.assertTrue("tall" in self.s.antonym('short')) # Schema 19
        self.assertTrue("short" in self.s.antonym('tall')) # Schema 20

        # Test of verbs
        self.assertTrue("question" in self.s.antonym('answer'))  # Schema 9
        # self.assertTrue("silence" in self.s.antonym('repeat')) # Schema 10 - doesn't work here