# -*- coding:UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

#--------------------------------------------
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.context import RequestContext  
  
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  

from bootstrap_toolkit.widgets import BootstrapUneditableInput  
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from forms import ChangepwdForm

#############################################


# Create your views here.
@csrf_protect

def login(request):
    if request.user.is_authenticated() or request.user.username:
        return HttpResponseRedirect('/')
    
        
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username == '' and password == '':
        context = {'error_message':''}
        return render(request,'registration/login.html',context)

    if username == '' or password == '':
        context = {'error_message':u'用户名/密码不能为空！'}
        return render(request,'registration/login.html',context)
        
    user = auth.authenticate(username=username, password=password)
    context = {'error_message': u'用户名/密码错误！'}
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect('/')
    else:
        #   ##Show an error page
        # Redirect to login page
        return render(request,'/registration/login.html',context)

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return render(request,'home/index.html')

#@login_required
def index(request):
    grp = ''
    if request.user.is_authenticated() :
        info = request.user.username 
        if not info:
            context = {'userinfo':u'你尚未登录！' }
        else:
            context = {'userinfo':info }

        return render(request,'home/index.html',context)
    else:
        context = {'error_message':''}
        return render(request,'home/index.html',context)

#=================================================================
@login_required  
def changepwd(request):  
    if request.method == 'GET':  
        form = ChangepwdForm()  
        return render_to_response('home/changepwd.html', RequestContext(request, {'form': form,}))  
    else:  
        form = ChangepwdForm(request.POST)  
        if form.is_valid():  
            username = request.user.username  
            oldpassword = request.POST.get('oldpassword', '')  
            user = auth.authenticate(username=username, password=oldpassword)  
            if user is not None and user.is_active:  
                newpassword = request.POST.get('newpassword1', '')  
                user.set_password(newpassword)  
                user.save()  
                return render_to_response('home/index.html', RequestContext(request,{'changepwd_success':True}))  
            else:  
                return render_to_response('home/changepwd.html', RequestContext(request, {'form': form,'oldpassword_is_wrong':True}))  
        else:  
            return render_to_response('home/changepwd.html', RequestContext(request, {'form': form,}))  



#=================================================================
@csrf_protect
def register(request):
    if request.user.is_authenticated() :
        context = {'error_message':''}
        return render(request,'home/index.html',context)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request,"home/register.html", {
        'form': form,
    })
