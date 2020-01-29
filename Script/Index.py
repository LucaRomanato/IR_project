import requests, json, os, csv
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import subprocess

#Start EL server
def startELServer ():
    command = os.path.abspath('../elasticsearch/bin/elasticsearch')
    popen = subprocess.Popen('cmd /c' + command)
    popen.wait()

#Connection to elasticsearch server and start client istance
def connectToELServer ():
    res = requests.get('http://localhost:9200')
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")
    return client, es

#Create json file from csv
def csvToJson ():
    csvfile = open('../Tweets-csv/tweets.csv', 'r', encoding="utf8")
    jsonfile = open('../Tweets-csv/tweets.json', 'w')
    fieldnames = ('user', 'text', 'location', 'date')
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')

#Create index Elasticsearch documents from the json
def indexing (client):
    docs = [l.strip() for l in open("../Tweets-csv/tweets.json", encoding="utf8", errors='ignore')]
    print ("Number of documents: ", len(docs))

    doc_list = []
    for num, doc in enumerate(docs):
        try:
            dict_doc = json.loads(doc)
            dict_doc["timestamp"] = datetime.now()
            dict_doc["id"] = num
            doc_list += [dict_doc]
        except json.decoder.JSONDecodeError as err:
            print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)

        try:
            print ("\nAttempting to index the list of docs using helpers.bulk()")
            resp = helpers.bulk(
                client,
                doc_list,
                index = "index",
                doc_type = "_doc"
            )
            print("Ho creato gli index")
            return resp
        except Exception as err:
            print("Elasticsearch helpers.bulk() ERROR:", err)
            quit()

def createIndexDocuments():
    try:
        client, es = connectToELServer();
    except Exception as err:
        startELServer();
        client, es = connectToELServer();
    csvToJson();
    indexing(client)

createIndexDocuments()
