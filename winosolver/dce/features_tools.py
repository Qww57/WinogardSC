from nltk import wordpunct_tokenize
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
from urllib.request import urlopen
from winosolver.nlptools.Chunker import *
import json


dictionary = PyDictionary()


def antonym(word):
    """
    Done like this because I find the result of wn more accurate for adjective
    but missing a lot of vocabulary especially for nouns.

    Works well with adjectives, a bit more tricky with nouns sometime.

    Limitation: verb in two words like "look out" that cannot be used.

    :param word: word that should be negated
    :return: antonym set
    """
    result = []
    for i in wn.synsets(word):
        if i.pos() in ['a', 's']:
            for j in i.lemmas():
                if j.antonyms():
                    result.append(j.antonyms()[0].name())

    result = list(set(result))
    if len(result) is 0 and dictionary.antonym(word):
        result.extend(dictionary.antonym(word))

    return result


def similarity(word1, word2):
    """
    Use concept net in order to find the similarity between two words.
    The order of the input doesn't not have any impact.

    Request are made using the urllib on ConceptNet website.

    :param word1: first word
    :param word2: second word
    :return: similarity coefficient as float between 0 and 1.
    """

    def sim(w1, w2):
        link = "http://conceptnet5.media.mit.edu/data/5.4/assoc/c/en/" + w1 + "?filter=/c/en/" + w2 + "/.&limit=1"
        response = urlopen(link).read().decode('utf8')
        obj = json.loads(response)
        try:
            return obj["similar"][0][1]
        except IndexError:
            return 0

    return float(sim(word1, word2) + sim(word2, word1)) / 2


# TODO unit tests

from winosolver.nlptools.GrammaticalClassification import analyze


def get_trait(schema):
    snippet = schema.snippet
    tokens = analyze(snippet)

    # If verb is "be" then return the next JJ.
    # Tree tagger is better
    for i in range(0, len(tokens), 1):
        if tokens[i].postag == "VVD":
            return tokens[i].lemma
        else:
            # Verb be
            if tokens[i].postag == "VBD":
                if tokens[i].postag == "VVG":  # verb in be+ING
                    return tokens[i].lemma
                for j in range(i, len(tokens), 1):
                    if tokens[j].postag == "JJ":
                        return tokens[j].lemma
                    if tokens[j].postag == "NN":
                        return tokens[j].lemma


def get_action(schema):
    main_prop = get_main_prop(schema)
    tokens = analyze(main_prop)

    # If verb is "be" then return the next JJ.
    # Tree tagger is better
    for i in range(0, len(tokens), 1):
        if tokens[i].postag == "VVD":
            return tokens[i].lemma
        else:
            # Verb be
            if tokens[i].postag == "VBD":
                if tokens[j].postag == "VVG":  # verb in be+ING
                    return tokens[j].lemma
                for j in range(i, len(tokens), 1):
                    if tokens[j].postag == "JJ":
                        return tokens[j].lemma
                    if tokens[j].postag == "NN":
                        return tokens[j].lemma

from winosolver.schema.XMLParser import *
"""
chunker = Chunker()
schema_set = parse_xml()
add_labels(schema_set)
for schema in schema_set[0:50]:
    if schema.get_type() is "DCE":
        print(get_trait(schema))
"""


def get_main_prop(schema):
    """
    Done by reverting and without deleting first in order to avoid having problems of deleting item
    of the list and then changing the index of the loop we are running.
    :param schema:
    :return:
    """

    # Tokenizing and reverting the token sequences
    sentence = wordpunct_tokenize(schema.sentence)
    snippet = wordpunct_tokenize(schema.snippet)
    sentence.reverse()
    snippet.reverse()

    # Replacing the tokens from the snippet in the sentence by empty spots
    for j in range(0, len(sentence) - len(snippet), 1):
        count = 0
        for i in range(0, len(snippet), 1):
            if sentence[j + i] == snippet[i]:
                count += 1
        if count == len(snippet):
            for i in range(0, len(snippet), 1):
                sentence[j + i] = ""

    # Reversing and removing empty spaces
    sentence.reverse()
    sentence = [word for word in sentence if word and not word == '.']

    # Returning a string
    sentence_str = ""
    for word in sentence:
        sentence_str += word + " ";

    return sentence_str


def get_link(schema):
    main_prop = get_main_prop(schema)
    str_main_prop = nltk.word_tokenize(main_prop)
    sentence = analyze(schema.sentence)
    link_set = [w.lemma for w in sentence if (w.postag == "IN" or w.postag == "RB") and w.word == str_main_prop[-1]]
    if link_set:
        return link_set[0]
    else:
        return ""


causal_set = ['because', 'since']
opposition_set = ['but', 'although']


def is_causal_relation(schema):
    return True if get_link(schema) in causal_set else False


def is_opposition_relation(schema):
    return True if get_link(schema) in opposition_set else False
