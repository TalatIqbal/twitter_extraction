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


def get_tweets(api, search_string, count, lang='en'):
    fetched_tweets = api.search(search_string, count=count, lang=lang)
    return fetched_tweets

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


	OP_DIR = '../data/output/'
	# search_string = 'covid'
	tweet_count = 100 # Max per request - set by twitter
	max_requests = 180 # Max requests - Set by twitter
	time_interval = 15 # Interval (mins) to wait - Set by twitter

	request_count = 0

	while True:
	    now = datetime.datetime.now()
	    str_time = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' \
	                + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second)
	    op_file = OP_DIR + 'tweets_' + str(str_time) + '_' + str(request_count) + '.tweet'

	    with open(op_file, 'w') as fp:
	        
	        fetched_tweets = get_tweets(api, search_string, tweet_count)
	        request_count += 1
	        
	        print('Request Count:', request_count, 'last', len(fetched_tweets),\
	              'tweets retrieved at', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end='\r')
	        
	        for tweet in fetched_tweets:
	            result = json.dumps(tweet._json)
	            fp.write(result + '\n')


def main():
	search_string = 'covid'
	extract_by_keyword(search_string)


if __name__ == '__main__':
    main()