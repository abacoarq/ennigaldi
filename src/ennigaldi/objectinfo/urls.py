from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ObjectList.as_view(), name='object_list'),
    url(r'^work/new/$', views.AddObject.as_view(), name='add_object'),
    url(r'^sicg/w_(?P<work_id>[0-9]+)/$', views.ObjectDetail.as_view(template_name="sicg_m305.html"), name='sicg_m305'),
    url(r'^xml/w_(?P<work_id>[0-9]+)/$', views.xml, name='vra_core_xml'),
    url(r'^yaml/w_(?P<work_id>[0-9]+)/$', views.yaml, name='yaml'),
]
