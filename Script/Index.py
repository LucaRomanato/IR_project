import requests, os, csv
from elasticsearch import Elasticsearch, helpers
import subprocess
import time


# Start EL server
def startELServer():
    command = os.path.abspath('../elasticsearch/bin/elasticsearch')
    popen = subprocess.Popen('cmd /c' + command)
    popen.wait()


# Connection to elasticsearch server and start client istance
def connectToELServer():
    res = requests.get('http://localhost:9200')
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")
    # cancellare index
    # es.indices.delete(index='index', ignore=[400, 404])
    return client, es


def indexing(client):
    body = {
        "settings": {
            "index": {"number_of_shards": 6,
                      "number_of_replicas": 1
                      }
        },
        "mappings": {
            "properties": {
                "date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "location": {"type": "keyword"},
                "text": {"type": "text"},
                "topic": {"type": "keyword"},
                "user": {"type": "keyword"}
            }
        }
    }
    client.indices.create(
        index="twitter6", body=body
    )

    with open("../Tweets-csv/tutto-csv.csv", "r", encoding="utf-8") as fileToLoad:
        reader = csv.DictReader(fileToLoad)

        resp = helpers.bulk(
            client,
            reader,
            index="twitter6",
            doc_type="_doc",

        )
        print("Mappato")


def createIndexDocuments():
    try:
        client, es = connectToELServer();
    except Exception as err:
        startELServer();
        client, es = connectToELServer();

    indexing(client)


createIndexDocuments()
