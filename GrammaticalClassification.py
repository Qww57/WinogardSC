import treetaggerwrapper
import unittest


class TreeTaggerWord:
    def __init__(self, triplet):
        self.word, self.postag, self.lemma = triplet


def analyze(sentence):
    """
    List of tags: http://courses.washington.edu/hypertxt/csar-v02/penntable.html
    :param sentence:
    :return:
    """

    # Initializing the tagger in English
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR='/TreeTagger')
    tags = tagger.TagText(sentence)

    # Improving the result layout
    def tag(output):
        words = []
        for w in output:
            words.append(TreeTaggerWord(w.split("\t")))
        return words

    data = tag(tags)
    return data


def tag_str(sentence):
    data = analyze(sentence)
    results = ""
    for x in data:
        results += x.postag + " "
    return results


def tag_list(sentence):
    data = analyze(sentence)
    results = []
    for x in reversed(data):
        results.insert(-1, x.postag)
    return results


class TestAnalyze(unittest.TestCase):

    example = "The city councilmen refused the demonstrators a permit because they feared violence."

    def test_analyze(self):
        results = analyze(self.example)
        print("Words tagged:{}".format(tag_list(self.example)))
        for r in results:
            print("Word: {}, postag: {}, lemma: {}".format(r.word, r.postag, r.lemma))
        self.assertGreater(len(results), 2)