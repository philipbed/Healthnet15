from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^upload/$',views.uploadResults,name='uploadTest'),
    url(r'^viewResults/$',views.viewAllResults,name='viewTestResults'),
    url(r'^update/(?P<pk>[0-9]+)/$',views.updateResults,name='updateTest'),
    url(r'^comments/(?P<pk>[0-9]+)/$',views.viewComments,name='viewComments'),
]


