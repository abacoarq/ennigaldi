from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^work/$', views.object_list, name='object_list'),
    url(r'^work/new/$', views.field_form, name='field_entry_form'),
    url(r'^sicg/w_', views.m305, name='sicg_m305'),
    url(r'^xml/w_', views.xml, name='vra_core_xml'),
]
