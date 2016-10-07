from winosolver.dce.dce_classifier import DirectCausalEventClassifier
from winosolver.schema.XMLParser import parse_xml
import time
import unittest


class TestDirectCausalEventClassifier(unittest.TestCase):

    def test_naive_bayes(self):

        debut = time.time()
        c = DirectCausalEventClassifier("naive_bayes", 100)
        print(str(int((time.time() - debut) / 60) + 1) + " minutes to generate the naive bayes.")

        # If interesting results, classifier is saved
        if c.get_accuracy() > 60:
            name = c.get_classifier_type() + "_" + str(int(c.get_accuracy())) + "_" \
                   + time.strftime("%x").replace("/", "-")
            c.save_classifier(name)

        print(" ")
        print("Analysis of the confusion matrix")
        c.get_confusion_matrix()

        print(" ")
        print("Analysis of the most important features")
        c.information(4)

        print(" ")
        print("Classify schema from dev test")
        for schema in c.get_dev_schemes():
            guess = c.answer(schema)
            print("Actual: " + schema.get_type() + " - Predicted: " + guess)

        print(" ")
        print("Analysis of errors from dev set")
        for error in c.get_errors():
            print(error)

        print(" ")
        print("Classify schema from test set")
        for schema in c.get_test_schemes():
            guess = c.answer(schema)
            print("Actual: " + schema.get_type() + " - Predicted: " + guess)
