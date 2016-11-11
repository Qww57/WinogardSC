""" Test class focusing on the DCE solver. """

from winosolver.dce.dce_solver import *
from winosolver.schema.XMLParser import *
import warnings
import unittest

warnings.filterwarnings("ignore")


class TestDCESolver(unittest.TestCase):

    def test_solver(self):
        schemes = parse_xml()
        add_labels(schemes)
        schemes = [schema for schema in schemes if schema.get_type() == "DCE"]
        print(len(schemes))
        right, wrong, silent = [], [], []

        for schema in schemes:
            guess = self.resolve(schema)
            if schema.correct == guess[0]:
                right.append([schemes.index(schema), guess])
            elif 'unable' in guess:
                silent.append([schemes.index(schema), guess])
            else:
                wrong.append([schemes.index(schema), guess])

        answers = len(wrong) + len(right)
        print(str(len(right) / answers * 100) + "% of good answers on DCE when answering")
        print(str(len(right) / len(schemes) * 100) + "% of good answers on all DCE")
        print(" ")
        print("Correct answer:")
        [print(r) for r in right]
        print(" ")
        print("Wrong answer:")
        [print(r) for r in wrong]
        print(" ")
        print("No answer:")
        [print(r) for r in silent]
        print(" ")
        print("End")

    @staticmethod
    def resolve(schema):
        dce_solver = DirectCausalEventSolver()
        answer = dce_solver.solve(schema) if dce_solver.solve(schema) is not None else "unable to predict"
        return answer
