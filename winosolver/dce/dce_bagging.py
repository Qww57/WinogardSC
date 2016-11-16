""" Class used in order to applying bagging principles to the DCE classifiers. """

from winosolver.Serializer import load
from winosolver.schema.XMLParser import parse_xml, add_labels
from collections import Counter


# Paths are set to be called from main
dce_1 = load("..\\data\\naive_bayes_77_10-07-16")
dce_2 = load("..\\data\\naive_bayes_75_10-09-16")
dce_3 = load("..\\data\\naive_bayes_80_10-09-16")
dce_4 = load("..\\data\\naive_bayes_85_10-08-16")
dce_5 = load("..\\data\\naive_bayes_80_11-14-16")

classifiers = [dce_1, dce_2, dce_3, dce_4]


class DCEClassifierBagging:

    # Ratio of the correct predictions among all of them.
    accuracy = 0

    # Ratio of the correct predictions among the DCE predictions.
    sensitivity = 0

    # Ratio of the correct predictions among the non-DCE predictions.
    specificity = 0

    @staticmethod
    def print_classifiers_accuracy():
        """
        Print the accuracy of the all classifiers used for bagging

        :return: console printings
        """
        [print(classifier.get_accuracy()) for classifier in classifiers]

    @staticmethod
    def classify(schema):
        """
        Return the most chosen answer among the classifier. All of them are voting with equal weight.

        :param schema: schema to solve
        :return: chosen classification
        """
        answers = [classifier.answer(schema) for classifier in classifiers]
        return Counter(answers).most_common(2)[0][0]

    def compute_efficiency(self):
        """
        Compute the accuracy, sensitivity and specificity obtained by the bagging of all classifiers for all the
        Winograd schemas.

        :return: (accuracy, sensitivity, specificity)
        """
        true_positive, true_negative = 0, 0
        false_positive, false_negative = 0, 0

        schema_set = parse_xml()
        add_labels(schema_set)

        for schema in schema_set:
            guess = self.classify(schema)
            if guess == schema.get_type():
                if guess == "DCE":
                    true_positive += 1
                else:
                    true_negative += 1
            elif guess == "DCE":
                false_positive += 1
            else:
                false_negative += 1

        self.accuracy = (true_positive + true_negative) / len(schema_set)
        self.sensitivity = true_positive / (true_positive + false_negative)
        self.specificity = true_negative / (true_negative + false_positive)

        print("Accuracy: " + str(self.accuracy))
        print("Sensitivity: " + str(self.sensitivity))
        print("Specificity: " + str(self.specificity))

        return self.accuracy, self.sensitivity, self.specificity
