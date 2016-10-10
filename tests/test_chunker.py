from winosolver.nlptools.Chunker import *
from winosolver.schema.XMLParser import parse_xml
import unittest


class TestChunker(unittest.TestCase):

    def test_example(self):
        # Running the chunker on a corpus
        chunker = Chunker()
        print()

        # Loading and chunking a sentence
        schemas = parse_xml()
        sentence = schemas[0].sentence
        sentence = pre_process_sentence(sentence)
        result = chunker.parse(sentence)
        print(str(get_main_pos(result)))
        full_structure = chunker.parse(sentence)
        # TODO MOVE TO FEATURES TEST
        main_structure = get_main_pos(full_structure)
        print([tag for (tag, words) in main_structure])

        sentence = schemas[0].sentence
        result = chunker.parse(sentence)
        print(str(get_main_pos(result)))

        sentence = schemas[158].sentence
        result = chunker.parse(sentence)
        print(str(get_main_pos(result)))
