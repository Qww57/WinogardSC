import os
import warnings
from winosolver.Serializer import load
from winosolver.schema.Schema import Schema
from winosolver.dce.dce_bagging import DCEClassifierBagging
from winosolver.dce.dce_solver import DirectCausalEventSolver, features

warnings.filterwarnings("ignore")


def main():
    os.system("cls")

    # Getting the user's input
    #pre_loaded = input("Run preloaded example? (y/n)")
    pre_loaded = 'y'
    if pre_loaded is 'y' or pre_loaded is 'Y':
        sentence = "Metz football team defeated the one from Paris because it was better."
        snippet = "it was better"
        pronoun = "it"
        answer_a = "Metz football team"
        answer_b = "the one from Paris"
        sentence_bis = "Metz football team defeated the one from Paris because it was bad."
        snippet_bis = "it was bad"
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

    opposite = Schema(
        ID=-1,
        sentence=sentence_bis,
        snip=snippet_bis,
        pron=pronoun,
        prop1=answer_a,
        prop2=answer_b,
        answer="to be guessed",
        source="console"
    )

    print()
    current.print()

    dce_classifier = DCEClassifierBagging()
    dce_solver = DirectCausalEventSolver()

    # Process of resolving one schema
    print("---- CLASSIFYING THE SCHEMA ----")
    guess = dce_classifier.classify(current)
    current.set_type(guess)
    print("Sentence has been classified as " + guess)
    print(" ")

    print("---- ANSWERING THE SCHEMA ----")
    # for feature_name in features(current):
    #    print(feature_name + " -> " + str(features(opposite)[feature_name]))
    answer = dce_solver.solve(current)
    print("Answer: " + str(answer))
    print("")

    opposite.print()

    # Process of resolving one schema
    print("---- CLASSIFYING THE SCHEMA ----")
    guess = dce_classifier.classify(opposite)
    opposite.set_type(guess)
    print("Sentence has been classified as " + guess)

    print(" ")
    print("---- ANSWERING THE SCHEMA ----")
    for feature_name in features(opposite):
        print(feature_name + " -> " + str(features(opposite)[feature_name]))
    answer = dce_solver.solve(opposite)
    print("Answer: " + str(answer))

    # os.system("pause")

main()

