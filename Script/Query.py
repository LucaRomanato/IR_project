import requests
from elasticsearch import Elasticsearch
from userPreprocess import preProcess
import elasticsearch as es

def connectToELServer ():
    res = requests.get('http://localhost:9200')
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")
    #cancellare index
    #es.indices.delete(index='index', ignore=[400, 404])
    return client, es

client, es = connectToELServer();


#####################
bow = preProcess()
print("BOW\n")
print(bow)
####################

#query prova base
#res = es.search(index='index',body={'query':{'match':{'text':'#SolarOrbiter'}}})
#print("%d documents found" % res['hits']['total']['value'])
#for doc in res['hits']['hits']:
#    print("id: %s, score: %s ) %s" % (doc['_id'], doc['_score'], doc['_source']['text']))
#    print("\n")

#Query BoW

text_query = "Trump"
must = []
must.append({"query_string":{ "query":text_query, "default_field": "text"}})

should = []
for i in range(0,20):
        should.append({"match" : { "text": bow[i]}})
        
#must.append({"query_string":{ "query":query, "default_field": "text"}})
#should.append({"match": {"text": bow}})
#q = {"must": must,"should": should}

# Take the user's parameters and put them into a
# Python dictionary structured as an Elasticsearch query:
query_body = {
        "query":{
                "function_score":{
                 "query": {
                         "bool" : { 
                                 "should": should,
                                 "must": must,
                                  }  
                          }
                         }
                        }
 
}

# Pass the query dictionary to the 'body' parameter of the
# client's Search() method, and have it return results:
res = es.search(index='index',body=query_body)
print("%d documents found" % res['hits']['total']['value'])
for doc in res['hits']['hits']:
    print("id: %s, score: %s, user: %s ) %s" % (doc['_id'], doc['_score'], doc['_source']['user'], doc['_source']['text']))
    print("\n")
