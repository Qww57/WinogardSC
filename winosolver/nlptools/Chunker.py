""" Chunker class used to obtain the structure of schemas as a tree"""

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
    """
    Pre processing of documents before chunking.

    :param document: set of string sentences
    :return: pre-processed set of set of tokens
    """
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


def pre_process_sentence(sentence):
    """
    Pre processing of sentence before chunking.

    :param sentence: string sentences
    :return: pre-processed set of tokens
    """
    return nltk.pos_tag(nltk.word_tokenize(sentence))


def get_main_pos(tree):
    """
    Return the nodes with a depth of 1 which corresponds of the main structure of the sentence.

    :param tree: tree obtained with the chunker
    :return: main structure as set of tuples of tag and word.
    """

    def get_words(parent_node):
        words = ""
        for child_node in parent_node:
            words += get_words(child_node) if type(child_node) is nltk.Tree else child_node[0] + " "
        return words

    main_labels = []
    for node in tree:
        if type(node) is nltk.Tree:
            node_tuple = node.label(), get_words(node)
            main_labels.append(node_tuple)
        else:
            node_tuple = (node[1], node[0])
            main_labels.append(node_tuple)
    return main_labels

