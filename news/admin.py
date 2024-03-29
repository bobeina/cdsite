# -*-coding:utf-8 -*-
from django.contrib import admin
from news.models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','description']
    list_filter = ['published','created']
    search_fields = ['title','description','content']
    date_hierarchy = 'created'
    save_on_top = True
    prepopulated_fields = {"slug":("title",)}

admin.site.register(Post,PostAdmin)

