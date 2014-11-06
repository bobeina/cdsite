# -*- coding:UTF-8 -*-
from django.shortcuts import render

# Create your views here.
from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^changepwd/$', views.changepwd, name='changepwd'),
    url(r'^register/$', views.register, name='register'),
)
