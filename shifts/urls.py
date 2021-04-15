from django.conf.urls import url
from django.urls import path
from .views import (
 ShiftsListView,
 ShiftsCreateView,
 ShiftsDeleteView,
 ShiftsDetailView,
 ShiftsUpdateView
)

app_name = 'shifts'

urlpatterns = [
    url(r'^$', ShiftsListView.as_view(), name='shifts_list'),
    url(r'^(?P<pk>\d+)/$', ShiftsDetailView.as_view(), name='shift_detail'),
    url(r'^new/$', ShiftsCreateView.as_view(), name='shift_create'),
    url(r'^(?P<pk>\d+)/update/$', ShiftsUpdateView.as_view(), name='shift_update'),
    url(r'^(?P<pk>\d+)/delete/$', ShiftsDeleteView.as_view(), name='shift_delete'),
]