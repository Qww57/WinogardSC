from winosolver.Serializer import load
from winosolver.schema.XMLParser import parse_xml, add_labels
from collections import Counter


# Paths are set to be called from main
dce_1 = load("..\\data\\naive_bayes_77_10-07-16")
dce_2 = load("..\\data\\naive_bayes_75_10-09-16")
dce_3 = load("..\\data\\naive_bayes_80_10-09-16")
dce_4 = load("..\\data\\naive_bayes_85_10-08-16")
dce_5 = load("..\\data\\naive_bayes_74_10-09-16")


class DCEClassifierBagging:

    @staticmethod
    def print_classifiers_accuracy():
        print(dce_1.get_accuracy())
        print(dce_2.get_accuracy())
        print(dce_3.get_accuracy())
        print(dce_4.get_accuracy())
        print(dce_5.get_accuracy())

    @staticmethod
    def classify(schema):
        answers = list()
        answers.append(dce_1.answer(schema))
        answers.append(dce_2.answer(schema))
        answers.append(dce_3.answer(schema))
        answers.append(dce_4.answer(schema))
        answers.append(dce_5.answer(schema))
        return Counter(answers).most_common(2)[0][0]

    def compute_efficiency(self):
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        schema_set = parse_xml()
        add_labels(schema_set)

        for schema in schema_set:
            guess = self.classify(schema)
            if guess == schema.get_type():
                if guess == "DCE":
                    true_positive += 1
                else:
                    true_negative += 1
            else:
                if guess == "DCE":
                    false_positive += 1
                else:
                    false_negative += 1

        print("Accuracy: " + str((true_positive + true_negative) / len(schema_set)))
        print("Sensitivity: " + str(true_positive / (true_positive + false_negative)))
        print("Specificity: " + str(true_negative / (true_negative + false_positive)))
