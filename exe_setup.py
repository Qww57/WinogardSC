from distutils.core import setup
import py2exe
import os
import nltk
from CommonKnowledgeDataBase import *
from DirectCausalEvent import *
from Model import *
from Sources import *
from ToolsForNLP import *


# From command line with python 3.4: python setup.py py2exe

# TODO some problems to fix: parse exception from XML file

setup(
    # Option to be run as executable from py2exe
    options = {
        'py2exe': {
            'bundle_files': 2,
            'includes':['nltk',
                        'commonknowledge', 'dce',
                        'schema', 'Model', 'nlptools']
            }
    },
    console = ['main.py'],
    # windows = [{'script': "hello.py"}],
    zipfile = None,
)
