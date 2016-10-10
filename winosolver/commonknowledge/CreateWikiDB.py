""" Script used to create a database made of wikipedia articles"""

from winosolver.commonknowledge.WikipediaDatabase import WikipediaDatabase
from nltk.corpus import words
import time
import warnings

warnings.filterwarnings("ignore")

print(len(words.words()))

# I started by performing the first 1000 requests. It had an average of 10 articles per minutes, so one request is
# performed and treated every 6 seconds. Getting the whole# database would take 237 000 / 10 / 60 / 24 = 16,5 days.
# It is then too long to have all of them, so I chose to just take the 30 first ones of each hundred: from 0 to 30,
# from 1000 to 1030, ..., etc, ..., and from 236 000 to 236 030.
#
# By choosing only the 30 first ones, the computation time decreases to only 12 hours. In terms of articles and
# requests, it would represent then 6900 requests (230 * 30), and at least 2300 articles since around 30%
# (303 for the first thousand) are leading to a new article download. This will create us a basis to start working with
# The database can then be extended further on easily since the WikipediaDataBase class contains a method to delete
# duplicates.

debut = time.time()

# Creating a huge wikipedia data base
database = WikipediaDatabase("WordListDB")
print(len(database.get_all_articles()))
for i in range(146, 160, 1):  # done until 146, max is 236 000 / 1000 = 230
    minIndex, maxIndex = i * 1000, i * 1000 + 30
    database.add_new_articles(minIndex, maxIndex) # done until 800

print(len(database.get_all_articles()))

database.delete_duplicates()
print(len(database.get_all_articles()))
print(str((time.time() - debut) / 60) + " minutes")
