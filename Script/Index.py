import requests, json, os, csv
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import subprocess
import elasticsearch as es

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
    #cancellare index
    #es.indices.delete(index='index', ignore=[400, 404])
    return client, es

#Create json file from csv
def csvToJson ():
    print("conversione csv to json")
    csvfile = open('../Tweets-csv/tweets.csv', 'r', encoding="utf8")
    jsonfile = open('../Tweets-csv/tweets.json', 'w')
    fieldnames = ('user', 'text', 'location', 'date')
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')
    
    print("fine conversione csv to json")

def get_data_from_text_file(self):
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]

def indexing (client):
    docs = get_data_from_text_file("../Tweets-csv/tweets.json")
    print ("String docs length:", len(docs))
    doc_list = []
    for num, doc in enumerate(docs):
        try:
            doc = doc.replace("True", "true")
            doc = doc.replace("False", "false")
            dict_doc = json.loads(doc)
            dict_doc["timestamp"] = datetime.now()
            dict_doc["_id"] = num
            doc_list += [dict_doc]
        except json.decoder.JSONDecodeError as err:
            print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)
            print ("Dict docs length:", len(doc_list))
        try:
            print ("\nAttempting to index the list of docs using helpers.bulk()")
            resp = helpers.bulk(
                client,
                doc_list,
                index = "index",
                doc_type = "_doc"
                )
            print ("helpers.bulk() RESPONSE:", resp)
            print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
    
        except Exception as err:
            print("Elasticsearch helpers.bulk() ERROR:", err)
            quit()

def createIndexDocuments():
    try:
        client, es = connectToELServer();
    except Exception as err:
        #startELServer();
        client, es = connectToELServer();

    csvToJson();
    indexing(client)

createIndexDocuments()

#query prova
res = es.search(index='index',body={'query':{'match':{'text':'NASA'}}})
print(res['hits']['hits']);