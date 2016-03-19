from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^viewer/(?P<document_pk>[0-9]+)$', views.viewer, name='viewer'),
    url(r'^viewer_raw/(?P<document_pk>[0-9]+)$', views.viewer_raw, name='viewer_raw'),
]
