from django.conf.urls import url
from django.urls import path

from .views.doctor_views import ReservationListView
from .views.patient_view import (DoctorsListView, PatientReservationsListView)

from .views import doctor_views as doc_view
from .views import patient_view as pat_view

app_name = 'reservation'

urlpatterns = [
    url(r'^$', DoctorsListView.as_view(), name='doctors_list'),
    url(r'^list/$', ReservationListView.as_view(), name='reservations_list'),
    url(r'^my_reservations/$', PatientReservationsListView.as_view(), name='patient_reservations_list'),
    path('<int:reservation_id>/change/', doc_view.reservationStatusChange, name='status_change'),
    path('<int:reservation_id>/reject/', doc_view.rejection_form_view, name='rejected-form-view'),
    path('<int:reservation_id>/reject/request', doc_view.rejection_form, name='rejected-form'),
    path('<int:doctor_id>/new', pat_view.reservations_create_view, name='reservation_form_view'),
    path('<int:doctor_id>/new/request', pat_view.rservationsCreate, name='reservation_form'),
    url(r'^search/$', doc_view.reservations_search, name='doc_search_result'),
    url(r'^search/$', pat_view.doctors_search, name='patient_search_result'),


]