# -*- coding:UTF-8 -*-
from django.shortcuts import render

# Create your views here.
from django.conf.urls import patterns, url

from cthulhudice import views

urlpatterns = patterns('',
    url(r'^$', views.loadpage, name='loadpage'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^chat/(\w+)$', views.chatDelete, name='chatDelete'),
    url(r'^createGame/$', views.createGame, name='createGame'),
)
