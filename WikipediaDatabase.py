import sqlite3
import wikipedia
import os
from wikipedia.wikipedia import WikipediaPage
from nltk.corpus import words
import unittest
import string
import random
from GoogleSearch import should_add


class Article:
    def __init__(self, title, url, content, summary):
        self.title = title
        self.url = url
        self.content = content
        self.summary = summary


def is_db_exists(name):
    created = False
    name += '.db'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for n in files:
            if n == name:
                created = True
    return created


class WikipediaDatabase():

    def __init__(self, name):
        """
        Initialization of the databse
        :param name:
        """
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

    def add_article(self, topic):
        """
        TO DELETE

        Add one article to the current database
        :param topic: one potential wikipedia article
        :return: update of database
        """
        new_articles = []
        try:
            article = WikipediaPage(topic)
            isinstance(article, WikipediaPage)
        except wikipedia.exceptions.DisambiguationError as e:
            for suggestion in e.options:
                new_articles.append(WikipediaPage(suggestion))
        except Exception as e:
            print(e)

        self.connect()
        try:
            self.cursor.execute("""INSERT INTO articles(title, content, url, keywords) VALUES(?, ?, ?, ?)""",
                            (article.title, article.content, article.url, article.summary))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        self.conn.close()

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

        new_articles = []
        for word in word_list[minIndex:maxIndex]:
            try:
                page = wikipedia.page(word)
                print(word + ":" + page.url)
                new_articles.append(page)
            except Exception as e:
                print(word + ": + No article has been found ")
        self.add_many_articles(new_articles)
        print("All articles have been added to the database")

    def print_all_articles(self):
        """
        Print list of articles in the database
        :return:
        """
        self.connect()
        self.cursor.execute("""SELECT title, url FROM articles""")
        for row in self.cursor:
            print('{0} : {1}'.format(row[0], row[1]))
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

    def get_articles_by_keyword(self, keywords):
        articles = self.get_all_articles()
        selection = []
        for article in articles:
            if should_add(keywords, article.content):
                selection.append(article)
        return selection

    def delete_database(self):
        created = False
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for n in files:
                if n == self.name:
                    file = os.path.join(dir_path, n)
                    os.remove(file)


class TestWikipediaDatabase(unittest.TestCase):

    def test_is_db_created(self):
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        self.assertFalse(is_db_exists(name))
        database = WikipediaDatabase(name)
        self.assertTrue(is_db_exists(name))
        database.delete_database()
        self.assertFalse(is_db_exists(name))

    def test_add_articles(self):
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)
        database.add_new_articles(12, 15)
        database.print_all_articles()
        self.assertGreater(len(database.get_all_articles()), 0)
        database.delete_database()

    def test_add_articles(self):
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)
        database.add_new_articles(12, 15)
        self.assertGreater(len(database.get_all_articles()), 0)

        # Creating another object connecting to the database
        database_2 = WikipediaDatabase(name)
        database_2.print_all_articles()
        self.assertGreater(len(database_2.get_all_articles()), 0)

        # Deleting from one instance
        database.delete_database()
        database_2.delete_database()

    def test_add_articles(self):
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)
        database.add_new_articles(12, 15)
        # The article Bad_Sobernheim contains the word Germany
        self.assertEqual(len(database.get_articles_by_keyword(["Germany"])), 1)
        database.delete_database()
