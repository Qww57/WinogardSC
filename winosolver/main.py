""" Main class proposing a console interface for the resolution of winograd schema"""

import os
import warnings
from winosolver.schema.XMLParser import parse_xml
from winosolver.schema.Schema import Schema
from winosolver.dce.dce_bagging import DCEClassifierBagging
from winosolver.dce.dce_solver import DirectCausalEventSolver, features

warnings.filterwarnings("ignore")


def dce(current, opposite):
    """
    Function used to resolve a couple of schemas

    :param current:
    :param opposite:
    :return:
    """
    dce_classifier = DCEClassifierBagging()
    dce_solver = DirectCausalEventSolver()

    # Process of resolving one schema
    current.print()
    opposite.print()

    print("---- CLASSIFYING THE SCHEMA ----")
    print(current.sentence)
    guess = dce_classifier.classify(current)
    current.set_type(guess)
    print("-> Classified as " + guess)
    print(opposite.sentence)
    guess = dce_classifier.classify(opposite)
    opposite.set_type(guess)
    print("-> Classified as " + guess)
    print(" ")

    print("---- ANSWERING THE SCHEMA ----")
    print(current.sentence)
    answer = dce_solver.solve(current)
    print("-> Answer: " + str(answer))
    print(opposite.sentence)
    answer = dce_solver.solve(opposite)
    print("-> Answer: " + str(answer))
    print(" ")


def main():
    os.system("cls")

    # Getting the user's input
    pre_loaded = input("Run preloaded examples? (y/n)")
    print(" ")

    if pre_loaded is 'y' or pre_loaded is 'Y':

        # First example
        sentence = "Metz football team won against the one from Paris because it was better."
        snippet = "it was better"
        pronoun = "it"
        answer_a = "Metz football team"
        answer_b = "the one from Paris"
        sentence_bis = "Metz football team won against the one from Paris because it was bad."
        snippet_bis = "it was bad"

        current = Schema(ID=1, sentence=sentence, snip=snippet, pron=pronoun, prop1=answer_a,
                         prop2=answer_b, answer="to be guessed", source="console")

        opposite = Schema(ID=1, sentence=sentence_bis, snip=snippet_bis, pron=pronoun, prop1=answer_a,
                          prop2=answer_b, answer="to be guessed", source="console")

        print("Resolution of the first example: ")
        dce(current, opposite)

        # Schema: Pete envies Martin because/although he is very successful.
        schemas = parse_xml()
        current = schemas[38]
        opposite = schemas[39]

        print("Resolution of the second example: ")
        dce(current, opposite)

    else:
        print("---- Enter schema to solve ----")
        sentence = input("Enter the full sentence of the schema:")
        snippet = input("Enter the snippet:")
        pronoun = input("Enter the ambiguous pronoun:")
        answer_a = input("Enter answer A:")
        answer_b = input("Enter answer B:")

        current = Schema(ID=1, sentence=sentence, snip=snippet, pron=pronoun, prop1=answer_a,
            prop2=answer_b, answer="to be guessed", source="console")

        dce_classifier = DCEClassifierBagging()
        dce_solver = DirectCausalEventSolver()

        print("---- CLASSIFYING THE SCHEMA ----")
        print(current.sentence)
        guess = dce_classifier.classify(current)
        current.set_type(guess)
        print("-> Classified as " + guess)
        print(" ")

        print("---- ANSWERING THE SCHEMA ----")
        print(current.sentence)
        answer = dce_solver.solve(current)
        print("-> Answer: " + str(answer))
        print(" ")

    print("---- END ----")
    os.system("pause")

main()

