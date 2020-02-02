from io import BytesIO

import requests
from flask import Flask, render_template, request, send_from_directory, jsonify, send_file, url_for
from Script.userPreprocess import preProcess
import webbrowser
from unsplash.api import Api
from unsplash.auth import Auth

client_id = "52d01f19c56e72284ecb5978e8730c065d6f4f35efee186b2f9af0723f88a880"
client_secret = "2606edd096635c8ece8f78f6438eae0e22c6ef41b16d41e9038499addfc74820"
redirect_uri = ""
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
unsplash_api = Api(auth)

app = Flask(__name__, template_folder='../pages', static_folder='../pages/static')
bow = []


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
    return render_template('login.html', title='Login')


@app.route("/<user>/bow", methods=['GET', 'POST'])
def bow(user):
    global bow
    bow = preProcess()
    return jsonify(bow)


@app.route("/<user>", methods=['GET', 'POST'])
def home(user):
    global bow
    #####################
    print(bow)
    ####################
    query = request.args.get('q', '', str)
    topic = request.args.get('t', '', str)
    page_number = request.args.get('pn', 1, int)
    page_size = request.args.get('ps', 10, int)

    # if(query!=""):
    # Chiamata

    return render_template('home.html', user=user, bow=bow, title=user + '\'s Home',
                           background_image=getImageUrl('science'))


if __name__ == "__main__":
    #webbrowser.open('http://localhost:5000')
    app.run()
