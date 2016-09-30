from WikipediaDatabase import WikipediaDatabase
import warnings

warnings.filterwarnings("ignore")

# Creating a huge wikipedia data base
database = WikipediaDatabase("WordListDB")
# database.add_new_articles(201, 250) # done until 200
# database.print_all_articles()
print(len(database.get_all_articles()))