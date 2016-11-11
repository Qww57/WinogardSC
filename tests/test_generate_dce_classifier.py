""" Script used to generate, test and select classifiers. """

from winosolver.dce.dce_classifier import DirectCausalEventClassifier
import time
import unittest


class TestDirectCausalEventClassifier(unittest.TestCase):

    def test_naive_bayes(self):

        debut = time.time()
        c = DirectCausalEventClassifier("naive_bayes")
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
        c.information(10)

        print(" ")
        print("Classify schema from test set")
        for schema in c.get_test_schemes():
            guess = c.answer(schema)
            print("Actual: " + schema.get_type() + " - Predicted: " + guess)
