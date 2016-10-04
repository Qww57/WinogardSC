import warnings

from winosolver.commonknowledge.WikipediaDatabase import WikipediaDatabase
from winosolver.nlptools import Tokenizer
from winosolver.schema import XMLParser

warnings.filterwarnings("ignore")

def main():
    # Read the schema set from XML
    schema_set = XMLParser.parse_xml()

    # Process of resolving one schema
    current = schema_set[69]

    # Getting the related information
    words = Tokenizer.meaningful_words(current.sentence)
    print(words)
    database = WikipediaDatabase('winosolver/commonknowledge/WordListDB')
    words = [token for token in words if token.islower()]
    print(words)
    print(len(database.get_all_articles()))

    # Grammatical analysis

main()

import os
os.system("pause")