import pandas as pd
import numpy as np
from nltk.corpus import stopwords

def Summary(keywords, tweets_df):
    # Creating a new column in pandas
    sLength = len(tweets_df['tweet'])
    tweets_df['cleaning_tweets'] = pd.Series(np.random.randn(sLength), index=tweets_df.index)

    #Cleaning tweets text
    for key, value in enumerate(tweets_df['tweet']):
        value = value.lower().decode('utf8')
        tweets_df['cleaning_tweets'][key] = value
    
    words_freq = WordsFrequencies(tweets_df['cleaning_tweets'])
    
    SentimentalAnalysis(tweets_df['cleaning_tweets'])

def WordsFrequencies(tweets):
    prepositions = ['a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'en', 'entre', 
                    'hacia', 'hasta', 'para', 'por', 'pro', 'según', 'sin', 'sobre', 'tras']
    symbols = ['¿', '?', '!', '¡', '“', '”', ':', ';', ',']
    words = ''
    for key, value in enumerate(tweets):
        words += value
    
    # Deleting special characters
    words = words.translate({ord(i): None for i in symbols})

    # Converting String into list
    wordlist = words.split()

    # Deleting prepositions
    for index, word in enumerate(wordlist):
        if(word in prepositions or word in stopwords.words('spanish')):
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
    return wordfreq_df.head(20)

def SentimentalAnalysis(tweets):
    tw_perception = []
    absolute_negative = ['verga', 'pinga', 'chucha', 'fck', 'fucking']
    very_negative = ['horrible', 'terrible', 'horribles', 'terribles','detesto', 'detesta', 'odio', 'odia', 
                    'aborrezco', 'pésimo', 'harta', 'harto']
    negative = ['tóxica', 'tóxico', 'malo', 'mala', 'malos', 'malas','no', 'negativo', 'feo', 'fea', 'feos', 'feas',
                 'preocupa', 'preocupo', 'preocupado', 'preocupada']
    positive = ['bueno', 'buena', 'buenos', 'buenas','sí', 'positivo', 'positivos',
                 'bonito', 'bonita', 'bonitos', 'bonitas','lindo', 'linda' ,'lindos', 'lindas']
    very_positive = ['excelente', 'excelentes','destacado', 'destacada', 'destacados', 'destacadas',
                'alucinante', 'alucinantes','precioso', 'preciosa','preciosos', 'preciosas',
                'bello', 'bella', 'bellos', 'bellas','hermoso', 'hermosa', 'hermosos', 'hermosas',
                'asombroso', 'asombrosa', 'asombrosos', 'asombrosas','impresionante','impresionantes']
    multipliers = ['mucho', 'mucha', 'muchos', 'muchas','bastante', 'bastantes','abundante', 'abundantes',
                    'enorme', 'enormes','gigante','gigantes', 'todo', 'toda', 'todos', 'todas']
    dividers = ['poco', 'poca', 'pocos', 'pocas', 'pequeño', 'pequeña', 'pequeños', 'pequeñas', 'chico', 'chica',
                'chicos', 'chicas', 'mínimo', 'mínima', 'mínimos', 'mínimas', 'escazo', 'escaza', 'escazos', 'escazas']
    absolute_negative_pts = -3
    very_negative_pts = -2
    negative_pts = -1
    neutral_pts = 0
    positive_pts = 1
    very_positive_pts = 2
    multiplier_pts = 2
    divider_pts = 2

    for key, value in enumerate(tweets):
        tokens = value.split()
        tw_perception.append({
            'tokens': tokens,
            'len': len(tokens),
            'pts': 0,
            'multiplier': 1,
            'divider': 1,
            'total': 0
        })
    for tokens in tw_perception:
        pts = 0
        multi = 0
        div = 0
        for text in tokens['tokens']:
            if(text in absolute_negative):
                pts += absolute_negative_pts
            elif(text in very_negative):
                pts += very_negative_pts
            elif(text in negative):
                pts += negative_pts
            elif(text in positive):
                pts += positive_pts
            elif(text in very_positive):
                pts += very_positive_pts
            elif(text in multipliers):
                multi += multiplier_pts
                tokens['multiplier'] = multi
            elif(text in dividers):
                div += divider_pts
                tokens['divider'] = div
            else:
                pts += neutral_pts
            
            tokens['pts'] = pts
            
        tokens['total'] = round((tokens['multiplier'] * tokens['pts']) / (tokens['divider'] * tokens['len']), 2)
    tw_perception_df = pd.DataFrame(data=tw_perception)
    print(tw_perception_df)










