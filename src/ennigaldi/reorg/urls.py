from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^start/$', views.StartBatch.as_view(), name='start_batch'),
    url(r'^', views.BatchList.as_view(), name='batch_list'),
]
