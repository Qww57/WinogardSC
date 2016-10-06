from apiclient.discovery import build
from bs4 import BeautifulSoup
import api_keys
import os
import nltk.data
import urllib.request


class GoogleSearch:

    def __init__(self):
        # Developer API key
        self.api_key = api_keys.google_custom_search_key

        # ID of the search engine
        self.cse_id = api_keys.google_custom_search_id

        # Web pages results from Google Search Engine
        self.gse_results = []

        # Terms that should be in the sentences
        self.search_terms = []

        # Request should look like: request="mouse * cat"
        self.request = ""

    def google_search(self, request, **kwargs):
        self.request = request
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=self.request,
                                 cx=self.cse_id,
                                 **kwargs).execute()
        if res is None:
            self.gse_results = []
        else:
            # pprint.pprint(res)
            self.gse_results = res['items']
        return self.gse_results

    def concatenate(self, search_terms):
        """
        Maybe not needed
        :param search_terms:
        :return:
        """
        if len(search_terms) is 1:
            self.request = search_terms[0]
        else:
            concat = ""
            for i in search_terms:
                concat = concat + " " + i #+ '.* ' + i
            # concat = concat + ' .* '
            self.request = concat
        return self.request

    """
    def display_pages(self, search_term):
        if self.gse_results is []:
            self.gse_results = self.google_search(search_term)
        for result in self.gse_results:
            pprint.pprint(result)
    """

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def tokenize_gse_result(self, gse_result):
        # FIXME
        url = gse_result[u'link']
        print(url)
        try:
            # Converting the HTML to bytes
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
            sentences = self.tokenizer.tokenize_gse_result(raw_text)

            # Tokenizing the text into sentences based on layout
            set = []
            for sentence in sentences:
                lines = sentence.splitlines()
                for line in lines:
                    word_groups = line.split('\\s{2,}')
                    for group in word_groups:
                        set.append(group)
            return set
        except Exception as e:
            return []

    def generate_sentences(self, gse_results):
        return [self.tokenize_gse_result(result) for result in gse_results]
