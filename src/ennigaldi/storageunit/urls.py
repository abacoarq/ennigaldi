from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all/$', views.UnitList.as_view(), name='unit_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.UnitDetail.as_view(), name='unit_detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.UpdateUnit.as_view(), name='update_unit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteUnit.as_view(), name='delete_unit'),
    url(r'^add/$', views.AddUnit.as_view(), name='field_entry_form'),
    url(r'^', views.TopLevelUnits.as_view(), name='unit_list_top'),
]
