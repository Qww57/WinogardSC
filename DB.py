import sqlite3
import wikipedia

"""
http://apprendre-python.com/page-database-data-base-donnees-query-sql-mysql-postgre-sqlite
"""

conn = sqlite3.connect('wiki_articles.db')
cursor = conn.cursor()


def create_table():
    # Creation of the database if running the program for the first time
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
         title TEXT,
         content TEXT,
         url TEXT,
         keywords TEXT
        )
    """)
    conn.commit()


def add_article(article):
    cursor.execute("""INSERT INTO articles(title, content, url, keywords) VALUES(?, ?, ?, ?)""",
               (article.title, article.content, article.url, article.title))
    conn.commit()

#ADD ROLLBACK IN ALL FUNCTIONS + do getters + go deleters

def add_many_articles(articles):
    list = []
    for article in articles:
        list.append((article.title, article.content, article.url, article.title))
    cursor.executemany("""INSERT INTO articles(title, content, url, keywords) VALUES(?, ?, ?, ?)""", list)
    conn.commit()

"""
cat = wikipedia.page("Cat")
add_article(cat)
dog = wikipedia.page("Dog")
elephant = wikipedia.page("Elephant")
articles = [dog, elephant]
add_many_articles(articles)
"""

from nltk.corpus import words
word_list = words.words()
print(len(word_list))

def add_new_articles(min, max):
    new_articles = []
    for word in word_list[min:max]:
        try:
            page = wikipedia.page(word)
            print(word + ":" + page.url)
            new_articles.append(page)
        except:
            print(word + ": + No article has been found")
    add_many_articles(new_articles)
    print("DONE")

# add_new_articles(15, 150)

cursor.execute("""SELECT title, url FROM articles""")
for row in cursor:
   print('{0} : {1}'.format(row[0], row[1]))

conn.close()