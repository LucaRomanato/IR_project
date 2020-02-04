from elasticsearch import Elasticsearch
import elasticsearch as es
import math

def connectToELServer():
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")
    return client, es


client, es = connectToELServer();


def search(query, topic, target, tweet_date, tweet_date_end, page_number, page_size, bow, country='US'):
    start_from = (page_number * page_size) - page_size

    must = []
    should = []

    for bow1 in bow:
        should.append({"match": {"text": bow1}})

    if query.startswith('"') and query.endswith('"'):
        query = query.replace('"', '')
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
            must.append({"term": {"user": target}})

        if tweet_date != "":
            must.append({"range": {"date": {"gte": tweet_date, "lte": tweet_date_end}}})

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
                            "origin": "2020-01-01 00:00:00",
                            "scale": "30d",
                            "offset": "1d",
                            "decay": 0.3
                        }
                    }
                }
            }

        }
    res = es.search(index='twitter', body=query_body)
    total_page = math.ceil(res['hits']['total']['value'] / page_size)

    return total_page, page_number, res['hits']['hits']
