from winosolver.nlptools.Tokenizer import should_add, detect_first_names
import unittest


class TestTokenizer(unittest.TestCase):

    def test_should_add(self):
        self.assertTrue(should_add(["cat"], "cat is huge man", "Exclusive"))
        self.assertFalse(should_add(["elephant"], "cat is huge man", "Exclusive"))

        self.assertTrue(should_add(["cat"], "cat is huge man", "Inclusive"))
        self.assertFalse(should_add(["elephant"], "cat is huge man", "Inclusive"))

        self.assertTrue(should_add(["cat", "man"], "cat is huge man", "Inclusive"))
        self.assertFalse(should_add(["cat", "rat"], "cat is huge man", "Exclusive"))

    def test_detect_first_names(self):
        text = "Mary and Ann are standing hand in hand"
        names = detect_first_names(text)
        expected = ["Mary", "Ann"]
        self.assertTrue(expected == names)