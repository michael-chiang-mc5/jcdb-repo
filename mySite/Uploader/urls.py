from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^uploadInterface/(?P<group_pk>[0-9]+)/$', views.uploadInterface, name='uploadInterface'),
    url(r'^editTitle/(?P<document_pk>[0-9]+)/$', views.editTitle, name='editTitle'),
]
