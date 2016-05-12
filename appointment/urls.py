from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.redirectAppointment),
    url(r'^view/$', views.viewAppointment, name='view'),

    url(r'^schedule/$', views.scheduleAppointment, name='schedule'),

    url(r'^doccreate/$', views.scheduleDoctor, name='scheduleDoctor'),
    url(r'^doccreate/(?P<patient>[0-9]+)/$', views.scheduleDoctor, name='scheduleDoctor'), # Pass in a patient

    url(r'^nurcreate/$', views.scheduleNurse, name='scheduleNurse'),
    url(r'^nurcreate/(?P<patient>[0-9]+)/$', views.scheduleNurse, name='scheduleNurse'), # Pass in a patient


    url(r'^update/(?P<pk>[0-9]+)/$', views.updateAppointment, name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.deleteAppointment, name='delete'),
]
    