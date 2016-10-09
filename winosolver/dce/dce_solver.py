from winosolver.dce.features_tools import *


def features(schema):
    feature_set = {}

    feature_set['causal_relation'] = is_causal_relation(schema)
    feature_set['opposition_relation'] = is_opposition_relation(schema)

    action = get_action(schema)
    trait = get_trait(schema)
    antonym_trait = antonym(trait)
    print("Action: {} - Trait: {} - !Trait: {}".format(action, trait, str(antonym_trait)))
    try:
        feature_set['action_trait_similarity'] = similarity(action, trait)
    except Exception as e:
        feature_set['action_trait_similarity'] = -1
    try:
        feature_set['action_!trait_similarity'] = similarity(action, antonym_trait[0])
    except Exception as e:
        feature_set['action_!trait_similarity'] = -1
    return feature_set


class DirectCausalEventSolver:

    # TODO: take the negation of the action into consideration
    # TODO Improve the antonym selection

    @staticmethod
    def solve(schema):
        if schema.get_type() == "DCE":
            feature_set = features(schema)
            if feature_set['causal_relation']:
                # If, couldn't get any words, so any information.
                if feature_set['action_!trait_similarity'] is -1 and feature_set['action_trait_similarity'] is -1:
                    return None
                else:
                    # if action and !trait are more related, then second element
                    if feature_set['action_trait_similarity'] > 0:
                        return schema.answer_A

                    # if action and !trait are more related, then first element
                    if feature_set['action_!trait_similarity'] > 0:
                        return schema.answer_B

                    return "unable to answer yet"

            elif feature_set['opposition_relation']:
                # If, couldn't get any words, so any information.
                if feature_set['action_!trait_similarity'] is -1 and feature_set['action_trait_similarity'] is -1:
                    return None
                else:
                    # if action and !trait are more related, then second element
                    if feature_set['action_trait_similarity'] > 0:
                        return schema.answer_B

                    # if action and !trait are more related, then first element
                    if feature_set['action_!trait_similarity'] > 0:
                        return schema.answer_A

                    return "unable to answer yet"
            else:
                print("Not enough information to resolve: " + schema.sentence)
                return None
        else:
            print("Not classified as DCE: " + schema.sentence)
            return None
