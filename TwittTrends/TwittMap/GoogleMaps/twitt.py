import tweepy

# Streaming with Tweepy
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print(status.text)
	def on_error(self, status_code):
	    if status_code == 420:
	        #returning False in on_data disconnects the stream
	        return False

# Set up Credentials
auth = tweepy.OAuthHandler('hHWm4pObqEpvLJgUjBmCGSz7v', '6UdRDTyT6Y53NX4X6ujGQ5oukynk9mQsB7pKRMF3UO58rhX3RJ')
auth.set_access_token('1624510022-aN1hkutTH5C3Wg7Jo2dCs9GHnbogNErlirLzT3a', 'PPzLsCyNeglF4Dkg5kWn4yQdMhmafhWrlBlAYUTG2HyBy')

api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['politics', 'Donald', 'Trump', 'Obama', 'Clinton', 'Carson', 'Obamacare'])
