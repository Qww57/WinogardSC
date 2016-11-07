""" Main class proposing a console interface for the resolution of winograd schema"""

import os
import warnings
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
        """
        sentence = "Metz football team won against the one from Paris because it was better."
        snippet = "it was better"
        pronoun = "it"
        answer_a = "Metz football team"
        answer_b = "the one from Paris"
        sentence_bis = "Metz football team won against the one from Paris because it was bad."
        snippet_bis = "it was bad"

        sentence = "The forward player scored to the goalkeeper because he was good."
        snippet = "he was good"
        pronoun = "he"
        answer_a = "The forward player"
        answer_b = "The goalkeeper"
        sentence_bis = "The forward player scored to the goalkeeper because he was bad."
        snippet_bis = "he was bad"
        """
        sentence = "The forward player missed against the goalkeeper because he was good."
        snippet = "he was good"
        pronoun = "he"
        answer_a = "The forward player"
        answer_b = "The goalkeeper"
        sentence_bis = "The forward player missed against the goalkeeper because he was bad."
        snippet_bis = "he was bad"
        """
        sentence = "The forward player scored to the goalkeeper although he was good."
        snippet = "he was good"
        pronoun = "he"
        answer_a = "The forward player"
        answer_b = "The goalkeeper"
        sentence_bis = "The forward player scored to the goalkeeper although he was bad."
        snippet_bis = "he was bad"

        sentence = "The forward player missed against the goalkeeper although he was good."
        snippet = "he was good"
        pronoun = "he"
        answer_a = "The forward player"
        answer_b = "The goalkeeper"
        sentence_bis = "The forward player missed against the goalkeeper although he was bad."
        snippet_bis = "he was bad"
        """
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
    """
    print("---- CLASSIFYING THE SCHEMA ----")
    guess = dce_classifier.classify(current)
    current.set_type(guess)
    opposite.set_type(guess)
    print("Sentence has been classified as " + guess)
    print(" ")
    """
    current.set_type("DCE")
    opposite.set_type("DCE")

    print("---- ANSWERING THE FIRST SCHEMA ----")
    print(current.sentence)
    answer = dce_solver.solve(current)
    print("Answer: " + str(answer))
    print("")

    opposite.print()

    print(" ")
    print("---- ANSWERING THE SECOND SCHEMA ----")
    print(opposite.sentence)
    answer = dce_solver.solve(opposite)
    print("Answer: " + str(answer))

    # os.system("pause")

main()

