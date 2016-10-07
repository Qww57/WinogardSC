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

"""
patterns = find_patterns()
for pattern in patterns:
    print(pattern)
"""