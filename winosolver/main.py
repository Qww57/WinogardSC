import os
import warnings
from winosolver.Serializer import load
from winosolver.schema.Schema import Schema
from winosolver.dce.dce_classifier import DirectCausalEventClassifier

warnings.filterwarnings("ignore")


def main():
    os.system("cls")

    # Getting the user's input
    pre_loaded = input("Run preloaded example? (y/n)")
    if pre_loaded is 'y' or pre_loaded is 'Y':
        sentence = "Metz football team defeated the one from Paris because it was better."
        snippet = "it was better"
        pronoun = "it"
        answer_a = "Metz football team"
        answer_b = "the one from Paris"
    else:
        print("---- Enter schema to solve ----")
        sentence = input("Enter the full sentence of the schema:")
        snippet = input("Enter the snippet:")
        pronoun = input("Enter the ambiguous pronoun:")
        answer_a = input("Enter answer A:")
        answer_b = input("Enter answer B:")

    current = Schema(
        ID=-1,
        sentence=sentence,
        snip=snippet,
        pron=pronoun,
        prop1=answer_a,
        prop2=answer_b,
        answer="to be guessed",
        source="console"
    )

    print()
    current.print()

    # Process of resolving one schema
    print("---- CLASSIFYING THE SCHEMA ----")
    dce_bayes_classifier = load("..\\data\\naive_bayes_77_10-07-16")
    isinstance(dce_bayes_classifier, DirectCausalEventClassifier)
    print(dce_bayes_classifier.get_accuracy())
    print(dce_bayes_classifier.information(10))  # FIXME with if None
    guess = dce_bayes_classifier.answer(current)
    current.set_type(guess)
    print("Sentence has been classified as " + guess)

    """
    dce_tree_classifier = load("..\\data\\decision_tree_77_10-07-16")
    isinstance(dce_tree_classifier, DirectCausalEventClassifier)
    print(dce_tree_classifier.get_accuracy())
    print(dce_tree_classifier.information(4))
    guess = dce_tree_classifier.answer(current)
    print("Sentence has been classified as " + guess)
    """

    print(" ")
    print("---- ANSWERING THE SCHEMA ----")
    print("...WILL COME SOON...")
    print(" ")

    os.system("pause")

main()

