from urllib.request import urlopen
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
import json
import warnings
import unittest

warnings.filterwarnings("ignore")

dictionary = PyDictionary()


class DirectCausalEventSolver:

    @staticmethod
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

        print(word + ": " + str(result))
        return result

    @staticmethod
    def similarity(word1, word2):
        """
        Use concept net in order to find the similarity between two words.
        The order of the two input should have a real limited impact (less than 0.01).

        Request are made using the urllib on ConceptNet website.

        :param word1: first word
        :param word2: second word
        :return: similarity coefficient as float between 0 and 1.
        """

        link = "http://conceptnet5.media.mit.edu/data/5.4/assoc/c/en/" + word1 + "?filter=/c/en/" + word2 + "/.&limit=1"
        response = urlopen(link).read().decode('utf8')
        obj = json.loads(response)
        try:
            return obj["similar"][0][1]
        except IndexError:
            return 0
