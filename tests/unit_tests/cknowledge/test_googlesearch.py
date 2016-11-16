from winosolver.cknowledge.GoogleSearch import GoogleSearch
import unittest


class TestGoogleSearch(unittest.TestCase):

    def test_research(self):
        gs = GoogleSearch()
        request = 'lecture'
        print("Performing Google search for word: " + request)
        gse_pages = gs.google_search(request)
        search_sentences = gs.generate_sentences(gse_pages)

        print(len(search_sentences))
