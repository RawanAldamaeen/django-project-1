from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, FormView,
)
from .models import Reservation
from base.models import Doctor, Patient
from .forms import NewReservation


class DoctorsListView(ListView):  # Doctors list view
    model = Doctor
    context_object_name = 'doctors'
    ordering = ['-id']
    template_name = 'reservations/doctors_list.html'


class ReservationListView(ListView):  # All reservations list view
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'reservations/reservations_list.html'


class PatientReservationsListView(ListView):  # Patient reservations list view
    model = Reservation
    context_object_name = "reservations"
    template_name = 'reservations/patient_reservations_list.html'


def rservationsCreate(request, doctor_id):  # Reservations create view
    print(request.POST)
    form = NewReservation(data=request.POST)
    doctor = Doctor.objects.get(id= doctor_id)
    if request.method == "POST":
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.patient_id = request.user.patient
            reservation.doctor_id = doctor
            reservation.status = 'new'
            reservation.save()
    return render(request, 'reservations/reservation_form.html', {'form': form})


@require_http_methods(["POST"])
def reservationStatusChange(request, reservation_id):  # Reservation change status view

    reservation = Reservation.objects.get(id=reservation_id)
    if 'confirm' in request.POST:
        reservation.status = "confirm"
    elif 'cancel' in request.POST:
        reservation.status = 'canceled'
    elif 'complete' in request.POST:
        reservation.status = 'closed'

    reservation.save()
    return redirect('reservations:reservations_list')


def reservations_search(request):  # Reservations search view
    query = request.GET['query']

    reservations = Reservation.objects.filter(
        Q(patient_id__name__icontains=query) |
        Q(status__icontains=query))

    params = {'reservations': reservations, 'query': query}
    return render(request, 'reservations/doc_search_result.html', params)


def doctors_search(request):  # Doctors search view
    query = request.GET['query']

    doctors = Doctor.objects.filter(
        Q(name__icontains=query) |
        Q(specialty_id__specialty__icontains=query))

    params = {'doctors': doctors, 'query': query}
    return render(request, 'reservations/patient_search_result.html', params)

