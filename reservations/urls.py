from django.conf.urls import url
from django.urls import path
from .views import (DoctorsListView,ReservationListView, PatientReservationsListView)
from . import views

app_name = 'reservation'

urlpatterns = [
    url(r'^$', DoctorsListView.as_view(), name='doctors_list'),
    url(r'^list/$', ReservationListView.as_view(), name='reservations_list'),
    url(r'^my_reservations/$', PatientReservationsListView.as_view(), name='patient_reservations_list'),
    path('<int:reservation_id>/change/', views.reservationStatusChange, name='status_change'),
    path('<int:reservation_id>/reject/', views.rejection_view, name='rejected-form'),
    path('<int:doctor_id>/new', views.reservations_create_view, name='reservation_form_view'),
    path('<int:doctor_id>/new/request', views.rservationsCreate, name='reservation_form'),
    url(r'^search/$', views.reservations_search, name='doc_search_result'),
    url(r'^doctors/search/$', views.doctors_search, name='patient_search_result'),

]