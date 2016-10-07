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
        self.ID = ID
        self.sentence = sentence
        self.snippet = snip
        self.pronoun = pron
        self.answer_A = prop1
        self.answer_B = prop2
        if 'A' in answer:
            self.correct = prop1
        elif 'B' in answer:
            self.correct = prop2
        else:
            self.correct = "unknown"
        self.source = source
        self.schema_type = "unknown"

    def set_type(self, schema_type):
        self.schema_type = schema_type

    def get_type(self):
        return self.schema_type

    def validate(self):
        valid = (isinstance(self.ID, int) and isinstance(self.schema_type, str) and
                 isinstance(self.answer_A, str) and isinstance(self.answer_B, str) and
                 isinstance(self.sentence, str) and isinstance(self.snippet, str) and
                 isinstance(self.pronoun, str) and isinstance(self.correct, str) and

                 self.schema_type and self.answer_A and self.answer_B and self.snippet and
                 self.sentence and self.sentence and self.ID is not None)

        return valid

    def print(self):
        print("----- Winograd Schema number " + str(self.ID) + " -----")
        print("Text: {}".format(self.sentence))
        print("Snippet: {}".format(self.snippet))
        print("Pronoun: {}".format(self.pronoun))
        print("Choices for '" + self.pronoun + "': A) " + self.answer_A + ",  or B) " + self.answer_B)
        print("Answer: " + self.correct)
        print("Source: " + self.source)
        print("")

    def __str__(self):
        return self.ID + ':' + self.sentence + ' - ' + self.pronoun + ' - ' + self.answer_A + ' or ' + self.answer_B
