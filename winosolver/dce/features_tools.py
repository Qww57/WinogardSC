from nltk import wordpunct_tokenize
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
from urllib.request import urlopen
from winosolver.nlptools.Chunker import *
from winosolver.nlptools.GrammaticalClassification import analyze
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
    try:
        for i in wn.synsets(word):
            if i.pos() in ['a', 's']:
                for j in i.lemmas():
                    if j.antonyms():
                        result.append(j.antonyms()[0].name())

        result = list(set(result))
        if len(result) is 0 and dictionary.antonym(word):
            result.extend(dictionary.antonym(word))
        return result
    except Exception as e:
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


def get_trait(schema):
    snippet = schema.snippet
    tokens = analyze(snippet)

    for i in range(0, len(tokens), 1):
        if "VV" in tokens[i].postag:
            return tokens[i].lemma
        else:
            # Verb be
            if "VB" in tokens[i].postag or "VH" in tokens[i].postag:
                if tokens[i + 1].postag == "VVG":  # verb in be+ING
                    return tokens[i + 1].lemma
                if tokens[i + 1].postag == "RBR":  # if comparative
                    return tokens[i + 1].lemma
                if tokens[i + 1].postag == "RBS":  # if superlative
                    return tokens[i + 1].lemma
                for j in range(i, len(tokens), 1):
                    if tokens[j].postag in ["JJ", "JJS", "JJR"]:
                        return tokens[j].lemma
                    if tokens[j].postag == "NN":
                        return tokens[j].lemma


def get_action(schema):
    main_prop = get_main_prop(schema)
    return get_main_element(main_prop)


def get_main_element(sentence):
    # If verb is "be" then return the next JJ.
    # Tree tagger is better
    tokens = analyze(sentence)

    for i in range(0, len(tokens), 1):
        if "VV" in tokens[i].postag:
            return tokens[i].lemma
        else:
            # Verb be
            if "VB" in tokens[i].postag or "VH" in tokens[i].postag:
                if tokens[i + 1].postag == "VVG":  # verb in be+ING
                    return tokens[i + 1].lemma
                if tokens[i + 1].postag == "RBR":  # if comparative
                    return tokens[i + 1].lemma
                if tokens[i + 1].postag == "RBS":  # if superlative
                    return tokens[i + 1].lemma
                for j in range(i, len(tokens), 1):
                    if tokens[j].postag in ["JJ", "JJS", "JJR"]:
                        return tokens[j].lemma
                    if tokens[j].postag == "NN":
                        return tokens[j].lemma


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
    link_set = [w.lemma for w in sentence if w.postag in ["IN", "RB", "CC", "RBS", "RBR"] and
                w.word == str_main_prop[-1]]
    if link_set:
        return link_set[0]
    else:
        return ""


causal_set = ['because', 'since', 'an effect of', 'an outcome of', 'an upshot of', 'as a consequence of',
              'as a result of', 'because', 'caused by', 'hence', 'stemmed from', 'still']

opposition_set = ['but', 'although', 'despite', 'even though', 'however', 'nevertheless', 'otherwise', 'though',
                  'alternatively', 'by contrast', 'whereas']


def is_causal_relation(schema):
    return True if get_link(schema) in causal_set else False


def is_opposition_relation(schema):
    return True if get_link(schema) in opposition_set else False


both_verbs = ['be', 'have', 'see', 'taste', 'smell', 'feel', 'look', 'think']

# CAREFUL, SOME OF THEM CAN BE: MEASURE = BE LONG HERE, NOT MEASURING
state_verbs = ['agree', 'appear', 'believe', 'belong', 'concern', 'consider', 'consist', 'contain', 'depend', 'deserve',
               'disagree', 'dislike', 'doubt', 'feel', 'fit', 'forget', 'guess', 'hate', 'hear', 'imagine', 'impress',
               'include', 'involve', 'know', 'like', 'love', 'matter', 'mean', 'measure', 'mind', 'mind', 'need', 'owe',
               'own', 'prefer', 'promise', 'realise', 'recognise', 'remember', 'seem', 'sound', 'suppose', 'sound',
               'weigh', 'wish', 'fear', 'satisfy', 'cost', 'equal', 'require']


def get_snippet_verb(schema):
    snippet = analyze(schema.snippet)
    verb_set = [word.lemma for word in snippet if "V" in word.postag]
    if verb_set:
        return verb_set[0]
    else:
        return None


def is_action_verb(v):
    return False if v in state_verbs else True


def is_state_verb(v):
    return True if v in state_verbs or v in both_verbs else False


def snippet_verb(schema):
    verb = get_snippet_verb(schema)
    if is_action_verb(verb) and is_state_verb(verb):
        return "A-S"
    if is_action_verb(verb):
        return "A"
    if is_state_verb(verb):
        return "S"
    return ""


def is_dce_structure(schema):
    # Basic structure of schema
    structure = ["N", "V", "N", "IN", "N", "V"]

    # Pre-processing
    full_structure = Chunker().parse(schema.sentence)
    main_structure = get_main_pos(full_structure)
    tags = [tag for (tag, words) in main_structure]
    tags = ["V" if "V" in tag else tag for tag in tags]
    tags = ["N" if tag in ["NN", "NNS", "NP", "NPS"] else tag for tag in tags]

    # Checking if the basic structure is contained in the schema
    return is_sub_sequence(structure, tags)


def is_sub_sequence(sub_seq, seq):
    """ Recursive method used in order to define if a sub-sequence is contained inside a sequence."""
    if len(sub_seq) == 0:
        return True
    if sub_seq[0] in seq:
        index = seq.index(sub_seq[0])
        if index + 1 < len(seq) or len(sub_seq) > 1:
            return is_sub_sequence(sub_seq[1:], seq[index + 1:])
        else:
            return True
    else:
        return False

"""
from winosolver.schema.XMLParser import *
schemes = parse_xml()
print(is_dce_structure(schemes[0]))
"""
