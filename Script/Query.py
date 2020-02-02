from elasticsearch import Elasticsearch
import elasticsearch as es
from Script.userPreprocess import preProcess
import math

def connectToELServer():
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")
    return client, es


client, es = connectToELServer();

# Il target è la pagina da cui ho preso il tweet
def search(query, topic, target, tweet_date, page_number, page_size, bow, country='US'):

    start_from = (page_number * page_size) - page_size

    must = []
    should = []

    for bow1 in bow:
        should.append({"match": {"text": bow1}})

    if query.startswith('"') and query.endswith('"'):
        query = query.replace('"','')
        query_body = {
            "size": page_size,
            "from": start_from,
            "query": {
                "function_score": {
                    "query": {
                        "match_phrase": {
                            "text": query
                        }
                    }
                }
            }

        }
    else:
        must.append({"query_string": {"query": query, "default_field": "text"}})

        if topic != "All":
            must.append({"term": {"topic": topic}})

        if target != "":
            must.append({"term": {"target": target}})

        if tweet_date != "":
            must.append({"term": {"date": tweet_date}})

        query_body = {
            "size": page_size,
            "from": start_from,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": should,
                            "must": must,
                        }
                    }
                }
            }

        }
    print(query_body)
    res = es.search(index='twitter6', body=query_body)
    print(res)
    total_page = math.ceil(res['hits']['total']['value']/page_size)

    return total_page, page_number, res['hits']['hits']

#nbow = preProcess()
#print(search('"the Sun from"', "", "", "", 0, 10, nbow))
