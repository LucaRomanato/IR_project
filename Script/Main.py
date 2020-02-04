import requests, os
from io import BytesIO
import webbrowser
from flask import Flask, render_template, request, send_from_directory, jsonify, send_file, url_for
from unsplash.api import Api
from unsplash.auth import Auth
import dateutil.parser
from elasticsearch import Elasticsearch
import subprocess

import userPreprocess as pp
import Index as id
import Twitter as tw
import Query as qu


client_id = "52d01f19c56e72284ecb5978e8730c065d6f4f35efee186b2f9af0723f88a880"
client_secret = "2606edd096635c8ece8f78f6438eae0e22c6ef41b16d41e9038499addfc74820"
redirect_uri = ""
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
unsplash_api = Api(auth)

app = Flask(__name__, template_folder='../pages', static_folder='../pages/static')
bow = []
user = []
users_bow = []
currentUser = None


# Start EL server
def startELServer():
    command = os.path.abspath('../elasticsearch/bin/elasticsearch')
    popen = subprocess.Popen('cmd /c' + command)
    popen.wait()


# Connection to elasticsearch server and start client istance
def connectToELServer():
    requests.get('http://localhost:9200')
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    client = Elasticsearch("localhost:9200")

    # Clear index if already exists
    if es.indices.exists(index="twitter"):
        es.indices.delete(index='twitter', ignore=[400, 404])
    return client, es


def Start():
    try:
        client, es = connectToELServer();
    except Exception as err:
        print(err)
        startELServer();
        client, es = connectToELServer();
    return (client, es)


def getImageUrl(topic):
    try:
        photo = unsplash_api.photo.random(1, query=topic)
        c = photo[0].urls.regular
        return photo[0].urls.regular
    except:
        return url_for('static', filename='img/back-black.jpg', _external=True)


@app.route("/uimages/<topic>", methods=['GET', 'POST'])
def uimages(topic):
    return getImageUrl(topic)


@app.route("/fimages/<topic>", methods=['GET', 'POST'])
def fimages(topic):
    res = requests.get(getImageUrl(topic))
    byte_res = BytesIO(res.content)
    return send_file(byte_res, mimetype='image/jpg', cache_timeout=0)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder,
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=['GET', 'POST'])
def login():
    global users_bow
    users_bow = pp.getUsersBows()
    all_users = pp.getUsers(users_bow)
    return render_template('login.html', title='Login', users=all_users)


@app.route("/<user>/bow", methods=['GET', 'POST'])
def bow(user):
    global bow
    global users
    global users_bow
    global currentUser
    currentUser = user
    users = pp.getUsersNotCurrent(users_bow, user)
    bow = pp.getUserBow(users_bow, user)

    return jsonify(bow)


@app.route("/search", methods=['POST'])
def search():
    global bow
    global currentUser

    data = request.get_json(force=True)
    query = data['q']
    topic = data['t']
    page_number = data['pn']

    target_pos = "target:" in query
    date_pos = "date:" in query

    if (target_pos):
        target = query[(target_pos + 6):].split(" ")[0].replace("target:", "")
        query = query.replace("target:" + query[(target_pos + 6):].split(" ")[0] + " ", "")
    else:
        target = ""

    if (date_pos):
        temp = query[(date_pos + 4):].split(" ")[0].replace("date:", "")
        date = dateutil.parser.parse(temp).strftime('%Y-%m-%d %H:%M:%S')
        date_string = str(date)
        temp_end = date_string.replace(date_string.split(" ")[1], "") + " " + "23:59:59"
        date_end = dateutil.parser.parse(temp_end).strftime('%Y-%m-%d %H:%M:%S')
        query = query.replace("date:" + query[(date_pos + 4):].split(" ")[0] + " ", "")
    else:
        date = ""
        date_end = ""

    res = qu.search(currentUser, query, topic, target, date, date_end, page_number, 10, bow, "")
    return jsonify(res)


@app.route("/<user>", methods=['GET', 'POST'])
def home(user):
    global bow
    global users

    return render_template('home.html', user=user, bow=bow, title=user + '\'s Home',
                           background_image=getImageUrl('all'), users=users)


print("Start ElasticSearch server")
client, es = Start()
print("Open connection")

print()

print("Start crawling date")
tw.twitter_scraper()
print("End crawling date")

print()

print("Start create index of tweet's document")
id.createIndexDocuments(client);
print("Index created successfully")

print()

print("Start GUI")

if __name__ == "__main__":
    webbrowser.open('http://localhost:5000')
    app.run()
