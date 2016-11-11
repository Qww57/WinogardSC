from winosolver.nlptools.GrammaticalClassification import analyze
import unittest


class TestAnalyze(unittest.TestCase):

    example = "The city councilmen refused the demonstrators a permit because they feared violence."

    def test_iteration(self):
        sentence = analyze(self.example)
        print([word.lemma for word in sentence if word.postag == "IN"])

    def test_iteration(self):
        sentence = analyze(self.example)
        print([word.lemma for word in sentence if "VV" in word.postag])

    def test_analyze(self):
        results = analyze(self.example)
        results.print()
        print(results.get_word_sequence())
        print(results.get_tag_sequence())
        print(results.get_lemma_sequence())
        self.assertGreater(len(results), 2)