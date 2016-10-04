from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='winosolver',
    
    version='0.0.1',
    
    description='Project used to solve automatically Winograd schema',
    
    longescription=long_description,
    
    url='https://github.com/Qww57/WinogardSC',
    
    author = 'Tresontani Quentin',
    
    author_email='tresontani.quentin@gmail.com',
    
    license='Free for non-commercial use',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'License :: Free for non-commercial use'
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic ::Scientific/Engineering :: Artificial Intelligence'

    ],
    
    install_requires=[
        'bs4', # for google searches
        'nltk', 'PyDictionary', 'treetaggerwrapper', # for natural language processing
        'untangle', # for XML reading
        'pymining', 'wikipedia', # for data mining from wikipedia articles
    ],
    
    package_data={},
    
    data_files=[('my_data', ['data/data_file'])], #TODO
)
