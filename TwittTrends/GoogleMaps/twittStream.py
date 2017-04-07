import tweepy
import sys
import json
import uuid
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from getpass import getpass
from boto.sqs.message import RawMessage

# Set up Credentials
auth = tweepy.OAuthHandler('hHWm4pObqEpvLJgUjBmCGSz7v', '6UdRDTyT6Y53NX4X6ujGQ5oukynk9mQsB7pKRMF3UO58rhX3RJ')
auth.set_access_token('1624510022-aN1hkutTH5C3Wg7Jo2dCs9GHnbogNErlirLzT3a', 'PPzLsCyNeglF4Dkg5kWn4yQdMhmafhWrlBlAYUTG2HyBy')

class MyStreamListener(tweepy.StreamListener):
    AWSKey = "{redacted}"
    AWSSecret = "{redacted}"
    def addToQueue(tweet):
        data = {
            'submitdate' : time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            'key' : str(uuid.uuid1()),
            'message' : str(tweet)
        }
        sqs = boto.connect_sqs(AWSKey, AWSSecret)
        queue = sqs.create_queue("TwittTrends")
        message = RawMessage()
        message.set_body(json.dumps(data))
        status = queue.write(message)

    def on_data(self, streamingData):
        try:
        	data = json.loads(streamingData)
        	# Only add tweets to elastic search with coordinates
        	coords = data['place']['bounding_box']['coordinates']
	        if coords is not None:
	        	# Note that twitter puts longitude first, then latitude
	        	# Mutliple coordinates given, I pick the first coordinate, as this is relatively accurate
	        	lon = coords[0][0][0]
	        	lat = coords[0][0][1]
	        	tweet = {
	                'coordinates': {'lat': lat, 'lon': lon},
	                'text': data['text']
	        	}
	        	print(tweet)
	        	# Insert data into elastic search
	        	response = requests.post('http://search-twitter-map-obukguehsa2d4it32tto6i3vbm.us-east-1.es.amazonaws.com/twitter/tweets', json=tweet)
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
