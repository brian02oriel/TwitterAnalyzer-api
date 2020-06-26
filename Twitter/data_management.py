import re
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
        tweets_df.loc[key, 'cleaning_tweets']= value
    
    words_freq = WordsFrequencies(keywords, tweets_df['cleaning_tweets'])
    
    perception = PerceptionAnalysis(tweets_df['cleaning_tweets'])

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

def PerceptionAnalysis(tweets):
    tw_perception = []
    absolute_negative = ['verga', 'pinga', 'chucha', 'fck', 'fucking', 'hdp', 'puta']
    very_negative = ['horrible', 'terrible', 'horribles', 'terribles','detesto', 'detesta', 'odio', 'odia', 
                    'aborrezco', 'pésimo', 'harta', 'harto']
    negative = ['tóxica', 'tóxico', 'malo', 'mala', 'malos', 'malas','no', 'negativo', 'feo', 'fea', 'feos', 'feas',
                 'preocupa', 'preocupo', 'preocupado', 'preocupada']
    positive = ['gusta', 'gustó', 'bueno', 'buena', 'buenos', 'buenas','sí', 'positivo', 'positivos',
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

    for value in tweets:
        value = deEmojify(value)
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
    #print(tw_perception_df)

    positive_count = 0
    negative_count  = 0
    neutral_count = 0
    general_perception = 0
    for value in tw_perception_df['total']:
        if(value > 0):
            positive_count += 1
        elif(value < 0):
            negative_count += 1
        else:
            neutral_count += 1
        general_perception += value
    general_perception = round(general_perception/len(tw_perception_df['total']), 2)
    #print('positive: {0} | negative: {1} | neutral: {2} | general perception: {3}'.format(positive_count, negative_count, neutral_count, general_perception))
    perception_summary = {
        'positive': positive_count,
        'negative': negative_count,
        'neutral': neutral_count,
        'general_perception': general_perception
    }
    return perception_summary


        

    


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)









