# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 07:38:10 2018

@author: Agata
"""

"""
This code prepares the data saved as a json file for further analysis. 
The text is cleaned, tokenized, stop words removed.

"""
import json
import string
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from gensim.models import Word2Vec
import re


def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
    '''
    this function will clean each tweet from:
        - stop words
        - emojis
        - html coding
        - links
        - digits
        - new line markers, #
        - UTF coding
     
    the text will be standardised to small letters
    
    the text will be tokenized
    
    Return: list of strings
    '''
    emoji_pattern = _EMOJI_REGEXP
    no_emoji=emoji_pattern.sub(r'', text)
    # html
    soup = BeautifulSoup(no_emoji, "html.parser")
    souped = soup.get_text()
    # links
    pat1 = r'@[A-Za-z0-9_]+'
    pat2 = r'https?://[A-Za-z0-9./]+'
    combined_pat = r'|'.join((pat1, pat2))
    stripped = re.sub(combined_pat, ' ', souped)
    # digits
    no_digits=re.sub(r'[0-9]', ' ', stripped)
    # small letter
    no_digits = no_digits.lower()
    # \n
    new_content = no_digits.replace('\n', ' ')
    # #
    new_content1 = new_content.replace('#', ' ')
    #usuwanie _
    #new_content2 = new_content1.replace('_', '')
    try:
        bom_removed = new_content1.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = new_content1  
    tokens = tokenizer.tokenize(bom_removed)
    return [tok for tok in tokens if tok not in stopwords and not tok.isdigit()]

if __name__ == '__main__':
    tweet_tokenizer = TweetTokenizer()
    punct = list(string.punctuation)
    stopword_list = stopwords.words('english') + punct + ['rt', 'via', '…', '’', '“', '...', '️', '‘']

    fname = 'tweets3.json'
    tweets_list=[]
    
    # in the json file every second line is populated
    # here the populated lines are read, processed and words are saved in a list
    with open(fname, 'r') as f:
        count = 0
        for line in f:
            count+=1
            if count % 2 != 0: 
                tweet = json.loads(line) 
                tokens = process(text=tweet.get('text', ''),
                                 tokenizer=tweet_tokenizer,
                                 stopwords=stopword_list)
                tweets_list.append(tokens)
###