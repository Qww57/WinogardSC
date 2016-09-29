from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
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

    # Request set
    search_terms = []

    # request=".*inquired.*but.*forgotten.*"

    request = ""

    def concatenate(self, search_terms):
        concat = ""
        for i in search_terms:
            concat = concat + '.*' + i
        concat = concat + '.*'
        self.request = concat
        return self.request

    def google_search(self, search_terms, **kwargs):
        self.search_terms = search_terms
        self.request = self.concatenate(search_terms)
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=request, cx=self.cse_id, **kwargs).execute()
        self.gse_results = res['items']
        return self.gse_results

    def display_pages(self, search_term):
        if self.gse_results is []:
            self.gse_results = self.google_search(search_term)
        for result in self.gse_results:
            pprint.pprint(result)


request = "raccoon"
gs = GoogleSearch()
search_terms = ['asked', 'but', 'forgot']
print(gs.concatenate(search_terms))
results = gs.google_search(request, num=3)


def tokenize(gse_results):

    results = []

    for result in gse_results:
        # Convert the HTML to string
        url = result[u'link']
        print(url)
        f = urllib.request.urlopen(url)
        mybytes = f.read() # read bytes from url
        f.close()
        mystr = mybytes.decode("utf8") # decodes bytes to string

        # Deleting all the html characters
        soup = BeautifulSoup(mystr, "html.parser")
        raw_text = soup.get_text()

        # Deleting useless empty lines
        raw_text = os.linesep.join([s for s in raw_text.splitlines() if s])

        # Tokenizing the text into sentences and filtering it
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') # Could be defined when instanciating the class
        sentences = tokenizer.tokenize(raw_text)

        set = []
        for sentence in sentences:
            lines = sentence.splitlines()
            for line in lines:
                word_groups = line.split('\\s{2,}')
                for group in word_groups:
                    set.append(group)

        filtered = []
        # DO for all search items
        for sentence in set:
            if request in sentence:
                filtered.append(sentence)

        results.extend(filtered)

    return results

print(len(tokenize(results)))

# def filter():
    # TODO filter sentences which are interesting
    # Have at least a verb to express