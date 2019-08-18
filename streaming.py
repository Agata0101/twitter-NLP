# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:21:25 2018

@author: Agata

"""

"""
this code:
    - connects to Twitter API
    - streams tweets containing specified key words in real time
    - saves the text of the tweet into the json file
"""



### CHANGING DIRECTORY
# where the file with downloaded tweets will be saved
import os
path="C:\\Users\\Agata\\Desktop\\big_data\\twitter"
os.chdir(path)
###

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json

import credentials


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Streaming of the tweets
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # authentification
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # filtering: 
        stream.filter(track=hash_tag_list, languages=["en"])


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    A listener handles tweets that are received from the stream.

    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # what to do with the tweets
    def on_data(self, data):
        # write the tweets to the specified json file
        # if an exception (small network disruptions)
        # then display the error and wait 5 sec before resuming the streaming
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
            time.sleep(5)
        return True
          
    def on_status(self, status):
        #don't save retweeted tweets
        if status.retweeted:
            return
    # error handler
    def on_error(self, status):
        # Error 420 is being sent if we exceed Twitter’s rate limit 
        # this error will be coming back and slowing down the streeaming
        if status == 420:
            print("rate limit exceeded")
            return False
        # in case of any other error, print it and continue streaming
        print(status)
        return True

 
if __name__ == '__main__':
 
    # downlad the tweets containing the following key words
    hash_tag_list = ["#bitcoin", "#blockchain","#cryptocurrency"]
    # specify the file to save the tweets
    fetched_tweets_filename = "tweets3.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
