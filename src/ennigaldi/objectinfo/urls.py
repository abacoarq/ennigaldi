from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^add/(?P<objectname_id>[0-9]+)/register/', views.object_entry, name='objectregister_form'),
    url(r'^add/{?P<work_id>[0-9]+/production/', views.ProductionEntry.as_view(), name='production_entry'),
    url(r'^add/(?P<work_id>[0-9]+)/description/', views.DescriptionEntry.as_view(), name='description_entry'),
    url(r'^add/$', views.title_entry, name='titleentry_form'),
    url('^(?P<pk>[0-9]+)/$', views.ObjectDetail.as_view(), name='objectregister_detail'),
    url(r'^sicg/(?P<pk>[0-9]+)/', views.ObjectDetail.as_view(template_name="objectinfo/sicg_m305.html"), name='sicg_m305'),
    url(r'^xml/(?P<pk>[0-9]+)/', views.xml, name='vra_core_xml'),
    url(r'^yaml/(?P<pk>[0-9]+)/', views.yaml, name='yaml'),
    url(r'^', views.ObjectList.as_view(), name='object_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
