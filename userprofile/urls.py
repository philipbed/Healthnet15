from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.userLogin, name='userLogin'),
    url(r'^logout/$', views.userLogout, name='userLogout'),

    url(r'^view/$', views.viewProfile, name='viewProfile'),
    url(r'^Adminview/(?P<pk>[0-9]+)/$$', views.AdminView, name='AdminView'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.updateProf, name='userUpdate'),
    url(r'^update/Doc(?P<pk>[0-9]+)/$', views.updateDoctor, name='doctorUpdate'),
    url(r'^update/Nur(?P<pk>[0-9]+)/$', views.updateNurse, name='nurseUpdate'),
    url(r'^update/Adm(?P<pk>[0-9]+)/$', views.updateAdmin, name='adminUpdate'),
    url(r'^update/Root(?P<pk>[0-9]+)/$', views.updateRoot, name='rootUpdate'),

    url(r'^personnel/$', views.viewAllPersonnel, name='viewAllPersonnel'),

    url(r'^delete/Doc(?P<pk>[0-9]+)/$', views.deleteDoc, name='deleteDoc'),
    url(r'^delete/Nur(?P<pk>[0-9]+)/$', views.deleteNurse, name='deleteNurse'),
    url(r'^delete/Adm(?P<pk>[0-9]+)/$', views.deleteAdmin, name='deleteAdmin'),

    url(r'^move/Nur(?P<pk>[0-9]+)/$', views.moveNurse, name='moveNurse'),
    url(r'^move/Doc(?P<pk>[0-9]+)/$', views.moveDoctor, name='moveDoctor'),

    url(r'^preferred/(?P<pk>[0-9]+)/$',views.getPreferredHospitals, name='preferredHospitals'),
    url(r'^updatePreferred/(?P<pk>[0-9]+)/$',views.updatePreferredHospitals,name='updatePreferredHospitals')
]
