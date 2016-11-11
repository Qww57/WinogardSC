from winosolver.schema.XMLParser import *
from winosolver.dce.dce_solver import *
import warnings

warnings.filterwarnings("ignore")
"""
schemes = parse_xml()
add_labels(schemes)
schemes = [schema for schema in schemes if schema.get_type() == "DCE"]
correct = [1, 2, 6, 10, 11, 13, 14, 18, 19, 21, 32, 45, 46]
[print(schema.sentence) for schema in schemes if schemes.index(schema) in correct]
"""
schemes = parse_xml()
add_labels(schemes)
schemes = [schema for schema in schemes if schema.get_type() == "DCE"]
# wrong = [0, 3, 7, 9, 12, 15, 17, 20, 22, 23, 24, 25, 33, 38, 39]
wrong = [12]
features = [print(str(s.sentence) + "\n" + str(features(s))) for s in schemes if schemes.index(s) in wrong]

