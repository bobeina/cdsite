# -*-coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from news.models import Post

def index(request):
    posts = Post.objects.filter(published=True)
    return render(request,'news/index.html',{'posts': posts})

def post(request, slug):
    post = get_object_or_404(Post,slug=slug)
    return render(request,'news/post.html',{'post': post})
