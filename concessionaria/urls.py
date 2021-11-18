from django.urls import path,include
from concessionaria.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^index/$',index),
    url(r'^login/$',login),
    url(r'^auth/$',auth_view),
    url(r'^logout/$',logout_view),
    url(r'^register/$',register),
    url(r'^registration/$',registration),
    url(r'^add_vehicle/$',add_vehicle),
    url(r'^manage_vehicles/$',manage_vehicles),
    url(r'^delete/$',delete),
]
