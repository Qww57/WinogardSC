from winosolver.dce.features_tools import *


def features(schema):
    feature_set = {}
    try:
        action = get_action(schema)
        trait = get_trait(schema)
        antonym_trait = antonym(trait)
        feature_set['causal_relation'] = is_causal_relation(schema)
        feature_set['opposition_relation'] = is_opposition_relation(schema)
        feature_set['action_trait_similarity'] = similarity(action, trait)
        feature_set['action_!trait_similarity'] = similarity(action, antonym_trait[0])
    except Exception as e:
        print(e.with_traceback())
        feature_set['logical_link'] = ''
        feature_set['snippet_verb'] = ''
        feature_set['sentence'] = ''
        feature_set['snippet'] = ''
    return feature_set


class DirectCausalEventSolver:

    def __init__(self):
        print("TODO")
