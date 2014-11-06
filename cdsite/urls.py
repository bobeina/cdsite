from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cdsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'home.views.index', name='index'),
    url(r'^home/', include('home.urls')),
    url(r'^register/', 'home.views.register', name='register'),
    url(r'^cthulhudice/', include('cthulhudice.urls')),
    url(r'^news/', include('news.urls')),
    
    #my auth
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),

)
