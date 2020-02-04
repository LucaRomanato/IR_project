import csv
from elasticsearch import helpers


def createIndexDocuments(client):
    body = {
        "settings": {
            "index": {"number_of_shards": 6,
                      "number_of_replicas": 1
                      },
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    }
                },
                "analyzer": {
                    "tweet_text_analyzer": {
                        "tokenizer": "standard",
                        "filter": [
                            "english_possessive_stemmer",
                            "lowercase",
                            "english_stop",
                            "english_stemmer"
                        ]
                    }
                },
                "normalizer": {
                    "keyword_lowercase": {
                        "type": "custom",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "location": {"type": "keyword", "normalizer": "keyword_lowercase"},
                "text": {
                    "type": "text",
                    "analyzer": "tweet_text_analyzer",
                    "search_analyzer": "tweet_text_analyzer"
                },
                "topic": {"type": "keyword", "normalizer": "keyword_lowercase"},
                "user": {"type": "keyword", "normalizer": "keyword_lowercase"}
            }
        }
    }
    client.indices.create(
        index="twitter", body=body
    )

    with open("../Tweets-csv/crawling-tweets.csv", "r", encoding="utf-8") as fileToLoad:
        reader = csv.DictReader(fileToLoad)

        resp = helpers.bulk(
            client,
            reader,
            index="twitter",
            doc_type="_doc",
        )
