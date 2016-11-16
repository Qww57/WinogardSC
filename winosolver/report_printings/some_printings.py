""" Some random code used for printings for the report"""
from winosolver.schema.XMLParser import *
from winosolver.dce.dce_solver import *
from winosolver.dce.dce_bagging import DCEClassifierBagging
from winosolver.Serializer import *
import warnings

warnings.filterwarnings("ignore")

schemes = parse_xml()
add_labels(schemes)
"""
schemas = [schema for schema in schemas if schema.get_type() == "DCE"]
correct = [1, 2, 6, 10, 11, 13, 14, 18, 19, 21, 32, 45, 46]
[print(schema.sentence) for schema in schemas if schemas.index(schema) in correct]

schemas = parse_xml()
add_labels(schemas)
schemas = [schema for schema in schemas if schema.get_type() == "DCE"]
# wrong = [0, 3, 7, 9, 12, 15, 17, 20, 22, 23, 24, 25, 33, 38, 39]
wrong = [12]
features = [print(str(s.sentence) + "\n" + str(features(s))) for s in schemas if schemas.index(s) in wrong]
"""
"""
classifier = DCEClassifierBagging()
classifier.print_classifiers_accuracy()
classifier.compute_efficiency()

"""
classifier = load("..\\data\\naive_bayes_80_11-14-16")
true_positive, true_negative, false_positive, false_negative = [], [], [], []
for schema in schemes:
    guess = classifier.answer(schema)
    if guess == schema.get_type():
        if guess == "DCE":
            true_positive.append(schemes.index(schema))
        else:
            true_negative.append(schemes.index(schema))
    elif guess == "DCE":
        false_positive.append(schemes.index(schema))
    else:
        false_negative.append(schemes.index(schema))
print("Correct: " + str(true_positive) + str(true_negative))
print("False positive: " + str(len(false_positive)) + str(false_positive))
print("False negative: " + str(len(false_negative)) + str(false_negative))
print("Accuracy: " + str((len(true_positive) + len(true_negative)) / len(schemes)))
print("Sensitivity: " + str(len(true_positive) / (len(true_positive) + len(false_negative))))
print("Specificity: " + str(len(true_negative) / (len(true_negative) + len(false_positive))))
