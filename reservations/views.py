from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from .models import Reservation
from base.models import Doctor, Patient
from .forms import NewReservation
from datetime import datetime, timedelta
from shifts.models import Shifts
from annoying.functions import get_object_or_None
from django.utils.translation import gettext as _
from django.utils import translation
from reservation import settings


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

    form = NewReservation(data=request.POST)
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == "POST":
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.patient_id = request.user.patient
            reservation.doctor_id = doctor

            # Check doctor available day
            day = datetime.strftime(reservation.date, "%A")
            doctor_shifts = get_object_or_None(Shifts, day=day, doctor_id=doctor)
            if doctor_shifts is None:
                messages.error(request, 'Doctor is unavailable on this day, please choose another day')
                return redirect(request.path)

            # Check doctor available time
            start = datetime.strptime(doctor_shifts.start_time, '%I:%M %p')
            print(start.time())
            end = datetime.strptime(doctor_shifts.end_time, '%I:%M %p')
            print(end.time())
            reservations = Reservation.objects.filter(doctor_id=doctor)
            for x in reservations:
                free = True
                while start < end:
                    # Check the time of the reservation in the shifts range
                    if x.time < start.time() or x.time > end.time():
                        print(x.time)
                        free = False
                        messages.error(request, 'Doctor is unavailable on this time, please choose another time')
                        return redirect(request.path)
                        break
                    # Check if the time of the reservations isn't conflict with other reservations
                    if x.time == reservation.time and x.status == 'confirm':
                        free = False
                        messages.error(request, 'Doctor is unavailable on this time, please choose another hour')
                        return redirect(request.path)
                        break
                    start += timedelta(hours=1)

            if free is True:
                print('accepted')
                reservation.status = 'new'
                reservation.save()
                # Doctor New Reservation notify email
                subject = f'New Reservation for {reservation.patient_id.name}'
                message = f'Hello Dr. {reservation.doctor_id.name}' \
                          f'THere is New reservation on {reservation.date}, at {reservation.time} for patinent : {reservation.patient_id.name},' \
                          f' go to your Reservations and take action with it'

                send_mail(subject, message, settings.EMAIL_HOST_USER, [reservation.doctor_id.user.email])

    return render(request, 'reservations/reservation_form.html', {'form': form})


@require_http_methods(["POST"])
def reservationStatusChange(request, reservation_id):  # Reservation change status view

    reservation = Reservation.objects.get(id=reservation_id)
    if 'confirm' in request.POST:

        reservation.status = "confirm"
        subject = f'Your Reservation is confirmed'
        message = f'Hello {reservation.patient_id.name}' \
                  f'Your reservation on {reservation.date}, at {reservation.time} with Doctor : {reservation.doctor_id.name}' \
                  f'is approved, make sure to be on the hospital 10 min before the time'

        send_mail(subject, message, settings.EMAIL_HOST_USER, [reservation.patient_id.user.email])

    elif 'complete' in request.POST:
        reservation.status = 'closed'

    reservation.save()
    return redirect('reservations:reservations_list')


def rejection_view(request, reservation_id):  # Reservation change status view
    if request.method == "POST":
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.status = 'canceled'
        reservation.rejection_reason = request.POST.get('rejection_reason')

        subject = f'Your Reservation Rejected'
        message = f'Hello {reservation.patient_id.name}' \
                  f'Your reservation on {reservation.date}, at {reservation.time} with Doctor : {reservation.doctor_id.name}' \
                  f'is Rejected for the following reason: {reservation.rejection_reason}'

        send_mail(subject, message, settings.EMAIL_HOST_USER, [reservation.patient_id.user.email])

        reservation.save()
    return render(request, 'reservations/reject_form.html')


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
