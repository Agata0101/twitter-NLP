# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 07:38:10 2018

@author: Agata

"""
"""
This code present different ways to vectorise data. Namely:
    - bag of words
    - bag of words with constrains
    - TF-IDF
    - N grams
    - Word-2-Vec representation
    
The code also contains a short analysis of each of those methods    
"""


import string
import json

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import emoji1
import re
import unicodedata
import contractions
import inflect
from nltk.stem import LancasterStemmer, WordNetLemmatizer

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#######  BAG OF WORDS
                
#define the parameters
tweet_tokenizer = TweetTokenizer()
punct = list(string.punctuation)
more_emoji=[]
stopword_list = stopwords.words('english') + more_emoji +punct

### initialisation
vect=CountVectorizer(tokenizer=tweet_tokenizer.tokenize, stop_words=stopword_list, lowercase=True)
### fit=> tokenize+bulid a dictionary
vect.fit(corpus)
### transform => create a bag of words represantation
R1=vect.transform(corpus)

##### Initial analysis of the words extracted from the tweets

# Display the number of words
print("Number of words: {}".format(len(vect.vocabulary_)))
#create the list of all the words
slowa=vect.get_feature_names()
#display first 50 words
print("First 50 of words: {}".format(slowa[:50]))

# Materialize the sparse data
data_dense = R1.todense()

# Compute Sparsicity = Percentage of Non-Zero cells
print("Sparsicity: ", ((data_dense > 0).sum()/data_dense.size)*100, "%")
del data_dense


######  LIMITED BAG OF WORDS

#create a bag of words represantation with 1000 most common words
### initialisation
vect=CountVectorizer(tokenizer=tweet_tokenizer.tokenize, stop_words=stopword_list, lowercase=True, max_features=1000, max_df=.15)
### fit=> tokenize+bulid a dictionary
vect.fit(corpus)
### transform => create a bag of words represantation
R2=vect.transform(corpus)


# Number of words
print("Number of words: {}".format(len(vect.vocabulary_)))
#list of all the words
slowa=vect.get_feature_names()
print("First 50 words: {}".format(slowa[:50]))


#######  TF-IDF

from sklearn.feature_extraction.text import TfidfVectorizer
vect2=TfidfVectorizer(tokenizer=tweet_tokenizer.tokenize, stop_words=stopword_list, lowercase=True)
#fit
fitted=vect2.fit(corpus)
#transform
R3 = fitted.transform(corpus)


#tfidf max values
# find maximum value for each of the features over all of dataset:
max_val = R3.max(axis=0).toarray().ravel()
#sort weights from smallest to biggest and extract their indices 
sort_by_tfidf = max_val.argsort()
#features names
feature_names = np.array(fitted.get_feature_names())

#analysis of the frequency
print("Words with the lowest tfidf:\n{}".format(
      feature_names[sort_by_tfidf[:100]]))

print("\nWords with the highest tfidf: \n{}".format(
      feature_names[sort_by_tfidf[-100:]]))


####### N GRAMS

vect1=CountVectorizer(tokenizer=tweet_tokenizer.tokenize, stop_words=stopword_list, lowercase=True, ngram_range=(1,2))
vect1.fit(corpus)
print("Size of the dictionary: {}".format(len(vect1.vocabulary_)))

R4=vect.transform(corpus)


###### WORD2VEC
# build vocabulary and train model
model = Word2Vec(tweets_list,size=100,window=5,min_count=2,workers=10)
model.train(tweets_list, total_examples=len(tweets_list), epochs=10)

# check the results 
# I choose some sample words and check what words are located close to them in the sample sapce
w="bitcoin"
model.wv.most_similar(positive=w)

w="ai"
model.wv.most_similar(positive=w)

w="bigdata"
model.wv.most_similar(positive=w)

w="cryptocurrency"
model.wv.most_similar(positive=w)
