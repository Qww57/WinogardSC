import os
import warnings
from winosolver.schema.Schema import Schema

warnings.filterwarnings("ignore")


def main():
    os.system("cls")

    # Getting the user's input
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

    current.print()

    # Process of resolving one schema
    print("---- CLASSIFYING THE SCHEMA ----")
    print("TODO")
    print(" ")

    print("---- SOLVING THE SCHEMA ----")
    print("TODO")
    print(" ")

    os.system("pause")


    """
    database = WikipediaDatabase('commonknowledge\\WordListDB')
    words = [token for token in words if token.islower()]
    print(words)
    print(len(database.get_all_articles()))
    """

main()

