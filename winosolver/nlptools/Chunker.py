import nltk
from nltk.corpus import conll2000

"""
Chunker. Also containing function returning the main structure of a sentence.
For instance: The city councilmen refused the demonstrators a permit because they feared violence.
--> [('NP', 'The city councilmen '), ('VBD', 'refused'), ('NP', 'the demonstrators '), ('NP', 'a permit '),
    ('IN', 'because'), ('NP', 'they '), ('VBD', 'feared'), ('NP', 'violence '), ('.', '.')]
"""


class Chunker(nltk.ChunkParserI):

    def __init__(self):
        """
        Based on from UnigramChunker from NLTK book, chapter 7
        :param train_sents:
        """
        # TODO change the chunk types
        self.test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
        train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)

    def evaluate(self, gold):
        print(self.tagger.evaluate(self.test_sents))

    def parse(self, sentence):
        """
        Taken from UnigramChunker from NLTK book, chapter 7
        :param sentence: list of tuples of words with pages
        :return:
        """
        if isinstance(sentence, str):
            sentence = pre_process_sentence(sentence)
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


def pre_process_document(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


def pre_process_sentence(sentence):
    return nltk.pos_tag(nltk.word_tokenize(sentence))


def get_main_pos(parent):
    main_labels = []
    for node in parent:
        if type(node) is nltk.Tree:
            node_tuple = node.label(), get_words(node)
            main_labels.append(node_tuple)
        else:
            node_tuple = (node[1], node[0])
            main_labels.append(node_tuple)
    return main_labels


def get_words(parent):
    words = ""
    for node in parent:
        if type(node) is nltk.Tree:
            words += get_words(node)
        else:
            words += node[0] + " "
    return words
