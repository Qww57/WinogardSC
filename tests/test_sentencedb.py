from winosolver.commonknowledge.SentenceDatabase import *
import unittest

# Some tests
get_frequent_related_itemsets(["dog"], 5)
get_frequent_related_itemsets(["cat", "eats"], 5)
get_frequent_related_itemsets(["cats", "eat"], 5)

# Causal relation so happened before
results = []
results.extend(get_frequent_related_itemsets(["asked", "forgot"], 5)[1])
results.extend(get_frequent_related_itemsets(["asks", "forgot"], 5)[1])
results.extend(get_frequent_related_itemsets(["ask", "forget"], 5)[1])
for result in results:
    print(result)


class TestSentenceDataBase(unittest.TestCase):

    def get_sentences(self):  # TODO PROPERLY
        sentences = get_sentences(["Dog", "Cat"], "Additive")
        self.assertGreaterEqual(len(sentences), 0)
        print(len(sentences))
        sentences.extend(get_sentences(["Cat", "Mouse"], "Exclusive"))
        print(len(sentences))
        sentences = get_sentences(["Dog", "Cat"], "Exclusive")
        print(len(sentences))
