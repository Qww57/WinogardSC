class Schema:

    def __init__(self, sentence, snip, pron, prop1, prop2, answer, source):

        """
        Basic constructor of a Winograd Schema

        :param sentence: sentence containing an ambiguity
        :param snip: snippet focusing on the ambiguity
        :param pron: ambiguous word whom we should guess the reference
        :param prop1: first possible reference of the word
        :param prop2: second possible reference of the word
        :param answer: correct answer among the two proposition
        """

        self._sentence = sentence
        self._snippet = snip
        self._pronoun = pron
        self._answer_A = prop1
        self._answer_B = prop2
        self._correct = answer
        self._source = source
        self._type = "default"

    def set_type(self, type):
        self._type = type

    def get_type(self):
        return self._type
