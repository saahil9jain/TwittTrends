#GoogleMaps/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse
from django.core import serializers
import requests
import json

def index(request):
	return render(request, 'index.html')

def post(Request):
	if Request.method == "POST":
	    msg = Request.POST.get('Search', None)
	elastic = 'http://search-twitter-map-obukguehsa2d4it32tto6i3vbm.us-east-1.es.amazonaws.com/twitter/_search?q='
	response = requests.get(elastic+msg+"&size=100")
	json_response = json.loads(response.text)
	tweet = []
	coordinates = []
	for resp in json_response['hits']['hits']:
	    tweet.append(resp['_source']['text'])
	    coordinates.append(resp['_source']['coordinates'])
	data = {'coordinates': coordinates, 'tweets': tweet}
	print(data)
	return JsonResponse(data)

def snspoll(request):
	context={"message":"confirmation"}
    if request.method=="GET":
        return render(request,'index.html')
    else:
        header=json.loads(request.body)
        if header['Type']=="SubscriptionConfirmation":
            subscribleURL=header['SubscribeURL']
            urllib2.urlopen(subscribleURL).read()
        elif header['Type']=="Notification":
            message=json.loads(json.loads(header["Message"]).get('default'))
            tweet=message['tweet']
            lat=message['lat']
            lon=message['lon']
            sentiment=message['sentiment']['type']

            tweet_data={
                "tweet":tweet,
                "coordinates":{"lat":lat,"lon":lon},
                "sentiment":sentiment
            }
            requests.post(ELASTICSEARCHCLUSTER_LINK,json=tweet_data)
            context={"message": "notification"}
    return render(request,'index.html',context)
