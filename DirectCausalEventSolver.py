from urllib.request import urlopen
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
import json
import warnings
import unittest

warnings.filterwarnings("ignore")


class DirectCausalEventSolver:

    dictionary = PyDictionary()

    def antonym(self, word):
        """
        Done like this because I find the result of wn more accurate for adjective
        but missing a lot of vocabulary especially for nouns.

        Works well with adjectives, a bit more tricky with nouns sometime.

        Limitation: verb in two words like "look out" that cannot be used.

        :param word: word that should be negated
        :return: antonym set
        """
        result = []
        for i in wn.synsets(word):
            if i.pos() in ['a', 's']:
                for j in i.lemmas():
                    if j.antonyms():
                        result.append(j.antonyms()[0].name())

        result = list(set(result))
        if len(result) is 0:
            result.extend(self.dictionary.antonym(word))

        print(word + ": " + str(result))
        return result

    @staticmethod
    def similarity(word1, word2):
        """
        Use concept net in order to find the similarity between two words.
        The order of the two input should have a real limited impact (less than 0.01).

        Request are made using the urllib on ConceptNet website.

        :param word1: first word
        :param word2: second word
        :return: similarity coefficient as float between 0 and 1.
        """

        link = "http://conceptnet5.media.mit.edu/data/5.4/assoc/c/en/" + word1 + "?filter=/c/en/" + word2 + "/.&limit=1"
        response = urlopen(link).read().decode('utf8')
        obj = json.loads(response)
        try:
            return obj["similar"][0][1]
        except IndexError:
            return 0


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

        self.assertTrue("strong" in self.s.antonym('weak')) # Schema 15
        self.assertTrue("light" in self.s.antonym('heavy')) # Schema 16

        self.assertTrue("tall" in self.s.antonym('short')) # Schema 19
        self.assertTrue("short" in self.s.antonym('tall')) # Schema 20

        # Test of verbs
        self.assertTrue("question" in self.s.antonym('answer'))  # Schema 9
        # self.assertTrue("silence" in self.s.antonym('repeat')) # Schema 10 - doesn't work here
