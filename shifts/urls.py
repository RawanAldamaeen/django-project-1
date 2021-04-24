from django.conf.urls import url
from . import views
from .views import (
 ShiftsListView,
 ShiftsFormView,
 ShiftsDeleteView,
 ShiftsUpdateView
)
from . import views
app_name = 'shifts'

urlpatterns = [
    url(r'^$', ShiftsListView.as_view(), name='shifts_list'),
    url(r'^new/$', ShiftsFormView.as_view(), name='shift_create_view'),
    url(r'^new/request/$', views.shifts_create, name='shift_create'),
    url(r'^(?P<pk>\d+)/update/$', ShiftsUpdateView.as_view(), name='shift_update'),
    url(r'^(?P<pk>\d+)/delete/$', ShiftsDeleteView.as_view(), name='shift_delete'),
]