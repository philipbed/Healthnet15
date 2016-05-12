from django.conf.urls import url

from . import views

"""
    @description: The Landing Page for the HealthNet Application
"""
urlpatterns = [
    url(r'^$', views.redirectLanding),
    url(r'^home/$', views.landingPage, name='landing'),
]
