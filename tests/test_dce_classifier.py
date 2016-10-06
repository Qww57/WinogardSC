from winosolver.dce.dce_classifier import DirectCausalEventClassifier
from winosolver.schema.XMLParser import parse_xml
import time
import unittest


class TestDirectCausalEventClassifier(unittest.TestCase):

    def test_naive_bayes(self):

        debut = time.time()
        c = DirectCausalEventClassifier("naive_bayes", 5)
        print(str(int((time.time() - debut) / 60) + 1) + " minutes to generate the naive bayes.")

        # If interesting results, saving it
        if c.get_accuracy() > 75:
            name = c.get_classifier_type() + "_" + str(int(c.get_accuracy())) + "_" \
                   + time.strftime("%x").replace("/", "-")
            c.save_classifier(name)

        print("DCE? - " + c.answer(parse_xml()[0]))
        print("DCE? - " + c.answer(parse_xml()[45]))
        print("DCE? - " + c.answer(parse_xml()[88]))
        print("DCE? - " + c.answer(parse_xml()[134]))

        print("Not DCE? - " + c.answer(parse_xml()[3]))
        print("Not DCE? - " + c.answer(parse_xml()[57]))
        print("Not DCE? - " + c.answer(parse_xml()[95]))
        print("Not DCE? - " + c.answer(parse_xml()[159]))

        for error in c.get_errors():
            print(error)

        c.create_confusion_matrix()
        c.get_confusion_matrix()

        c.information(4)
