from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^work/$', views.object_list),
    url(r'^work/new/$', views.field_form),
    url(r'^work/', views.m305),
]
