import tweepy
import sys
import json
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from getpass import getpass
import boto.sqs
from boto.sqs.message import Message

# Set up Credentials for Twitter API
auth = tweepy.OAuthHandler('hHWm4pObqEpvLJgUjBmCGSz7v', '6UdRDTyT6Y53NX4X6ujGQ5oukynk9mQsB7pKRMF3UO58rhX3RJ')
auth.set_access_token('1624510022-aN1hkutTH5C3Wg7Jo2dCs9GHnbogNErlirLzT3a', 'PPzLsCyNeglF4Dkg5kWn4yQdMhmafhWrlBlAYUTG2HyBy')

# Get queue
conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='AKIAJ2SBRP7FL2443UCA', aws_secret_access_key='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')
queue = conn.create_queue('TwittTrends')

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, streamingData):
        try:
        	data = json.loads(streamingData)
        	# Only add tweets with geolocation info and in English
        	coords = data['place']['bounding_box']['coordinates']
        	language = data["lang"]
	        if (coords is not None) and (language == "en"):
	        	# Note that twitter puts longitude first, then latitude
	        	# Mutliple coordinates given, I pick the first coordinate, as this is relatively accurate
	        	lon = coords[0][0][0]
	        	lat = coords[0][0][1]
	        	tweet = {
	                'coordinates': {'lat': lat, 'lon': lon},
	                'text': data['text']
	        	}
	        	print(tweet)
	        	message = Message()
	        	message.set_body(json.dumps(tweet))
	        	queue.write(message)

	        	# Insert data into elastic search
	        	# response = requests.post('http://search-twitter-map-obukguehsa2d4it32tto6i3vbm.us-east-1.es.amazonaws.com/twitter/tweets', json=tweet)
        except:
        	pass
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
	api = tweepy.API(auth)
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	myStream.filter(track=['and', 'yes', 'politics', 'Florida', 'Donald', 'Trump', 'Obama', 'Clinton', 'Carson', 'Obamacare', 'India', 'USA', 'lol', 'sad', 'angry', 'love', 'hate', 'happy', 'mad', 'fear', 'trust', 'joy', 'jealous', 'fun'])