from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
import pprint
import os
import nltk.data
import urllib.request


class GoogleSearch:

    # Developer API key
    api_key = "AIzaSyBrOcNKaPDyLouNwtP_Z-VUymYAlde6VI8"

    # ID of the search engine
    cse_id = "016483961005489098817:-9elerlp7mu"

    # Web pages results from Google Search Engine
    gse_results = []

    # Terms that should be in the sentences
    search_terms = []

    # Request should look like: request="mouse * cat"
    request = ""

    """ maybe not needed """
    def concatenate(self, search_terms):
        if len(search_terms) is 1:
            self.request = search_terms[0]
        else:
            concat = ""
            for i in search_terms:
                concat = concat + " " + i #+ '.* ' + i
            # concat = concat + ' .* '
            self.request = concat
        return self.request

    def google_search(self, request, search_terms, **kwargs):
        self.search_terms = search_terms
        self.request = request # TODO maybe generate a list of request with OR in between
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=self.request, cx=self.cse_id, **kwargs).execute()
        if res is None:
            self.gse_results = []
        else:
            self.gse_results = res['items']
        return self.gse_results

    def display_pages(self, search_term):
        if self.gse_results is []:
            self.gse_results = self.google_search(search_term)
        for result in self.gse_results:
            pprint.pprint(result)



    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def tokenize(self, gse_result):

        # Converting the HTML text to String
        url = gse_result[u'link']
        print(url)
        f = urllib.request.urlopen(url)
        mybytes = f.read()  # read bytes from url
        f.close()
        mystr = mybytes.decode("utf8")  # decodes bytes to string

        # Deleting all the HTML characters
        soup = BeautifulSoup(mystr, "html.parser")
        raw_text = soup.get_text()

        # Deleting empty lines
        raw_text = os.linesep.join([s for s in raw_text.splitlines() if s])

        # Tokenizing the text into sentences based on punctuation
        sentences = self.tokenizer.tokenize(raw_text)

        # Tokenizing the text into sentences based on layout
        set = []
        for sentence in sentences:
            lines = sentence.splitlines()
            for line in lines:
                word_groups = line.split('\\s{2,}')
                for group in word_groups:
                    set.append(group)
        return set

    def generate_sentences(self, gse_results):
        results = []

         # For each page in the results
        for result in gse_results:
            set = self.tokenize(result)

            # Filtering the sentences by selecting the ones containing the search items
            filtered = []
            for sentence in set:
                if should_add(self.search_terms, sentence):
                    results.append(sentence)

            # Adding the sentences to the results.
            results.extend(filtered)

        return results

    # def filter():
        # TODO filter sentences which are interesting
        # Should have at least 3 words
        # Then should have at least a verb


def should_add(search_terms, sentence):
    attach = True;
    for term in search_terms:
        if term not in wordpunct_tokenize(sentence):
            attach = False;
    return attach

"""
print(should_add(["cat"], "cat is huge man") is True)
print(should_add(["elephant"], "cat is huge man") is False)
print(should_add(["cat", "man"], "cat is huge man") is True)
print(should_add(["cat", "rat"], "cat is huge man") is False)


gs = GoogleSearch()
request = '\"police * demonstrator\"'
search_terms = ['police', 'demonstrator']
gse_pages = gs.google_search(request, search_terms)
knowledge_sentences = gs.tokenize(gse_pages)

print(len(knowledge_sentences))

for sentence in knowledge_sentences:
    print("Sentence: " + sentence)
"""

