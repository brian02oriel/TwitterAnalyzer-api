import sys
sys.path.insert(1, '/Tweepy')
from Twitter.tweets import Tweets

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    return "<h1>Welcome to Tweet Analyzer </h1><p>This path is for test conection between the API and the Client</p>"

@app.route('/api/twitter', methods=['POST'])
def get_tweets():
    #print(request.args.get('keyword'))
    keyword = request.args.get('keyword')
    results = Tweets(keyword)
    return jsonify(results)

app.run()