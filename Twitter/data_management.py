import pandas as pd
import numpy as np

def Summary(keywords, tweets_df):
    # Creating a new column in pandas
    sLength = len(tweets_df['tweet'])
    tweets_df['cleaning_tweets'] = pd.Series(np.random.randn(sLength), index=tweets_df.index)

    #Cleaning tweets text
    for key, value in enumerate(tweets_df['tweet']):
        value = value.lower().decode('utf8')
        tweets_df['cleaning_tweets'][key] = value
    
    WordsFrequencies(keywords, tweets_df)

def WordsFrequencies(keywords, tweets_df):
    prepositions = ['a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'en', 'entre', 
                    'hacia', 'hasta', 'para', 'por', 'pro', 'según', 'sin', 'sobre', 'tras']
    words = ''
    for key, value in enumerate(tweets_df['cleaning_tweets']):
        words += value
    
    # Deleting @ character
    words = words.translate({ord(i): None for i in '@'})
    
    # Converting String into list
    wordlist = words.split()
    for index, word in enumerate(wordlist):
        if(word in prepositions):
            wordlist[index] = ''
    wordlist = [value for value in wordlist if(value != '')]

    wordfreq = []

    # Creating frequencies array of words
    for words in wordlist:
        wordfreq.append(wordlist.count(words))
    
    # Creating a new df with the word frequencies
    wordfreq_df = pd.DataFrame({'words': wordlist, 'frequency': wordfreq})

    # Sorting words by frequency
    wordfreq_df.sort_values(by=['frequency'], inplace=True, ascending=False)
    wordfreq_df.drop_duplicates(subset=['words', 'frequency'], keep='first', inplace=True)
    wordfreq_df.reset_index(drop=True, inplace=True)
    print(wordfreq_df.head(10))








