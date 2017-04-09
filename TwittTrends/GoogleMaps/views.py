#!/usr/bin/python
# -*- coding: utf-8 -*-
# GoogleMaps/views.py

from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from urllib.request import urlopen


def index(request):
    return render(request, 'index.html')


def post(Request):
    if Request.method == 'POST':
        msg = Request.POST.get('Search', None)
    if Request.method == 'GET':
        msg = Request.GET.get('Search', None)
    elastic = 'http://search-twitter-map-obukguehsa2d4it32tto6i3vbm.us-east-1.es.amazonaws.com/twittertrend/_search?q='
    response = requests.get(elastic + msg + '&size=100')
    json_response = json.loads(response.text)
    tweet = []
    coordinates = []
    sentiments = []
    for resp in json_response['hits']['hits']:
        tweet.append(resp['_source']['tweet'])
        coordinates.append(resp['_source']['coordinates'])
        sentiments.append(resp['_source']['sentiment'])
    data = {'coordinates': coordinates, 'tweets': tweet,
            'sentiments': sentiments}
    print (data)
    return JsonResponse(data)


@csrf_exempt
def snspoll(request):
    context = {'message': 'confirmation'}
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        body_unicode = request.body.decode('utf-8')
        header = json.loads(body_unicode)
        if header['Type']=="SubscriptionConfirmation":
            subscribleURL=header['SubscribeURL']
            urlopen(subscribleURL).read()
        elif header['Type'] == 'Notification':
            message = json.loads(json.loads(header['Message']).get('default'))
            tweet = message['tweet']
            lat = message['coordinates']['lat']
            lon = message['coordinates']['lon']
            sentiment = message['sentiment']

            tweet_data = {'tweet': tweet, 'coordinates': {'lat': lat,
                          'lon': lon}, 'sentiment': sentiment}
            requests.post('http://search-twitter-map-obukguehsa2d4it32tto6i3vbm.us-east-1.es.amazonaws.com/twittertrend/tweets', json=tweet_data)
            print(requests.status)
            context = {'message': 'notification'}
    return render(request, 'index.html', context)
