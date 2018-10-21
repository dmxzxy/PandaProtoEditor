from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project/create/$', views.project_create, name='project_create'),
    url(r'^project/create/branche/$', views.project_create_branche, name='project_create_branche'),
    url(r'^project/branche/(?P<branche_id>[0-9]+)/$', views.branche_detail, name='branche_detail'),
    url(r'^project/branche/help/(?P<branche_id>[0-9]+)/$', views.branche_help, name='branche_help'),

    url(r'^project/branche/export/(?P<branche_id>[0-9]+)/$', views.branche_export, name='branche_export'),
    url(r'^project/branche/sync/(?P<branche_id>[0-9]+)/$', views.branche_sync, name='branche_sync'),
 
    url(r'^protocal/$', views.index, name='protocal_detail_parent'),
    url(r'^protocal/(?P<protocal_id>[0-9]+)$', views.protocal_detail, name='protocal_detail'),
    
    url(r'^module/(?P<module_id>[0-9]+)$', views.module_detail, name='module_detail'),
]