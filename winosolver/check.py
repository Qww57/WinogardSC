import warnings
import os
from winosolver.nlptools import Tokenizer, GrammaticalClassification
from winosolver.schema import XMLParser
from winosolver.dce.DirectCausalEventSolver import DirectCausalEventSolver

warnings.filterwarnings("ignore")

"""
Script to be run in the console to check that the installation has been done properly.
"""


def test():
    # Read the schema set from XML
    schema_set = XMLParser.parse_xml()
    schema_set[0].print()

    # Process of resolving one schema
    current = schema_set[69]

    # Getting the related information
    words = Tokenizer.meaningful_words(current.sentence)
    print(words)

    # Grammatical analysis
    print("")
    print(GrammaticalClassification.analyze(words))

    # DCE
    solver = DirectCausalEventSolver
    print("Antonym of " + words[1] + " " + str(solver.antonym(word=words[1])))
    print("Relation with 'answer': " + str(solver.similarity("answer", solver.antonym(word=words[1])[0])))

test()

os.system("pause")