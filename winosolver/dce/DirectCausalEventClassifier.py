import random

import nltk

from winosolver import Serializer
from winosolver.nlptools.GrammaticalClassification import *
from winosolver.schema.XMLParser import parse_xml, add_labels_ECC


def features(schema):
    features = {}
    snippet = analyze(schema.snippet)
    sentence = analyze(schema.sentence)

    # TODO maybe should be here the diff between sentence and snippet to avoid redundancy + Specific sequence
    # X action Y link Z action / trait
    # features['sentence'] = str(sentence.get_tag_sequence())

    # TODO should be different here, maybe something like a true false on a specific sequence
    features['snippet'] = str(snippet.get_tag_sequence())

    # TODO categorize schema_type of verb like action or state
    verb_set = [word.lemma for word in snippet if "VV" in word.postag]
    if verb_set:
        features['snippet_verb'] = verb_set[0]
    else:
        features['snippet_verb'] = ""

    # TODO not good enough here since Tree Tagger confuses preposition and conjunctions
    # TODO and we want only conjunctions --> use of NLTK
    # TODO replace then by schema_type of conjunction (causal, concession, etc)
    link_set = [word.lemma for word in sentence if word.postag == "IN"]
    if link_set:
        features['logical_link'] = link_set[0]
    else:
        features['logical_link'] = ""

    # TODO add feature with case of the Y, COI or COD

    return features


class DirectCausalEventClassifier:

    """
    Classifier used in order to classify scheme as Direct Causal Event or not
    """

    classifiers = {
        'naive_bayes' : nltk.NaiveBayesClassifier,
        'decision_tree' : nltk.DecisionTreeClassifier
    }

    def __init__(self, classifier_type):
        """

        :param classifier_type: schema_type of classifier chosen
        """
        self.accuracy = 0
        self.classifier_type = classifier_type

        # Creation of the feature set
        schemes = parse_xml()
        add_labels_ECC(schemes) # Only done on the 160 first ones
        feature_sets = [(features(schema), schema.get_type()) for schema in schemes[0:159]]
        random.shuffle(feature_sets)

        # [print(feature) for feature in feature_sets] # TODO DELETE LATER

        # Creating the train and test sets and training the classifier
        self.train_set, self.dev_set, self.test_set = feature_sets[0:90], feature_sets[91:119], feature_sets[120:159]
        self.classifier = self.classifiers[classifier_type].train(self.train_set)
        self.accuracy = nltk.classify.accuracy(self.classifier, self.test_set)
        print("Accuracy of answers: {} %".format(self.accuracy * 100))

    def get_classifier(self):
        return self.classifier

    def get_classifier_type(self):
        return self.classifier_type

    def get_accuracy(self):
        return self.accuracy * 100

    def answer(self, schema):
        return self.classifier.classify(features(schema))

    def information(self, nb):
        return self.classifier.show_most_informative_features(nb)

    def save_classifier(self, name):
        Serializer.save(self.classifier, name)
