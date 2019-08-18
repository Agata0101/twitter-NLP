# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 08:05:08 2018

@author: Agata
"""

"""
time seris analysis of tweets

This code calculates how many tweets have been published per minute and then display this information on a graph

This analysis aims to show how interest in a subject veries in time
"""

import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
import numpy as np
import pickle


fname = 'tweets3.json'

with open(fname, 'r') as f:
    #create a list with all the dates/times when the tweets were published
    all_dates = []
    count = 0
    for line in f:
        count+=1
        if count % 2 != 0: 
            tweet = json.loads(line) 
        all_dates.append(tweet.get('created_at'))
    ones = np.ones(len(all_dates))
    idx = pd.DatetimeIndex(all_dates)
    # the actual series 
    my_series = pd.Series(ones, index=idx)

    # Resampling / bucketing into 1-minute buckets
    per_minute = my_series.resample('1Min', how='sum').fillna(0)
    print(my_series.head())
    print(per_minute.head())
    
#fig, ax = plt.subplots()
fig = plt.figure(1, figsize=(14,9))
ax = fig.add_subplot(1, 1, 1)
ax.grid(True)
ax.set_title("Tweets frequency", fontsize=16, fontweight=500)

hours = mdates.MinuteLocator(interval=20)
date_formatter = mdates.DateFormatter('%H:%M')



ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(date_formatter)
#datemin = datetime(2015, 10, 31, 15, 0)
#datemax = datetime(2015, 10, 31, 18, 0)
#ax.set_xlim(datemin, datemax)
max_freq = per_minute.max()
ax.set_ylim(0, max_freq)
ax.plot(per_minute.index, per_minute)

#save the plot
plt.savefig('tweet_time_series.jpg')

