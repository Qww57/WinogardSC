from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import nltk.data
import pprint
import urllib.request


class GoogleSearch:

    # Developer API key
    api_key = "AIzaSyBrOcNKaPDyLouNwtP_Z-VUymYAlde6VI8"

    # ID of the search engine
    cse_id = "016483961005489098817:-9elerlp7mu"

    # Web pages results from Google Search Engine
    gse_results = []

    # Request set
    request_set = []

    # request=".*inquired.*but.*forgotten.*"

    request="cat"

    def google_search(self, search_term, **kwargs):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=search_term, cx=self.cse_id, **kwargs).execute()
        self.gse_results = res['items']
        return self.gse_results

    '''
    def display_pages(self, search_term):
        if self.gse_results is []:
            self.gse_results = self.google_search(search_term)
        for result in self.gse_results:
            pprint.pprint(result)
    '''


request = "cat"
gs = GoogleSearch()
results = gs.google_search(request, num=1)

for result in results:
    # Get the url link of the result page
    url = result[u'link']
    title = result[u'title']
    print(url)

    # Convert the HTML to string
    f = urllib.request.urlopen(url)
    mybytes = f.read() # read bytes from url
    f.close()
    mystr = mybytes.decode("utf8") # decodes bytes to string

    # Deleting all the html characters
    soup = BeautifulSoup(mystr, "html.parser")
    raw_text = soup.get_text()

    # Tokenizing the text into sentences and filtering it
    # TODO tokenize with punkt but should do it also with spaces etc
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') # Could be defined when instanciating the class
    sentences = tokenizer.tokenize(raw_text)
    print(len(sentences))

    filtered = []
    for sentence in sentences:
        if request in sentence:
            filtered.append(sentence)

    print(len(filtered))
    # print(filtered[0])
    print(filtered[15])