from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project/create/$', views.project_create, name='project_create'),
    url(r'^project/create/branch/$', views.project_create_branch, name='project_create_branch'),
    url(r'^project/branch/(?P<branch_id>[0-9]+)/$', views.branch_detail, name='branch_detail'),
    url(r'^project/branch/help/(?P<branch_id>[0-9]+)/$', views.branch_help, name='branch_help'),

    url(r'^project/branch/export/(?P<branch_id>[0-9]+)/$', views.branch_export, name='branch_export'),
    url(r'^project/branch/sync/(?P<branch_id>[0-9]+)/$', views.branch_sync, name='branch_sync'),
 
    url(r'^protocol/$', views.index, name='protocol_detail_parent'),
    url(r'^protocol/(?P<protocol_key>.*)$', views.protocol_detail, name='protocol_detail'),
    
    url(r'^message/$', views.index, name='message_detail_parent'),
    url(r'^message/(?P<message_key>.*)$', views.message_detail, name='message_detail'),

    url(r'^enum/$', views.index, name='enum_detail_parent'),
    url(r'^enum/(?P<enum_key>.*)$', views.enum_detail, name='enum_detail'),
    
    url(r'^module/(?P<module_id>[0-9]+)$', views.module_detail, name='module_detail'),
]