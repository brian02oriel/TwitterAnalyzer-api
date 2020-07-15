import sys
sys.path.insert(1, '/Tweepy')
from Twitter.tweets import Tweets
import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    return "<h1>Welcome to Tweet Analyzer </h1><p>This path is for test conection between the API and the Client</p>"

@app.route('/api/twitter', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_tweets():
    #print("REQUEST json: ",request.json.get('keywords'))    
    #print("\n")
    keywords = request.json.get('keywords')
    results = Tweets(keywords)
    #print(results)
    return jsonify(results)

app.run()