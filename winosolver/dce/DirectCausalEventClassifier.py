import random

import nltk

from winosolver import Serializer
from winosolver.nlptools.Chunker import Chunker, get_main_pos, pre_process_document
from winosolver.nlptools.GrammaticalClassification import *
from winosolver.schema.XMLParser import parse_xml, add_labels
from winosolver.nlptools.structure_mining import *


chunker = Chunker()


def features(schema):
    feature_set = {}

    snippet = analyze(schema.snippet)
    main_prop = get_main_prop(schema)
    sentence = analyze(main_prop)

    # Creating a tree structure for the sentence
    full_structure = chunker.parse(schema.sentence)
    main_structure = get_main_pos(full_structure)

    # Main structure of the sentence after chucking: should reflect:
    # X (NP) action (VB) Y (NP) complements (?) link (IN) Z (NP) action (VB) complements (?)
    feature_set['sentence'] = str([tag for (tag, words) in main_structure])

    # Full structure of the snippet
    feature_set['snippet'] = str(snippet.get_tag_sequence())

    # TODO categorize schema_type of verb like action or state
    verb_set = [word.lemma for word in snippet if "V" in word.postag]
    if verb_set:
        feature_set['snippet_verb'] = verb_set[0]
    else:
        feature_set['snippet_verb'] = ""

    # TODO not good enough here since Tree Tagger confuses preposition and conjunctions
    # TODO and we want only conjunctions --> use of NLTK
    # TODO can also be done using the chunker in some cases, less efficient maybe
    str_main_prop = nltk.word_tokenize(main_prop)
    link_set = [w.lemma for w in sentence if (w.postag == "IN" or w.postag == "RB") and w.word == str_main_prop[-1]]
    if link_set:
        feature_set['logical_link'] = link_set[0]
    else:
        feature_set['logical_link'] = ""

    # TODO replace then by schema_type of conjunction (causal, concession, etc)

    # TODO add feature with case of the Y, COI or COD

    return feature_set


import unittest


class test_dce_classifier_features(unittest.TestCase):

    def test_features(self):
        schemas = parse_xml()
        self.show_features(schemas[0])
        self.show_features(schemas[1])
        self.show_features(schemas[42])
        self.show_features(schemas[43])

    def show_features(self, schema):
        print(schema.sentence)
        feature_set = features(schema)
        for feature_name in feature_set:
            print(feature_name + " -> " + feature_set[feature_name])


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
        add_labels(schemes) # Only done on the 160 first ones
        feature_sets = [(features(schema), schema.get_type()) for schema in schemes[0:270]]
        random.shuffle(feature_sets)

        # [print(feature) for feature in feature_sets] # TODO DELETE LATER

        # Creating the train and test sets and training the classifier: 273 * 0.632 = 172
        self.train_set, self.dev_set, self.test_set = feature_sets[0:170], feature_sets[171:210], feature_sets[221:270]
        # self.train_set, self.dev_set, self.test_set = feature_sets[0:63], feature_sets[63:75], feature_sets[75:100]
        print("Feature sets created - Start of the training")
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

    def get_confusing_matrix(self):
        ref = [schema.get_typet() for schema in parse_xml()]
        test = [self.answer(schema) for schema in parse_xml()]
        cm = nltk.ConfusionMatrix(ref, test)
        print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))
