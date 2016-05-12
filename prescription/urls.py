from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.createPrescription, name='create'),
    url(r'^create/(?P<patient>[0-9]+)/$', views.createPrescription, name='create'),

    url(r'^delete/(?P<pk>[0-9]+)/$', views.deletePrescription, name='delete'),
    
    url(r'^view/$', views.viewPrescriptions, name='view'),
]
