from winosolver.schema.XMLParser import *
from winosolver.dce.features_tools import *

schemes = parse_xml()
add_labels(schemes)

print([schemes.index(schema) for schema in schemes if schema.get_type() == "DCE"])
DCE = [0, 1, 6, 7, 8, 9, 10, 11, 14, 15, 22, 23, 28, 29, 30, 31, 34, 35, 38, 39, 44, 45, 50, 51, 68, 69, 88, 89, 134,
       135, 146, 147, 150, 151, 210, 211, 214, 215, 226, 227, 252, 253, 254, 259, 260, 261, 262, 263, 264, 267, 268]


prob_DCE = len(DCE) / len(schemes)

# print([schemes.index(schema) for schema in schemes if schema.get_type() != "DCE"])
non_DCE = [2, 3, 4, 5, 12, 13, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 32, 33, 36, 37, 40, 41, 42, 43, 46, 47, 48, 49,
           52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
           81, 82, 83, 84, 85, 86, 87, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
           108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
           130, 131, 132, 133, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 148, 149, 152, 153, 154, 155, 156, 157,
           158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
           180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201,
           202, 203, 204, 205, 206, 207, 208, 209, 212, 213, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 228, 229,
           230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
           255, 256, 257, 258, 265, 266, 269, 270, 271, 272]

""" ANALYZING RULE R1 """

# print([schemes.index(schema) for schema in schemes if is_dce_structure(schema) is False])
# Applying this method is quite time consuming, that's why it is hard written here.
non_R1 = [8, 9, 39, 46, 47, 52, 53, 56, 57, 64, 65, 66, 67, 69, 76, 77, 84, 85, 90, 91, 96, 97, 100, 101, 108, 109, 110,
          111, 116, 117, 130, 131, 132, 133, 136, 137, 146, 147, 154, 155, 156, 157, 158, 159, 166, 167, 188, 189, 202,
          203, 208, 209, 210, 211, 216, 217, 222, 223, 224, 225, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 242,
          243, 244, 245]

# Calculate the new ensembles
R1 = [schemes.index(schema) for schema in schemes if schemes.index(schema) not in non_R1]
R1_DCE = [schemes.index(schema) for schema in schemes if schemes.index(schema) in R1 and
          schema.get_type() == "DCE"]
R1_non_DCE = [schemes.index(schema) for schema in schemes if schemes.index(schema) in R1 and
              schema.get_type() != "DCE"]
DCE_non_R1 = [schemes.index(schema) for schema in schemes if schemes.index(schema) in non_R1 and
              schema.get_type() == "DCE"]
non_DCE_non_R1 = [schemes.index(schema) for schema in schemes if schemes.index(schema) in non_R1 and
                  schema.get_type() != "DCE"]

print("P(DCE) = " + str(len(DCE)/len(schemes)))
print("P(R1) = " + str(len(R1)/len(schemes)))
print(" ")
print("P(DCE | R1) = " + str(len(R1_DCE) / len(R1)))
print("P(non-DCE | R1) = " + str(len(R1_non_DCE) / len(R1)))
print("P(R1 | DCE) = " + str(len(R1_DCE) / len(DCE)))
print("P(DCE | non-R1) = " + str(len(DCE_non_R1) / len(non_R1)))

# Calculate the new ensembles
R2 = [schemes.index(schema) for schema in schemes if is_causal_relation(schema) or
      is_opposition_relation(schema)]
non_R2 = [schemes.index(schema) for schema in schemes if schemes.index(schema) not in R2]
R2_DCE = [schemes.index(schema) for schema in schemes if schemes.index(schema) in R2 and
          schema.get_type() == "DCE"]
R2_non_DCE = [schemes.index(schema) for schema in schemes if schemes.index(schema) in R2 and
              schema.get_type() != "DCE"]
DCE_non_R2 = [schemes.index(schema) for schema in schemes if schemes.index(schema) in non_R2 and
              schema.get_type() == "DCE"]
non_DCE_non_R2 = [schemes.index(schema) for schema in schemes if schemes.index(schema) in non_R2 and
                  schema.get_type() != "DCE"]
"""
print("-----")
print("P(DCE) = " + str(len(DCE) / len(schemes)))
print("P(R2) = " + str(len(R2) / len(schemes)))
print(" ")
print("P(DCE | R2) = " + str(len(R2_DCE) / len(R2)))
print("P(non-DCE | R2) = " + str(len(R2_non_DCE) / len(R2)))
print("P(R2 | DCE) = " + str(len(R2_DCE) / len(DCE)))
print("P(DCE | non-R2) = " + str(len(DCE_non_R2) / len(non_R2)))
"""

# Calculate the new ensembles
R3 = [schemes.index(schema) for schema in schemes if "S" in snippet_verb(schema)]
non_R3 = [schemes.index(schema) for schema in schemes if schemes.index(schema) not in R3]
R3_DCE = [schemes.index(schema) for schema in schemes if schemes.index(schema) in R3 and
          schema.get_type() == "DCE"]
R3_non_DCE = [schemes.index(schema) for schema in schemes if schemes.index(schema) in R3 and
              schema.get_type() != "DCE"]
DCE_non_R3 = [schemes.index(schema) for schema in schemes if schemes.index(schema) in non_R3 and
              schema.get_type() == "DCE"]
non_DCE_non_R3 = [schemes.index(schema) for schema in schemes if schemes.index(schema) in non_R3 and
                  schema.get_type() != "DCE"]

print("-----")
print("P(DCE) = " + str(len(DCE) / len(schemes)))
print("P(R3) = " + str(len(R3) / len(schemes)))
print(" ")
print("P(DCE | R3) = " + str(len(R3_DCE) / len(R3)))
print("P(non-DCE | R3) = " + str(len(R3_non_DCE) / len(R3)))
print("P(R3 | DCE) = " + str(len(R3_DCE) / len(DCE)))
print("P(DCE | non-R3) = " + str(len(DCE_non_R3) / len(non_R3)))
