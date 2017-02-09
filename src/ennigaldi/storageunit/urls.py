from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.unit_list, name='unit_list'),
    url(r'^add/$', views.field_form, name='field_entry_form'),
]
