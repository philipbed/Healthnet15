from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.createHistory, name='create'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.viewHistory, name='history'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update, name='update'),
    url(r'^error/$', views.viewHistory, name='error'),
]