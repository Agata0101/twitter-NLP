# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 07:28:20 2018

@author: Agata
"""
"""

this code:
    - analises the sentiment using two libraries Vader and TextBlob
    
    - comapres the results and presents them visulaly

"""

# Import the libraries

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

import pandas as pd
import numpy as np
from unidecode import unidecode


fname = 'tweets.json'

# read the json file with saved tweets and store the date and the sentiment calculated by both libraries
with open(fname, 'r') as f:
    all_dates = []
    vader_sentiment = []
    textblob_sentiment = []
    count = 0
    for line in f:
        count+=1
        if count % 2 != 0: 
            data = json.loads(line) 
            tweet = unidecode(data['text'])
        all_dates.append(data.get('created_at'))
        vader_sentiment.append(SentimentIntensityAnalyzer().polarity_scores(tweet)['compound'])
        textblob_sentiment.append(TextBlob(tweet).sentiment.polarity)
    idx = pd.DatetimeIndex(all_dates)
    # 
    vader = pd.Series(vader_sentiment, index=idx)
    text_blob = pd.Series(textblob_sentiment, index=idx)


#### CHANGE OF THE SENTIMENT IN TIME
#fig, ax = plt.subplots()
fig = plt.figure(1, figsize=(14,9))
ax = fig.add_subplot(1, 1, 1)
ax.grid(True)
ax.set_title("Textblob", fontsize=16, fontweight=500)

hours = mdates.MinuteLocator(interval=20)
date_formatter = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(date_formatter)
ax.plot(text_blob.index, text_blob, 'o')

#plt.savefig('tweet_time_series.jpg')

### DESCRIPTIVE STATISTICS AND HISTOGRAMS
#textblob

def stats(data, name):
    '''
    this function generates descriptive statistics and histograms
    '''
    print(data.dexcribe())
    # seaborn histogram
    sns.distplot(data, hist=True, kde=False, 
                 bins=int(2/0.05), color = 'blue',
                 hist_kws={'edgecolor':'black'})
    # Add labels
    plt.title('Distribution of sentiment using ', name)
    plt.xlabel('Measure of sentiment')
    plt.ylabel('Count')

#generate histograms and stats
stats(text_blob, "Textblob")
stats(vader, "Vader")


def sentiment(x):
    '''
    this function assigns the sentiment based on a score
    '''
    if x<0.05 and x>-0.05:
        return 'neutral'
    elif x>=0.05:
        return 'positive'
    else:
        return 'negative'
    
   
df['v_rating']=df['v_score'].map(sentiment)
df['tb_rating']=df['tb_score'].map(sentiment)

sns.set(font_scale=1.5)
sns.countplot(df['v_rating'], order = ['positive',  'negative', 'neutral']).set_title("VADER Sentiment")
sns.countplot(df['tb_rating'], order = ['positive',  'negative', 'neutral']).set_title("TextBlob Sentiment")

### Analysis of the differences in distributions
#positive sentiment
df['v_score'].plot(kind="density",
                      xlim= (0.05,1),  ylim= (0,2.4), label='Vader')
sns.distplot(df['tb_score'], hist = False, kde = True,
                 kde_kws = {'shade': False, 'linewidth': 2},label='TextBlob' 
                  )
plt.title('Analysis of the differences in distributions for positive sentiment')
plt.xlabel('Sentiment score')
plt.ylabel('')


