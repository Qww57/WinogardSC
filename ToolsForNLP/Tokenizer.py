from nltk.tokenize import wordpunct_tokenize, RegexpTokenizer
import nltk
import unittest

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def tokenize(paragraph):
    """
    Convert a paragraph into a set of sentences
    :param paragraph:
    :return:
    """

    # Tokenizing the text into sentences based on punctuation
    sentences = RegexpTokenizer(r'\w+').tokenize(paragraph)

    # Tokenizing the text into sentences based on layout
    set = []
    for sentence in sentences:
        lines = sentence.splitlines()
        for line in lines:
            word_groups = line.split('\\s{2,}')
            for group in word_groups:
                set.append(group)

    return set


def meaningful_words(sentence):

    tokens = RegexpTokenizer(r'\w+').tokenize(sentence)

    # Load the corresponding list of stopwords: words without meaning
    stopwords = set(nltk.corpus.stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stopwords]

    return tokens


def interesting_sentences(paragraph, search_terms):
    results = []
    sentences = tokenize(paragraph)

    # Filtering the sentences by selecting the ones containing the search items
    filtered = []
    for sentence in sentences:
        if should_add(search_terms, sentence):
            results.append(sentence)

    # Adding the sentences to the results.
    results.extend(filtered)

    return results


def should_add(search_terms, sentence):
    attach = True

    for term in search_terms:
        if term not in wordpunct_tokenize(sentence):
            attach = False

    return attach


def detect_first_names(text):
    # TODO See with Standford NRE Tagger
    # See also with CoreNLP from their university
    tokens = tokenize(text)
    return [token for token in tokens if not token.islower() and not token.isupper()]


class TestTokenizer(unittest.TestCase):

    def test_detect_first_names(self):
        text = "Mary and Ann are standing hand in hand"
        names = detect_first_names(text)
        expected = ["Mary", "Ann"]
        self.assertTrue(expected == names)