import os
import warnings
from winosolver.Serializer import load
from winosolver.schema.Schema import Schema
from winosolver.dce.dce_classifier import DirectCausalEventClassifier

warnings.filterwarnings("ignore")


def main():
    os.system("cls")

    # Getting the user's input
    print("---- Enter schema to solve ----")
    # sentence = input("Enter the full sentence of the schema:")
    sentence = "Metz football team defeated the one from Paris because it was better."
    print("Sentence: " + sentence)
    # snippet = input ("Enter the snippet:")
    snippet = "it was better"
    print("Snippet: " + snippet)
    #pronoun = input("Enter the ambiguous pronoun:")
    pronoun = "it"
    print("Pronoun : " + pronoun)
    # answer_a = input("Enter answer A:")
    answer_a = "Metz football team"
    print("Answer A: " + answer_a)
    # answer_b = input("Enter answer B:")
    answer_b = "the one from Paris"
    print("Answer B: " + answer_b)

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
    dce_classifier = load("..\\tests\\naive_bayes_84_10-06-16")
    isinstance(dce_classifier, DirectCausalEventClassifier)
    print(dce_classifier.get_accuracy())
    dce_classifier.create_confusion_matrix()
    print(dce_classifier.get_confusion_matrix())

    print(" ")
    print("---- SOLVING THE SCHEMA ----")
    print("TODO")
    print(" ")

    os.system("pause")

main()

