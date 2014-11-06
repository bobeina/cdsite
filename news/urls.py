# -*- coding:UTF-8 -*-
from django.shortcuts import render

# Create your views here.
from django.conf.urls import patterns, url

from news import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[\w\-]+)/$','news.views.post'),
    #url(r'^post/$', views.post, name='post'),
)
