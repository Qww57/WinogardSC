import warnings

from CommonKnowledgeDataBase.WikipediaDatabase import WikipediaDatabase
from ToolsForNLP import Tokenizer
from Sources import XMLParser

warnings.filterwarnings("ignore")

def main():
    # Read the schema set from XML
    schema_set = XMLParser.parse_xml()

    # Process of resolving one schema
    current = schema_set[69]

    # Getting the related information
    words = Tokenizer.meaningful_words(current.sentence)
    print(words)
    database = WikipediaDatabase('main')
    words = [token for token in words if token.islower()]
    print(words)
    articles = database.add_many_articles(words)
    database.print_all_articles()

    # Grammatical analysis


    articles


main()