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


print("\n\n\n\n\n")
#Query BoW con una parola keyword
text_query = "#YourShotPhotographer"
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
          "size":100,
          "query": {
            "function_score": {
              "query": {
                "bool" : { 
                            "should": should,
                            "must": must,
                            }
                        },
                "linear": {
                        "date_calendar": {
                                "origin": "2019-10-08", 
                                "scale": "10d",
                                "offset": "2d", 
                                "decay" : 0.7 
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
    print("id: %s, score: %s, user: %s, location: %s, date: %s )\n %s" % (
            doc['_id'], doc['_score'], doc['_source']['user'], doc['_source']['location'],
            doc['_source']['date'], doc['_source']['text']))
    print("\n")
