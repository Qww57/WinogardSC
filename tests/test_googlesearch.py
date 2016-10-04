from winosolver.commonknowledge import GoogleSearch
import unittest

class TestGoogleSearch(unittest.TestCase):

    def test_research(self):
        gs = GoogleSearch()
        request = '\"police * demonstrator\"'
        search_terms = ['police', 'demonstrator']
        gse_pages = gs.google_search(request, search_terms)
        knowledge_sentences = gs.tokenize(gse_pages)

        print(len(knowledge_sentences))

        for sentence in knowledge_sentences:
            print("Sentence: " + sentence)
