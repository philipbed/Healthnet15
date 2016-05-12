from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin/$', views.createAdmin, name='createAdmin'),
    url(r'^patient/$', views.createPatient, name='createPatient'),
    url(r'^doctor/$', views.createDoctor, name='createDoctor'),
    url(r'^nurse/$', views.createNurse, name='createNurse'),
]
