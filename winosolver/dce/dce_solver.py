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

    @staticmethod
    def solve(schema):
        if schema.get_type() == "DCE":

            feature_set = features(schema)
            for feature in feature_set:
                print(str(feature) + " -> " + str(feature_set[feature]))
            print("")

            simi = feature_set['action_trait_similarity']
            dissimi = feature_set['action_!trait_similarity']

            if feature_set['causal_relation']:
                # if action and !trait are more related, then second element
                if simi > 0 and simi > dissimi:
                    return schema.answer_A, ((simi - dissimi) / simi)

                # if action and !trait are more related, then first element
                if dissimi > 0 and dissimi > simi:
                    return schema.answer_B, ((dissimi - simi) / dissimi)

                return "unable to answer yet"

            if feature_set['opposition_relation']:
                # if action and !trait are more related, then second element
                if simi > 0 and simi > dissimi:
                    return schema.answer_B, ((simi - dissimi) / simi)

                # if action and !trait are more related, then first element
                if dissimi > 0 and dissimi > simi:
                    return schema.answer_A, ((dissimi - simi) / dissimi)

                return "unable to answer yet"
            else:
                print("Not enough information to resolve: " + schema.sentence)
                return None
        else:
            print("Not classified as DCE: " + schema.sentence)
            return None
