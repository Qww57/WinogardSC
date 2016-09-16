import untangle
import os
from Schema import Schema


def parse_xml():

    schemes = []

    # Loading the XML file
    script_dir = os.path.dirname(__file__)
    rel_path = "sources/WSCollection.xml"
    path = os.path.join(script_dir, rel_path)
    id = 0

    # Reading the XML file
    for schema in untangle.parse(path).collection.schema:

        # Getting the text
        text1 = schema.text.txt1.cdata
        pron = schema.text.pron.cdata
        text2 = schema.text.txt2.cdata
        text = text1 + pron + text2

        # Getting the snippet
        try:
            quote1 = schema.quote.quote1.cdata
        except IndexError:
            quote1 = ""
        q_pron = schema.quote.pron.cdata
        try:
            quote2 = schema.quote.quote2.cdata
        except IndexError:
            quote2 = ""
        snippet = quote1 + q_pron + quote2

        # Getting the answers
        answers = []
        for answer in schema.answers.answer:
            answers.append(answer.cdata)
        answer_a = answers[0]
        answer_b = answers[1]
        correct = schema.correctAnswer.cdata

        source = schema.source.cdata

        new_schema = Schema(id, text, snippet, pron, answer_a, answer_b, correct, source)
        schemes.append(new_schema)
        id += 1

    return schemes


input = parse_xml()
print(len(input))
input[0].print()
