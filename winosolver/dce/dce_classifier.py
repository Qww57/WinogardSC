""" Implementation of supervised learning classifier to detect dce schema"""

import random
import time
from winosolver import Serializer
from winosolver.nlptools.Chunker import *
from winosolver.dce.features_tools import get_main_prop, get_link
from winosolver.nlptools.GrammaticalClassification import analyze
from winosolver.schema.XMLParser import *

chunker = Chunker()


def features(schema):
    feature_set = {}
    try:
        snippet = analyze(schema.snippet)
        main_prop = get_main_prop(schema)
        sentence = analyze(main_prop)

        # Creating a tree structure for the sentence
        full_structure = chunker.parse(schema.sentence)
        main_structure = get_main_pos(full_structure)

        # Main structure of the sentence after chucking: should reflect:
        # X (NP) action (VB) Y (NP) complements (?) link (IN) Z (NP) action (VB) complements (?)
        # TODO as boolean: matches structure or not.
        feature_set['sentence'] = str([tag for (tag, words) in main_structure])

        # Full structure of the snippet
        feature_set['snippet'] = str(snippet.get_tag_sequence())

        # TODO categorize schema_type of verb like action or state
        verb_set = [word.lemma for word in snippet if "V" in word.postag]
        if verb_set:
            feature_set['snippet_verb'] = verb_set[0]
        else:
            feature_set['snippet_verb'] = ""

        # Criteria 2
        feature_set['logical_link'] = get_link(schema)

        # TODO replace then by schema_type of conjunction (causal, concession, etc)
        # TODO add feature with case of the Y, COI or COD
    except Exception as e:
        print("Error: " + str(e) + "for following schema ")
        print(schema)
        feature_set['logical_link'] = ''
        feature_set['snippet_verb'] = ''
        feature_set['sentence'] = ''
        feature_set['snippet'] = ''
    return feature_set


class DirectCausalEventClassifier:

    """
    Classifier used in order to classify scheme as Direct Causal Event or not
    """

    classifiers = {
        'naive_bayes' : nltk.NaiveBayesClassifier,
        'decision_tree' : nltk.DecisionTreeClassifier
    }

    def __init__(self, classifier_type, set_length=None):
        """
        Default value of set_length is -1.
        :param classifier_type: schema_type of classifier chosen
        :param set_length: number of schemas used in order to train and test the classifier
        """
        self.accuracy = 0
        self.cm = "not defined"
        self.classifier_type = classifier_type

        debut = time.time()

        # Creation of the feature set
        schemes = parse_xml()
        add_labels(schemes)

        # Creating the train, dev and test sets
        length = len(schemes) if set_length is None else set_length
        train_length = int(length * 0.5)

        # DCE frequency in corpus is around 0.186
        dce_percentage = 0
        while dce_percentage < 0.156 or dce_percentage > 0.216:
            random.shuffle(schemes)
            self.train_schemes = schemes[0:train_length]
            self.test_schemes = schemes[(train_length + 1):length]
            count = 0
            for schema in self.train_schemes:
                count = count + 1 if schema.get_type() is "DCE" else count
            dce_percentage = count / train_length

        print("Train set with " + str(dce_percentage * train_length) + " DCE schema. (" + str(dce_percentage) + ")")

        self.train_set = [(features(schema), schema.get_type()) for schema in self.train_schemes]
        self.test_set = [(features(schema), schema.get_type()) for schema in self.test_schemes]
        print("Feature set created in " + str(int((time.time() - debut) / 60) + 1) + " minute(s).")
        debut = time.time()

        # Training the classifier
        self.classifier = self.classifiers[classifier_type].train(self.train_set)
        print("Classifier trained in " + str(int((time.time() - debut) / 60) + 1) + " minute(s).")
        debut = time.time()

        # Testing the classifier accuracy
        self.accuracy = nltk.classify.accuracy(self.classifier, self.test_set)
        print("Accuracy of answers: {} %".format(self.accuracy * 100))
        print("Accuracy computed in " + str(int((time.time() - debut) / 60) + 1) + " minute(s).")
        debut = time.time()

        # Creating the confusion matrix
        self.create_confusion_matrix()
        print("Confusion matrix created in " + str(int((time.time() - debut) / 60) + 1) + " minute(s).")

    def get_classifier(self):
        return self.classifier

    def get_test_schemes(self):
        return self.test_schemes

    def get_dev_schemes(self):
        return self.dev_schemes

    def get_classifier_type(self):
        return self.classifier_type

    def answer(self, schema):
        return self.classifier.classify(features(schema))

    # Get classifier's accuracy properties

    def get_accuracy(self):
        return self.accuracy * 100

    def information(self, nb):
        if self.get_classifier_type() is 'naive_bayes':
            return self.classifier.show_most_informative_features(nb)
        if self.get_classifier_type() is 'decision_tree':
            return self.classifier.pseudocode(depth=nb)

    def create_confusion_matrix(self):
        ref = [schema.get_type() for schema in parse_xml()]
        test = [self.answer(schema) for schema in parse_xml()]
        self.cm = nltk.ConfusionMatrix(ref, test)
        print(self.cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))

    def get_confusion_matrix(self):
        return self.cm

    # Saving the classifier

    def save_classifier(self, name):
        Serializer.save(self, name)
