""" Script used in order to try to cluster the Winograd schemas"""

from nltk import ngrams
from winosolver.nlptools.Chunker import Chunker, pre_process_sentence, get_main_pos


example = 'this is a foo bar sentences and i want to ngramize it'


def structure_n_gram(sentence):
    chunker = Chunker()
    sentence = pre_process_sentence(sentence)
    sentence = chunker.parse(sentence)
    sentence = get_main_pos(sentence)

    print(sentence)
    structure = [word[0] for word in sentence]

    n_grams = ngrams(structure, 4)

    for grams in n_grams:
        print(grams)

structure_n_gram(example)