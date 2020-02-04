# Information Retrival project
## Tweetify personalized search engine for tweets
#### Develop by
- Matteo Pelucchi: 806798
- Luca Romanato: 807691

### About

The following project implemented a custom search engine for tweets based
on user's preferences.

### Requirements
- Python 3.7 or higher
- ElasticSearch
free download at the following link: https://www.elastic.co/downloads/elasticsearch

### Instructions
Clone repository:
```
git clone https://github.com/LucaRomanato/IR_project.git
cd IR_project
```
Install dependency:
```
pip install -r requirements.txt
```
Now, it is usefull to put ElastiSearch folder in the root of the project and rename ElasticSearch folder in "elasticsearch" (without quotes)

The root folder must be as follow:

```bash
C:.
│   .gitignore
│   README.md
│   requirements.txt
│
├───elasticsearch
├───pages
├───Script
└───Tweets-csv
```
Run ElasticSearch, you can use this command if the previous suggested commands have been executed:
```
./elasticsearch/bin/elasticsearch

Alternatively, just start the elasticsearch.bat file in the bin folder
```

Now the environment is ready, run the program with this command:
```
cd IR_project/Script
python main.py
```
### Notes
* Tweets are in: "Tweets-csv/crawling-tweets.csv"
* Users's bows are: in "Tweets-csv/users-bows.csv"

If you need to regenerate these files you have to lunch the following commands:
* Tweets: `python -c 'import Twitter; print Twitter.getTweetPrompt()'`
* Bows: `python -c 'import Twitter; print Twitter.getUserPrompt()'`