import random

from ToolsForNLP.GrammaticalClassification import *
from sources.XMLParser import parse_xml, add_labels_ECC


class DirectCausalEventClassifier:
    """
    Naive Bayes Classifier used in order to classify scheme as Direct Causal Event or not.
    """

    def __init__(self):
        self.accuracy = 0

        # Creation of the feature set
        schemes = parse_xml()
        add_labels_ECC(schemes) # Only done on the 40 first ones
        feature_sets = [(self.features(schema), schema.get_type()) for schema in schemes[0:41]]
        random.shuffle(feature_sets)

        # TODO DELETE LATER
        for feature in feature_sets:
            print(feature)

        # Creating the train and test sets and training the classifier
        self.train_set, self.test_set, self.dev_set = feature_sets[0:20], feature_sets[20:30], feature_sets[30:41]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        self.accuracy = nltk.classify.accuracy(self.classifier, self.test_set)
        print("Accuracy of answers: {} %".format(self.accuracy * 100))

    def get_accuracy(self):
        return self.accuracy * 100

    @staticmethod
    def features(schema):
        features = {}
        snippet = analyze(schema.snippet)
        sentence = analyze(schema.sentence)

        # TODO maybe should be here the diff between sentence and snippet to avoid redundancy
        features['sentence'] = str(sentence.get_tag_sequence())
        features['snippet'] = str(snippet.get_tag_sequence())

        verb_set = [word.lemma for word in snippet if "VV" in word.postag]
        if verb_set:
            features['snippet_verb'] = verb_set[0]
        else:
            features['snippet_verb'] = ""

        # TODO not good enough here since Tree Tagger confuses preposition and conjunctions
        # TODO and we want only conjunctions --> use of NLTK
        link_set = [word.lemma for word in sentence if word.postag == "IN"]
        if link_set:
            features['logical_link'] = link_set[0]
        else:
            features['logical_link'] = ""

        return features

    def answer(self, schema):
        return self.classifier.classify(self.features(schema))

    def information(self, nb):
        return self.classifier.show_most_informative_features(nb)


class TestDirectClausalEventClassifier(unittest.TestCase):

    c = DirectCausalEventClassifier()

    def some_tests(self):
        # Should be ECC
        print("ECC? - " + self.c.answer(parse_xml()[45]))
        print("ECC? - " + self.c.answer(parse_xml()[46]))
        print("ECC? - " + self.c.answer(parse_xml()[47]))
        print("ECC? - " + self.c.answer(parse_xml()[48]))

        # Should not be ECC
        print("Not ECC? - " + self.c.answer(parse_xml()[57]))
        print("Not ECC? - " + self.c.answer(parse_xml()[58]))
        print("Not ECC? - " + self.c.answer(parse_xml()[59]))
        print("Not ECC? - " + self.c.answer(parse_xml()[60]))

        self.c.information(10)
