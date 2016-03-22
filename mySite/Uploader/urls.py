from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.list, name='list'),
    url(r'^delete/(?P<document_pk>[0-9]+)/$', views.delete, name='delete'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^uploadInterface/(?P<group_pk>[0-9]+)/$', views.uploadInterface, name='uploadInterface'),
]
