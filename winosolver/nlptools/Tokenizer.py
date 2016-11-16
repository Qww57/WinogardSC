""" Script defining a few basic function related to tokenizing"""

from nltk.tokenize import wordpunct_tokenize, RegexpTokenizer
import nltk


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def tokenize_in_sentences(paragraph):
    """
    Convert a paragraph into a set of sentences
    :param paragraph:
    :return:
    """
    # Tokenizing the text into sentences based on punctuation
    sentences = tokenizer.tokenize(paragraph)

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
    return [token for token in tokens if token.lower() not in stopwords]


def interesting_sentences(paragraph, search_terms, type):
    return [sentence for sentence in tokenize_in_sentences(paragraph) if should_add(search_terms, sentence, type)]


def should_add(search_terms, sentence, type):
    if type is None or type is "Exclusive":
        attach = True
        for term in search_terms:
            if term.lower() not in [word.lower() for word in wordpunct_tokenize(sentence)]:
                attach = False
    else:
        attach = False
        for term in search_terms:
            if term.lower() in [word.lower() for word in wordpunct_tokenize(sentence)]:
                attach = True
    return attach


def detect_first_names(text):
    # TODO See with Standford NRE Tagger - See also with CoreNLP from their university
    # FIXME
    return [token for token in tokenize_in_sentences(text) if not token.islower() and not token.isupper()]
