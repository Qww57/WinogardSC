from conceptnet5.query import lookup

#for assertion in lookup('c/en/example'):
#    print(assertion)

association = "http://conceptnet5.media.mit.edu/data/5.4/assoc/list/en/demonstrator,violence@0.5,teacher@-1?limit=50&filter=/c/en"
analysis = "http://conceptnet5.media.mit.edu/data/5.3/c/en/example"

import json
from urllib.request import urlopen

response = urlopen(association).read().decode('utf8')
obj = json.loads(response)
print(obj)
for o in obj:
    print(o)

response = urlopen(analysis).read().decode('utf8')
print(response)
obj = json.loads(response)
print(obj)
for o in obj:
    print(o)


# filter = core, if don't want to use the creative commons

import requests
import json

from urllib.request import urlopen

#myResponse = requests.get(address)
#if (myResponse.ok):
  #  print(myResponse.content)
  #  jData = json.loads(myResponse.content)

    #print("The response contains {0} properties".format(len(jData)))
    #print("\n")
    #for key in jData:
    #   print(key + " : " + jData[key])
    # print("DONE")
#else:
    # If response code is not ok (200), print the resulting http error code with description
 #   myResponse.raise_for_status()

import codecs

# myResponse = urlopen(address).read().decode('utf8')
# obj = json.loads(myResponse)
# print(myResponse)
# reader = codecs.getreader("utf-8")
# jData = json.loads(reader(myResponse))