from nltk import wordpunct_tokenize
from pymining import itemmining
from winosolver.schema.XMLParser import parse_xml, add_labels
from winosolver.nlptools.GrammaticalClassification import analyze


# TODO unit tests


def find_patterns(schema_type):
    """
    Function not called in the code. Used to think about how to solve the problem by finding patterns on
    DCE elements.
    :return:
    """
    # Creating the schema input list
    schema_set = parse_xml()
    add_labels(schema_set)
    print(str(len(schema_set)) + " schema founds")

    # getting the structure
    sentences = []
    snippets = []
    for schema in schema_set:
        if schema.get_type() is schema_type:
            sentences.append(analyze(schema.sentence).get_tag_sequence())
            snippets.append(analyze(schema.snippet).get_tag_sequence())
    print(str(len(snippets)) + " snippets to analyze founds")

    # Analyze of the collected snippets
    relim_input = itemmining.get_relim_input(tuple(snippets))
    support = int(len(snippets) / 4) + 1
    report = itemmining.relim(relim_input, min_support=support)
    results = [rep for rep in report if len(rep) > 2]
    print(str(len(results)) + " frequent structure sets with min support of " + str(support))

    return results


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


# TODO rewrite as unit tests

"""
patterns = find_patterns()
for pattern in patterns:
    print(pattern)

schemas = parse_xml()
print(get_main_prop(schemas[0]))
print(get_main_prop(schemas[1]))
print(get_main_prop(schemas[2]))

print(get_link(schemas[0]))
print(get_link(schemas[1]))
print(get_link(schemas[2]))
"""