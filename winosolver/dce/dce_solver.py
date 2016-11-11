

from winosolver.dce.features_tools import *


def features(schema):

    feature_set = {}

    # Getting the type of relation
    feature_set['causal_relation'] = is_causal_relation(schema)
    feature_set['opposition_relation'] = is_opposition_relation(schema)

    # Getting the actions from both sentences
    action1 = get_action(schema)
    trait = get_trait(schema)
    antonym_trait = antonym(trait)

    try:
        feature_set['action_trait_similarity'] = similarity(action1, trait)
    except Exception as e:
        feature_set['action_trait_similarity'] = -1
    try:
        feature_set['action_!trait_similarity'] = similarity(action1, antonym_trait[0])
    except Exception as e:
        feature_set['action_!trait_similarity'] = -1

    # Features not used, but saved for result discussion
    feature_set['action'] = action1
    feature_set['trait'] = trait
    feature_set['antonym'] = antonym_trait
    feature_set['action_snippet'] = get_snippet_verb(schema)

    return feature_set


class DirectCausalEventSolver:

    @staticmethod
    def solve(schema):
        if schema.get_type() == "DCE":

            feature_set = features(schema)

            simi = feature_set['action_trait_similarity']
            dissimi = feature_set['action_!trait_similarity']

            if feature_set['causal_relation']:
                # if action and !trait are more related, then second element
                if simi > 0 and simi > dissimi:
                    return schema.answer_A, ((simi - dissimi) / simi)

                # if action and !trait are more related, then first element
                if dissimi > 0 and dissimi > simi:
                    return schema.answer_B, ((dissimi - simi) / dissimi)

                return None

            if feature_set['opposition_relation']:
                # if action and !trait are more related, then second element
                if simi > 0 and simi > dissimi:
                    return schema.answer_B, ((simi - dissimi) / simi)

                # if action and !trait are more related, then first element
                if dissimi > 0 and dissimi > simi:
                    return schema.answer_A, ((dissimi - simi) / dissimi)

                return None
            else:
                # print("Not enough information to resolve: " + schema.sentence)
                return None
        else:
            # print("Not classified as DCE: " + schema.sentence)
            return None
