import re
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import itertools
from joblib import dump, load


def Summary(keywords, tweets_df):
    # Creating a new column in pandas
    sLength = len(tweets_df['tweet'])
    tweets_df['clear_tweets'] = pd.Series(np.random.randn(sLength), index=tweets_df.index)

    #Cleaning tweets text
    for key, value in enumerate(tweets_df['tweet']):
        value = value.lower().decode('utf8')
        tweets_df.loc[key, 'clear_tweets']= value
    
    words_freq = WordsFrequencies(keywords, tweets_df['clear_tweets'])
    
    perception = PerceptionAnalysis(tweets_df)

    return words_freq, perception

def WordsFrequencies(keywords, tweets):
    prepositions = ['a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'en', 'entre', 
                    'hacia', 'hasta', 'para', 'por', 'pro', 'según', 'sin', 'sobre', 'tras']
    symbols = ['¿', '?', '!', '¡', '“', '”', '.',':', ';', ',', '|', '#', '-']
    words = ''
    for value in tweets:
        words += value
    
    # Deleting special characters
    words = words.translate({ord(i): None for i in symbols})

    # Converting String into list
    wordlist = words.split()

    # Deleting prepositions
    for index, word in enumerate(wordlist):
        if(word in prepositions or word in stopwords.words('spanish') or word in keywords):
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
    wordlist = list()
    for index in range(50):
        wordlist.append({
            'text': wordfreq_df['words'].iloc[index],
            'value': int(wordfreq_df['frequency'].iloc[index])
        })
    
    return wordlist

def PerceptionAnalysis(tweets_df):
    # Creating empty columns
    empty_column = np.empty([500, 1])
    empty_column[:] = np.zeros(1)
    # Creating empty array column
    empty_column_array = np.zeros(3)

    # Merging a temp Dataframe with the empty array column with the tweets Dataframe
    temp_df = pd.DataFrame({'tokens': [empty_column_array], 'scores': [empty_column_array]})
    tweets_df = pd.merge(tweets_df, temp_df, how='left', left_index=True, right_index=True)
    # Adding column with empty cells (0)
    tweets_df['length'] = empty_column
    tweets_df['absolutely_negative'] = empty_column
    tweets_df['very_negative'] = empty_column
    tweets_df['negative'] = empty_column
    tweets_df['neutral'] = empty_column
    tweets_df['positive'] = empty_column
    tweets_df['very_positive'] = empty_column
    tweets_df['perception'] = empty_column

    absolute_negative = ['verga', 'pinga', 'chucha', 'fck', 'fucking', 'hdp', 'puta', 'mierda']
    very_negative = ['horrible', 'terrible', 'horribles', 'terribles','detesto', 'detesta', 'odio', 'odia', 
                    'aborrezco', 'pésimo', 'harta', 'harto', 'hartas', 'hartos', 'enojarse', 'enojado', 'enojada', 'enojados', 'enojadas']
    negative = ['maliciosa', 'malicioso', 'maliciosas', 'maliciosos','tóxica', 'tóxico', 'malo', 'mala', 'malos', 'malas','no', 'negativo', 'feo', 'fea', 'feos', 'feas',
                'preocupa', 'preocupo', 'preocupado', 'preocupada']
    positive = ['bien', 'de acuerdo','gusta', 'gustó', 'bueno', 'buena', 'buenos', 'buenas','sí', 'positivo', 'positivos',
                'bonito', 'bonita', 'bonitos', 'bonitas','lindo', 'linda' ,'lindos', 'lindas']
    very_positive = ['romance', 'amor', 'mejor', 'feliz', 'excelente', 'excelentes','destacado', 'destacada', 'destacados', 'destacadas',
                'alucinante', 'alucinantes','precioso', 'preciosa','preciosos', 'preciosas',
                'bello', 'bella', 'bellos', 'bellas','hermoso', 'hermosa', 'hermosos', 'hermosas',
                'asombroso', 'asombrosa', 'asombrosos', 'asombrosas','impresionante','impresionantes', 'felicito', 'felicidades']

    absolute_negative_pts = -3
    very_negative_pts = -2
    negative_pts = -1
    neutral_pts = 0
    positive_pts = 1
    very_positive_pts = 2

    for key, value in enumerate(tweets_df['clear_tweets']):
        tweets_df['tokens'].iloc[key] = value.split()
        tweets_df['length'].iloc[key] = len(value)
    
    for key, value in enumerate(tweets_df['tokens']):
        scores = list()
        for text in value:
            if(any(text in sub for sub in absolute_negative)):
                scores.append(absolute_negative_pts)
            elif(any(text in sub for sub in very_negative)):
                scores.append(very_negative_pts)
            elif(any(text in sub for sub in negative)):
                scores.append(negative_pts)
            elif(any(text in sub for sub in positive)):
                scores.append(positive_pts)
            elif(any(text in sub for sub in very_positive)):
                scores.append(very_positive_pts)
            else:
                scores.append(neutral_pts)
        tweets_df['scores'].iloc[key] = np.array(scores)
    
    
    for key, value in enumerate(tweets_df['scores']):
        freqs = [i for i, j in itertools.groupby(value)]
        #print(freqs)
        for score in freqs:
            #(score, _ ) = freqs[index]
            if(score == -3):
                tweets_df['absolutely_negative'].iloc[key] += 1
            elif(score == -2):
                tweets_df['very_negative'].iloc[key] += 1
            elif(score == -1):
                tweets_df['negative'].iloc[key] += 1
            elif(score == 1):
                tweets_df['positive'].iloc[key] += 1
            elif(score == 2):
                tweets_df['very_positive'].iloc[key] += 1
            else:
                tweets_df['neutral'].iloc[key] += 1

    features = ['length', 'absolutely_negative', 'very_negative', 'negative', 'neutral', 'positive', 'very_positive']
    X = tweets_df[features]
    clf = load('Twitter/model.joblib')
    y = clf.predict(X)
    perception = ShowClass(y)
    perception_count = {'very_negative': 0,'negative': 0, 'neutral': 0, 'positive': 0, 'very_positive': 0}
    for value in perception:
        perception_count[value] += 1

    return perception_count


        
def ShowClass(prediction):    
    predicted_classes = list()
    classes = {-2: 'very_negative', -1: 'negative', 0: 'neutral', 1: 'positive', 2: 'very_positive'}
    for value in prediction:
        predicted_classes.append(classes[value])
    
    return predicted_classes
    


#def deEmojify(text):
#    regrex_pattern = re.compile(pattern = "["
#        u"\U0001F600-\U0001F64F"  # emoticons
#        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#        u"\U0001F680-\U0001F6FF"  # transport & map symbols
#        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                           "]+", flags = re.UNICODE)
#    return regrex_pattern.sub(r'',text)









