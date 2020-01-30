import requests
from elasticsearch import Elasticsearch
import elasticsearch as es

def connectToELServer ():
    res = requests.get('http://localhost:9200')
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")
    #cancellare index
    #es.indices.delete(index='index', ignore=[400, 404])
    return client, es

client, es = connectToELServer();

#query prova base
res = es.search(index='index',body={'query':{'match':{'text':'#SolarOrbiter'}}})
print("%d documents found" % res['hits']['total']['value'])
for doc in res['hits']['hits']:
    print("id: %s, score: %s ) %s" % (doc['_id'], doc['_score'], doc['_source']['text']))
    print("\n")
    
#query prova con BoW
