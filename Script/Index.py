import requests, json, os, csv
import pandas as pd
from time import sleep
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from os import popen
import subprocess


subprocess.Popen('../elasticsearch/bin/elasticsearch')
#By default, the Elasticsearch instance will listen on port 9200
res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")
index_name = "index" #nel resp del bulk va perforza settato a mano

#cancellare index
#es.indices.delete(index='index', ignore=[400, 404])

csvfile = open('data.csv', 'r')
jsonfile = open('file.json', 'w')
#da csv a json
#fieldnames = ("Username","Text","Location", "Date","Topic")
fieldnames = ("Make","Model","Year") #sistemo nome colonne
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')

    
# define a function that will load a text file
def get_data_from_text_file(self):
# the function will return a list of docs
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]

# call the function to get the string data containing docs
docs = get_data_from_text_file("file.json")

# print the length of the documents in the string
print ("String docs length:", len(docs))

# define an empty list for the Elasticsearch docs
doc_list = []

# use Python's enumerate() function to iterate over list of doc strings
for num, doc in enumerate(docs):

# catch any JSON loads() errors
    try:

# prevent JSONDecodeError resulting from Python uppercase boolean
        doc = doc.replace("True", "true")
        doc = doc.replace("False", "false")

# convert the string to a dict object
        dict_doc = json.loads(doc)

# add a new field to the Elasticsearch doc
        dict_doc["timestamp"] = datetime.now()
    
# add a dict key called "_id" if you'd like to specify an ID for the doc
        dict_doc["_id"] = num

# append the dict object to the list []
        doc_list += [dict_doc]

    except json.decoder.JSONDecodeError as err:
# print the errors
        print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)

        print ("Dict docs length:", len(doc_list))

# attempt to index the dictionary entries using the helpers.bulk() method
    try:
        print ("\nAttempting to index the list of docs using helpers.bulk()")

# use the helpers library's Bulk API to index list of Elasticsearch docs
        resp = helpers.bulk(
            client,
            doc_list,
            index = "index",
            doc_type = "_doc"
            )

# print the response returned by Elasticsearch
        print ("helpers.bulk() RESPONSE:", resp)
        print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

    except Exception as err:

# print any errors returned w
## Prerequisiteshile making the helpers.bulk() API call
        print("Elasticsearch helpers.bulk() ERROR:", err)
        quit()

# get all of docs for the index
# Result window is too large, from + size must be less than or equal to: [10000]
query_all = {
'size' : 10_000,
'query': {
'match_all' : {}
}
}

print ("\nSleeping for a few seconds to wait for indexing request to finish.")
sleep(2)

# pass the query_all dict to search() method
resp = client.search(
index = index_name,
body = query_all
)

print ("search() response:", json.dumps(resp, indent=4))

# print the number of docs in index
print ("Length of docs returned by search():", len(resp['hits']['hits']))

#test query
res=es.get(index=index_name, doc_type='_doc',id=1)
print(res)

#res= es.search(index='some_index',body={'query':{'match':{'Make':'Alfa'}}})
#print(res['hits']['hits'])



