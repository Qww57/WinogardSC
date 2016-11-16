from winosolver.schema.Schema import Schema
from winosolver.dce.dce_solver import DirectCausalEventSolver


def create_example():

    schema_set = []

    sentence = "The forward player scored to the goalkeeper because he was good."
    snippet = "he was good"
    pronoun = "he"
    answer_a = "The forward player"
    answer_b = "The goalkeeper"
    sentence_bis = "The forward player scored to the goalkeeper because he was bad."
    snippet_bis = "he was bad"

    current = Schema(ID=1, sentence=sentence, snip=snippet, pron=pronoun,prop1=answer_a, prop2=answer_b,
                     answer="to be guessed", source="console")

    opposite = Schema(ID=2, sentence=sentence_bis, snip=snippet_bis, pron=pronoun,prop1=answer_a, prop2=answer_b,
                      answer="to be guessed", source="console")

    schema_set.extend([current, opposite])

    sentence = "The forward player scored to the goalkeeper although he was good."
    snippet = "he was good"
    pronoun = "he"
    answer_a = "The forward player"
    answer_b = "The goalkeeper"
    sentence_bis = "The forward player scored to the goalkeeper although he was bad."
    snippet_bis = "he was bad"

    current = Schema(ID=3, sentence=sentence, snip=snippet, pron=pronoun, prop1=answer_a, prop2=answer_b,
                     answer="to be guessed", source="console")

    opposite = Schema(ID=4, sentence=sentence_bis, snip=snippet_bis, pron=pronoun, prop1=answer_a, prop2=answer_b,
                      answer="to be guessed", source="console")

    schema_set.extend([current, opposite])

    sentence = "The forward player missed against the goalkeeper because he was good."
    snippet = "he was good"
    pronoun = "he"
    answer_a = "The forward player"
    answer_b = "The goalkeeper"
    sentence_bis = "The forward player missed against the goalkeeper because he was bad."
    snippet_bis = "he was bad"

    current = Schema(ID=5, sentence=sentence, snip=snippet, pron=pronoun, prop1=answer_a, prop2=answer_b,
                     answer="to be guessed", source="console")

    opposite = Schema(ID=6, sentence=sentence_bis, snip=snippet_bis, pron=pronoun, prop1=answer_a, prop2=answer_b,
                      answer="to be guessed", source="console")

    schema_set.extend([current, opposite])

    sentence = "The forward player missed against the goalkeeper although he was good."
    snippet = "he was good"
    pronoun = "he"
    answer_a = "The forward player"
    answer_b = "The goalkeeper"
    sentence_bis = "The forward player missed against the goalkeeper although he was bad."
    snippet_bis = "he was bad"

    current = Schema(ID=7, sentence=sentence, snip=snippet, pron=pronoun, prop1=answer_a, prop2=answer_b,
                     answer="to be guessed", source="console")

    opposite = Schema(ID=8, sentence=sentence_bis, snip=snippet_bis, pron=pronoun, prop1=answer_a, prop2=answer_b,
                  answer="to be guessed", source="console")

    schema_set.extend([current, opposite])

    for schema in schema_set:
        schema.set_type("DCE")

    return schema_set

sentences = create_example()
[print(sentence) for sentence in sentences]
print(" ")
solver = DirectCausalEventSolver()
print(solver.solve(sentences[0]))
print(solver.solve(sentences[1]))
print(solver.solve(sentences[2]))
print(solver.solve(sentences[3]))
print(solver.solve(sentences[4]))
print(solver.solve(sentences[5]))
print(solver.solve(sentences[6]))
print(solver.solve(sentences[7]))
