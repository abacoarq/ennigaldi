from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ObjectList.as_view(), name='object_list'),
    url(r'^add/$', views.title_entry, name='titleentry_form'),
    url(r'^add/(?P<objectname_id>[0-9]+)/register/$', views.object_entry, name='objectregister_form'),
    url(r'^add/(?P<work_id>[0-9]+)/description/$', views.DescriptionForm.as_view(), name='description_form'),
    url(r'^sicg/(?P<work_id>[0-9]+)/$', views.ObjectDetail.as_view(template_name="sicg_m305.html"), name='sicg_m305'),
    url(r'^xml/(?P<work_id>[0-9]+)/$', views.xml, name='vra_core_xml'),
    url(r'^yaml/(?P<work_id>[0-9]+)/$', views.yaml, name='yaml'),
]
