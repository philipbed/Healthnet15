from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^compose/$', views.compose, name='send'),
    url(r'^compose/(?P<recipient>[0-9]+)/$', views.compose, name='send'), # Send a message to a specific person
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^outbox/$', views.outbox, name='outbox'),
    url(r'^view/(?P<message_id>[\d]+)/$', views.view, name='view'),
    url(r'^delete/(?P<message_id>[\d]+)/$', views.delete, name='delete'),
    url(r'^reply/(?P<message_id>[\d]+)/$', views.reply, name='reply'),
]
    