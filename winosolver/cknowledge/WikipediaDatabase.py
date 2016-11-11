from nltk.corpus import words
from wikipedia.wikipedia import WikipediaPage
from winosolver.nlptools import Tokenizer
import os
import sqlite3
import wikipedia


class Article:
    """
    Representation of a wikipedia article object
    """

    def __init__(self, title, url, content, summary):
        self.title = title
        self.url = url
        self.content = content
        self.summary = summary


def is_db_exists(name):
    """
    :param name: name of the database
    :return: boolean for existence of database
    """
    created = False
    name += '.db'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for n in files:
            if n == name:
                created = True
    return created


class WikipediaDatabase:

    def __init__(self, name):
        """
        Initialization of the databse
        :param name:
        """
        # TODO FIXME static path
        self.name = name + '.db'
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        Creation of the database if running the program for the first time
        :return:
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             title TEXT,
             content TEXT,
             url TEXT,
             keywords TEXT
            )
        """)
        self.conn.commit()

    def add_many_articles(self, topics):
        """
        Add many articles to the current database
        :param new_articles: list of wikipedia articles from the wikipedia API
        :return: update of database
        """
        article_list = []
        self.connect()
        new_articles = []
        if isinstance(topics[0], str):
            for topic in topics:
                try:
                    new_article = WikipediaPage(topic)
                    new_articles.append(new_article)
                except wikipedia.exceptions.DisambiguationError as e:
                    print(topic + ": too many ambiguous results") #for suggestion in e.options:
                except Exception as e:
                    print(e)
        else:
            new_articles = topics
        try:
            for article in new_articles:
                isinstance(article, WikipediaPage)
                article_list.append((article.title, article.content, article.url, article.summary))
            self.cursor.executemany("""INSERT INTO articles(title, content, url, keywords) VALUES(?, ?, ?, ?)""",
                                    article_list)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        self.conn.close()

        return new_articles

    def add_new_articles(self, minIndex, maxIndex):
        """
        Search for articles on wikipedia from the word list of NLTK and add them to
        the current database
        :param minIndex: index to start in the list of words
        :param maxIndex:
        :return:
        """
        word_list = words.words()

        if minIndex is None:
            minIndex = 0
        if maxIndex is None:
            maxIndex = len(word_list)

        index = minIndex-1

        new_articles = []
        for word in word_list[minIndex:maxIndex]:
            index += 1
            try:
                page = wikipedia.page(word)
                print(str(index) + ":" + word + ":" + page.url)
                new_articles.append(page)
            except Exception as e:
                print(str(index) + ":" + word + ": + No article has been found ")
        self.add_many_articles(new_articles)
        print("All articles have been added to the database")

    def print_all_articles(self):
        """
        Print list of articles in the database
        :return:
        """
        self.connect()
        self.cursor.execute("""SELECT id, title, url FROM articles""")
        for row in self.cursor:
            print('({0}) {1} : {2}'.format(row[0], row[1], row[2]))
        self.conn.close()

    def get_all_articles(self):
        """
        Return all wikipedia articles
        :return: list of wikipedia articles
        """
        self.connect()
        self.cursor.execute("""SELECT title, url, content, keywords FROM articles""")
        articles = []
        for row in self.cursor:
            article = Article(row[0], row[1], row[2], row[3])
            articles.append(article)
        self.conn.close()
        return articles

    def get_articles_by_keywords(self, keywords):
        articles = self.get_all_articles()
        return [article for article in articles if Tokenizer.should_add(keywords, article.content, "Inclusive")]

    def delete_duplicates(self):
        """
        Removes all the duplicates from database
        :return: boolean returning status
        """
        self.connect()
        try:
            self.cursor.execute("""DELETE FROM articles WHERE id NOT IN
                                    (
                                      SELECT MIN(id) id
                                        FROM articles
                                       GROUP BY title
                                    );""")
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            return False

    def delete_database(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for n in files:
                if n == self.name:
                    file = os.path.join(dir_path, n)
                    os.remove(file)
