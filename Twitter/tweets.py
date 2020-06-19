# -*- coding: utf-8 -*-
import tweepy as tw
import pandas as pd
from Twitter.data_management import Summary

def Auth():
    #API keys
    consumer_key= 'ZkaLWawtOntqbTgtcPHlKrO1j'
    consumer_secret= 'vVzxBCkKRY3iNCASZnbxwAyXMgISI9doZmYS8M8DUcRl7wVZCh'
    access_token= '1017240891197657094-D5l0VSWNeRBIRamwNIsioY2JMuz8oJ'
    access_token_secret= 'UXRPR0iwIlpw0QQFStvP4sNu40Gmu6C6OSwlFaO8dUjIU'

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
    tweets = tw.Cursor(api.search, q=search_words, lang="es", since=date_since).items(50)

    #Iterates on tweet
    users_locs = [[tweet.user.screen_name, tweet.text.encode('utf-8'), tweet.user.location , tweet.created_at] for tweet in tweets]

    #Create panda dataframe
    tweet_df = pd.DataFrame(data=users_locs, columns = ['user', 'tweet', 'location', 'date'])
    Summary(keywords, tweet_df)

    tweet_json = tweet_df.T.to_dict('list')

    return tweet_json
