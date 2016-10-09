from winosolver.dce.dce_solver import *
from winosolver.schema.XMLParser import *
import warnings
import unittest

warnings.filterwarnings("ignore")


class TestDCESolver(unittest.Testcase):

    def test_solver(self):
        schema_set = parse_xml()
        add_labels(schema_set)
        schema_set = [schema for schema in schema_set if schema.get_type() == "DCE"]

        right_count = 0
        answer_count = 0
        for schema in schema_set:
            print("")
            feature_set = features(schema)
            for feature_name in feature_set:
                print(str(feature_name) + " -> " + str(feature_set[feature_name]))
            guess = self.resolve(schema)
            if 'unable' not in guess:
                answer_count += 1
            print(schema.correct + " - predicted: " + guess)
            if schema.correct == guess:
                right_count += 1

        print(str(right_count / answer_count * 100) + "% of good answers when answering")
        print(str(right_count / len(schema_set) * 100) + "% of good answers in general")

    @staticmethod
    def resolve(schema):
        dce_solver = DirectCausalEventSolver()
        answer = dce_solver.solve(schema) if dce_solver.solve(schema) is not None else "unable to predict"
        return answer

