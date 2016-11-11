from winosolver.cknowledge.WikipediaDatabase import *
import random
import string
import unittest


# FIXME WITH STATIC PATHS


class TestWikipediaDatabase(unittest.TestCase):

    def test_is_db_created(self):
        # Random string for name of a new database
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        self.assertFalse(is_db_exists(name))

        # Creating the database
        database = WikipediaDatabase(name)
        self.assertTrue(is_db_exists(name))

        # Deleting the database
        database.delete_database()
        self.assertFalse(is_db_exists(name))

    def test_add_articles_one_database(self):
        # Creating a new database
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)

        # Adding articles, at most 4.
        database.add_new_articles(12, 15)
        self.assertGreater(len(database.get_all_articles()), 0)
        self.assertGreaterEqual(4, len(database.get_all_articles()))

        # Deleting the database
        database.delete_database()

    def test_delete_duplicates(self):
        # Creating a database with 3 identical articles
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)
        database.add_many_articles(["Cat", "Cat", "Dog", "Cat"])
        self.assertEqual(len(database.get_all_articles()), 4)

        # Deleting the duplicates in the database, should be only two article now
        self.assertTrue(database.delete_duplicates())
        self.assertEqual(len(database.get_all_articles()), 2)

        # Shouldn't delete any new articles now
        self.assertTrue(database.delete_duplicates())
        self.assertEqual(len(database.get_all_articles()), 2)

        # Deleting the database
        database.delete_database()

    def test_add_articles_two_databases(self):
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)
        database.add_new_articles(12, 15)
        self.assertGreater(len(database.get_all_articles()), 0)

        # Creating another object connecting to the database
        database_2 = WikipediaDatabase(name)
        self.assertGreater(len(database_2.get_all_articles()), 0)

        # Deleting the database
        database.delete_database()
        database_2.delete_database()

    def test_get_article_by_keywords(self):
        # Creating a database
        name = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        database = WikipediaDatabase(name)
        database.add_many_articles(["Cat", "FC Metz", "Hospital", "Dog"])

        # The articles Cat and Dog contain the word species
        self.assertEqual(len(database.get_articles_by_keywords(["species"])), 2)
        database.delete_database()
