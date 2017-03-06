from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.UnitList.as_view(), name='unit_list'),
    url(r'^(?P<unit_id>[0-9]+)/$', views.unit_detail, name='unit_detail'),
    url(r'^add/$', views.AddUnit.as_view(), name='field_entry_form'),
]
