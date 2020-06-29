# -*- coding: utf-8 -*-
from os import environ
import tweepy as tw
import pandas as pd
import json
from Twitter.data_management import Summary

def Auth():
    #API keys
    consumer_key= environ.get('CONSUMER_KEY')
    consumer_secret= environ.get('CONSUMER_SECRET')
    access_token= environ.get('ACCESS_TOKEN')
    access_token_secret= environ.get('ACCESS_SECRET')

    #Authentication 
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    return api

def Tweets(keywords):
    api = Auth()

    #Define the search
    search_words = (keywords).encode('utf-8')
    date_since = "2019-06-01"

    #Collect tweets
    tweets = tw.Cursor(api.search, q=search_words, lang="es", since=date_since).items(int(environ.get('DEVELOPMENT_TWEETS_COUNT')))

    #Iterates on tweet
    users_locs = [[tweet.user.screen_name, tweet.text.encode('utf-8'), tweet.user.location , tweet.created_at] for tweet in tweets]

    #Create panda dataframe
    tweet_df = pd.DataFrame(data=users_locs, columns = ['user', 'tweet', 'location', 'date'])
    words_freq, perception = Summary(keywords, tweet_df)
    tw_summary = {
        'words_freq': words_freq,
        'perception': perception,
    }
    #tw_summary = json.dumps(tw_summary)
    return tw_summary
