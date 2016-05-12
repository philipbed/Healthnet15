from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.listLog, name='log'),
    url(r'^(?P<reverseTime>\d{1})/(?P<startDay>\d{8})/(?P<endDay>\d{8})/$', views.listLog, name='log'),

    url(r'^stats/$', views.stats, name='stats'),
    url(r'^stats/(?P<startDay>\d{8})/(?P<endDay>\d{8})/$', views.stats, name='stats'),
    url(r'^stats/(?P<startDay>\d{8})/(?P<endDay>\d{8})/(?P<hospital>[0-9]+)/$', views.stats, name='stats'),

    url(r'^filter/$', views.filterLog, name='filter'),
    url(r'^stats/filter/$', views.filterStats, name='filterStats'),
]
