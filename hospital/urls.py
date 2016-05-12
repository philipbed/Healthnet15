from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hospitalRedirect),
    url(r'^create/$', views.createHospital, name='create'),
    url(r'^view/$', views.viewHospitals, name='view'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.updateHospital.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.deleteHospital, name='delete'),
]
