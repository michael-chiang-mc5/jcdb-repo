from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^addGroupInterface/$', views.addGroupInterface, name='addGroupInterface'),
    url(r'^addGroup/$', views.addGroup, name='addGroup'),
    url(r'^deleteGroup/(?P<group_pk>[0-9]+)/$', views.deleteGroup, name='deleteGroup'),
    url(r'^groupAdminPanel/(?P<group_pk>[0-9]+)/$', views.groupAdminPanel, name='groupAdminPanel'),
    url(r'^groupMemberView/(?P<group_pk>[0-9]+)/$', views.groupMemberView, name='groupMemberView'),
]
