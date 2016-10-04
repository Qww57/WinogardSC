import treetaggerwrapper


class TreeTaggerList:
    def __init__(self, tree_word_list):
        for word in tree_word_list:
            isinstance(word, TreeTaggerWord)
        self.tree_word_list = tree_word_list
        self.index = 0

    def get_word_sequence(self):
        return [tree_word.word for tree_word in self.tree_word_list]

    def get_tag_sequence(self):
        return [tree_word.postag for tree_word in self.tree_word_list]

    def get_lemma_sequence(self):
        return [tree_word.lemma for tree_word in self.tree_word_list]

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.tree_word_list[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __len__(self):
        return len(self.tree_word_list)

    def __str__(self):
        s = "["
        for word in self.tree_word_list:
            s += word.to_string() + ", "
        s += "]"
        return s

    def print(self):
        print(str(self))


class TreeTaggerWord:
    def __init__(self, triplet):
        self.word, self.postag, self.lemma = triplet
        self.nltk_tag = "" #from NLTK

    def to_string(self):
        return "[" + self.word + ", " + self.postag + ", " + self.nltk_tag + ", " + self.lemma + "]"

    def set_nltk_tag(self, tag):
        self.nltk_tag = tag

    def print(self):
        print(self.to_string())


def analyze(sentence):
    """
    List of tags: http://courses.washington.edu/hypertxt/csar-v02/penntable.html
    :param sentence:
    :return:
    """
    # Initializing the tagger in English
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR='/TreeTagger')
    tags = tagger.TagText(sentence)

    # Improving the result layout
    def tag(output):
        words = []
        for w in output:
            words.append(TreeTaggerWord(w.split("\t")))
        return words

    data = TreeTaggerList(tag(tags))
    return data
