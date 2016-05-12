from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^patientList/$', views.patientList, name='patientList'),
    url(r'^admit/(?P<pk>[0-9]+)/$',views.admitPatient, name='admitPatient'),
    url(r'^patientInfo/(?P<pk>[0-9]+)/$', views.viewPatientDetails, name='patientDetails'),
    url(r'^admitted/$', views.admittedPatients, name='admittedPats'),
    url(r'^discharge/(?P<pk>[0-9]+)/$', views.dischargePatient, name='discharge'),
    url(r'^transferSuccess/([0-9]+)/$', views.transferPatient, name='transferPatient'),
    url(r'^transferFailed/([0-9]+)/$', views.transferFailed, name='cannotTransfer'),
]
