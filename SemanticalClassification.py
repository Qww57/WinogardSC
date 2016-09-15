import unittest
from nltk.corpus import wordnet as wn


def semantic_field(word, similarity):
    """
    :param similarity: threshold to accept hypernyms as result
    :param word: should be in English
    :return: set of words related to the input word
    """

    s_field = list()
    # Synonyms that share a common meaning
    for synset in wn.synsets(word):
        # Lemma: a specific sense of a specific word
        for lemma in synset.lemmas("eng"):
            s_field.insert(-1, lemma.name())
            # lemma.derivationnaly_related_forms();
            # lemma.pertainyms()
            # lemma.antonyms()

        # Hypernyms
        hyper = lambda s: s.hypernyms()

        for hyper_synset in synset.closure(hyper):
            if hyper_synset.path_similarity(synset) >= similarity:
                for hyper_lemma in hyper_synset.lemmas("eng"):
                    s_field.insert(-1, hyper_lemma.name())

    return sorted(list(set(s_field)))


def sense(word, hint, confidence):
    """
    :param word:
    :param hint:
    :param confidence: added confidence if the world has only one synset
    :return:
    """
    w_syn_set = wn.synsets(word)
    if len(w_syn_set) is 1:
        return w_syn_set[0]
    else:
        h_syn_set = wn.synsets(hint)
        current_syn = w_syn_set[0]
        current_sim = 0;

        # Running the list of synonyms sets
        for s_syn in w_syn_set:
            similarity = 0;
            div = 0
            for h_syn in h_syn_set:
                sim = wn.path_similarity(s_syn, h_syn)
                if sim is not None:
                    div += 1
                    similarity += sim

            if div is not 0:
                similarity /= div

            if similarity > current_sim:
                current_sim = similarity
                current_syn = s_syn

        return current_syn


print(sense("councilman", "violence", 0.1).definition())
print(sense("demonstrator", "violence", 0.1).definition())

print(sense("", "", 0.1).definition())

"""
s1 = wn.synsets("councilman")
s2 = wn.synsets("demonstrator")
s3 = wn.synsets("violence")

for s in s1:
    print(s)
    print(s.definition())
    print(s.examples())

# Here we have 3 different synset for demonstrator and only one of them is relevant for us
for s in s2:
    print(s)
    print(s.definition())
    similarity = 0;
    div = 0
    for l in s3:
        h = wn.path_similarity(s, l)
        if h is not None:
            div += 1
            similarity += h

    if div is not 0:
        similarity /= div
    print(similarity)
    print(s.examples())

for s in s3:
    print(s)
    print(s.definition())
    print(s.examples())
"""


class SemanticFieldExample(unittest.TestCase):

    def test_example(self):
        # Testing to get the semantic field of specific key words
        council = semantic_field('councilman', 0.2)
        demonst = semantic_field('demonstrator', 0.2)
        print("Word: {} semantics: {}".format('councilman', council))
        print("Word: {} semantics: {}".format('demonstrator', demonst))