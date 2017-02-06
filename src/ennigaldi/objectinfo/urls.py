from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.object_list, name='object_list'),
    url(r'^work/new/$', views.field_form, name='field_entry_form'),
    url(r'^sicg/w_(?P<work_id>[0-9]+/$', views.m305, name='sicg_m305'),
    url(r'^xml/w_(?P<work_id>[0-9]+/$', views.xml, name='vra_core_xml'),
    url(r'^yaml/w_(?P<work_id>[0-9]+/$', views.yaml, name='yaml'),
]
