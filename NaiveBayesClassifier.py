import nltk
import random
from XMLParser import parse_xml


class AnswerNaiveBayesClassifier:

    def __init__(self):
        self.accuracy = 0

        # Creation of the feature set
        schemes = parse_xml()
        feature_sets = [(self.features(schema), schema.correct) for schema in schemes]
        random.shuffle(feature_sets)

        for feature in feature_sets:
            print(feature)

        # Creating the train and test sets and training the classifier
        size = int(len(feature_sets) * 0.5)
        self.train_set, self.test_set = feature_sets[size:], feature_sets[:size]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        self.accuracy = nltk.classify.accuracy(self.classifier, self.test_set)
        print("Accuracy of answers: {} %".format(self.accuracy * 100))

    def get_accuracy(self):
        return self.accuracy * 100

    def features(self, schema):
        features = {}

        # TODO find real good features that can be used depending of type of schema
        features['Answer_A'] = schema.answer_A
        features['Answer_B'] = schema.answer_B

        return features

    def answer(self, schema):
        return self.classifier.classify(self.features(schema))

    def guess_answer(self):
        """
        Without telling him the possible answers the network still always find one of the possibilities as an answer
        """
        bullshit = 0;
        for schema in parse_xml():
            answer = self.answer(schema)
            if answer not in schema._answer_A and answer not in schema._answer_B:
                if schema._answer_B not in answer and schema._answer_A not in answer:
                    bullshit += 1
                    print("----- Wrong predicted answer: " + answer)
                    schema.print()
            # print("----- Predicted answer: " + answer)
            # schema.print()
        print("{} wrong possible answers over {} questions".format(bullshit, len(parse_xml())))


classifier = AnswerNaiveBayesClassifier()
classifier.answer(parse_xml()[125])

