# Get 10000 random pages from Wikipedia.
import urllib
import os
import shutil
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
import pprint
import os
import nltk.data
import urllib.request
import wikipedia
"""
class just_internet:
    from urllib.request import urlopen
    html = urlopen("http://www.google.com/")

    #Make the directory to store the HTML pages.
    try:
        print("Created the directory for storing the pages")
        os.mkdir('randompages')
    except:
        print('folder already created')

    base = 'http://en.wikipedia.org/wiki/'


    def download_random(num_page):
        for i in range(0, int(num_page)):
            download_page('Special:Random')
            print("Retrieved and saved page, "+ str(i))


    def download_page(name):
        url = base + name

        # Converting the HTML text to String
        wf = urllib.request.urlopen(url)
        mybytes = wf.read()  # read bytes from url
        wf.close()
        mystr = mybytes.decode("utf8")  # decodes bytes to string

        # Deleting all the HTML characters
        soup = BeautifulSoup(mystr, "html.parser")
        article_name = soup.title
        # body = soup.find('div',id="bodyContent")
        # raw_text = soup.find_all('p')
        # print(raw_text)

    def delete_empty_files():
        # Deleting all the empty files
        for root, dirs, files in os.walk('randompages/', topdown=False):
            for name in files:
                file = os.path.join(root, name)
                if os.stat(file).st_size is 0:
                    os.remove(file)

    # download_random(10)

    # delete_empty_files()
"""


