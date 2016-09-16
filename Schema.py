class Schema:

    def __init__(self, ID, sentence, snip, pron, prop1, prop2, answer, source):

        """
        Basic constructor of a Winograd Schema

        :param sentence: sentence containing an ambiguity
        :param snip: snippet focusing on the ambiguity
        :param pron: ambiguous word whom we should guess the reference
        :param prop1: first possible reference of the word
        :param prop2: second possible reference of the word
        :param answer: correct answer among the two proposition
        """
        self._ID = ID
        self._sentence = sentence
        self._snippet = snip
        self._pronoun = pron
        self._answer_A = prop1
        self._answer_B = prop2
        if 'A' in answer:
            self._correct = prop1
        else:
            self._correct = prop2
        self._source = source
        self._type = "default"

    def set_type(self, type):
        self._type = type

    def get_type(self):
        return self._type

    def print(self):
        print("----- Winograd Schema number " + str(self._ID) + " -----")
        print("Text: {}".format(self._sentence))
        print("Snippet: {}".format(self._snippet))
        print("Choices for '" + self._pronoun + "': A) " + self._answer_A + ",  or B) " + self._answer_B)
        print("Answer: " + self._correct)
        print("Source: " + self._source)
        print("")