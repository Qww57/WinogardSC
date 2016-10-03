import warnings
from nltk.corpus import words
import time
from CommonKnowledgeDataBase.WikipediaDatabase import WikipediaDatabase

warnings.filterwarnings("ignore")

print(len(words.words()))

# After having request the first 1000,Too long to have all of them, so I'll just take the 30 first ones of each hundred
# 0 to 30, 1000 to 1030, ... , 236 000 to 236 030
#
# It will enable me to make the computation faster since 10 articles are downloaded per minute, getting the whole
# database would take 237 000 / 10 / 60 / 24 = 16,5 days to download everything.By choosing only the 50 first ones,
# the computation time is decreased by 100. It would take only 12 hours then. It would represent then 230*30,
# 6900 requests, since around 30% (303 for the first thousand) are leading to a new article download. We can expect
# to reach 2 300 articles.
#
# Some tests will be performed on this data set. Later on, it could be easily extended since
# the WikipediaDataBase class contains a method to delete duplicates.

debut = time.time()

# Creating a huge wikipedia data base
database = WikipediaDatabase("WordListDB")
print(len(database.get_all_articles()))
for i in range(1, 10, 1): # max is 236 000 / 1000 = 230
    minIndex, maxIndex = i * 1000, i * 1000 + 30
    database.add_new_articles(800, 1000) # done until 800
print(len(database.get_all_articles()))

database.delete_duplicates()
print(len(database.get_all_articles()))
print(str((time.time() - debut)/60) + " minutes")

