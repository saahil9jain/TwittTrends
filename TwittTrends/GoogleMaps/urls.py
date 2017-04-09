#GoogleMaps/urls.py
from django.conf.urls import url
from GoogleMaps import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'^post/$', views.post, name='post'),
		url(r'^snspoll/$', views.snspoll, name='snspoll')
]
