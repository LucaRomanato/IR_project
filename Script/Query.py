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
def search(query, topic, target, tweet_date, start_from, page_size, bow, country='US'):
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

        if topic != "":
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
                    },
                    "gauss": {
                        "date": {
                            "origin": "2020-01-29 00:00:00",
                            "scale": "10d"
                        }
                    }
                }
            }

        }

    res = es.search(index='twitter5', body=query_body)
    print(res)
    total_page = math.ceil(res['hits']['total']['value']/10)

    return total_page, res['hits']['hits']

nbow = preProcess()
print(search('"the Sun from"', "", "", "", 0, 10, nbow))
