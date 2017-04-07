#GoogleMaps/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from GoogleMaps.models import Tweets
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
	response = requests.get(elastic+msg)
	json_response = json.loads(response.text)
	tweet = []
	coordinates = []
	for resp in json_response['hits']['hits']:
	    tweet.append(resp['_source']['text'])
	    coordinates.append(resp['_source']['coordinates'])
	data = {'coordinates': coordinates, 'tweets': tweet}
	print(data)
	return JsonResponse(data)