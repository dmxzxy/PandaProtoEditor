from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project/create/$', views.project_create, name='project_create'),
    url(r'^project/create/branche/$', views.project_create_branche, name='project_create_branche'),
    url(r'^project/(?P<project_id>[0-9]+)/$', views.project_detail, name='project_detail'),
]