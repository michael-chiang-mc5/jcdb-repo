from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^jcdb_logout/$', views.jcdb_logout, name='jcdb_logout'),
]
