import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json
import pandas as pd
import csv
import re #regular expression
import string
import datetime
import numpy as np
import math
import json
import time


# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        
        print(status.id_str)
            
        OP_DIR = '../data/stream/'
        op_file = OP_DIR + 'tweets_' + str(status.id_str) + '.stream'

        with open(op_file, 'w', encoding='utf-8') as fp:
            result = json.dumps(status._json)
            fp.write(result + '\n')            

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

def extract_by_keyword(search_string):


	# Retrieve Credentials
	oauth_file = '../auth/oauth.txt'
	keys = []
	line = 'a'
	with open(oauth_file) as fp:
	    while line:
	        line = fp.readline().strip()
	        keys.append(line)

	#Twitter credentials for the app
	consumer_key = keys[2]
	consumer_secret = keys[3]
	access_key = keys[0]
	access_secret = keys[1]

	#pass twitter credentials to tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


	streamListener = StreamListener()
	stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
	with open("../data/out.csv", "w", encoding='utf-8') as f:
	    f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
	tags = ['corona', 'covid', 'virus', 'flu']
	stream.filter(track=tags, languages=['en'])


def main():
	search_string = 'corona'
	extract_by_keyword(search_string)


if __name__ == '__main__':
    main()