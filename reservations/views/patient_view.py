from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from reservations.models import Reservation
from doctors.models.doctor import Doctor
from patient.models import Patient
from reservations.forms import NewReservation
from datetime import datetime
from shifts.models import Shifts
from annoying.functions import get_object_or_None
from reservation import settings


class DoctorsListView(ListView):  # Doctors list view
    model = Doctor
    context_object_name = 'doctors'
    ordering = ['-id']
    template_name = 'reservations/doctors_list.html'


class PatientReservationsListView(ListView):  # Patient reservations list view
    model = Reservation
    context_object_name = "reservations"
    template_name = 'reservations/patient_reservations_list.html'


def reservations_create_view(request, doctor_id):  # Doctors login view
    obj = get_object_or_None(Doctor, id=doctor_id)
    if not obj:
        raise Http404('Doctor not found')

    form = NewReservation()
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'reservations/reservation_form.html', {'doctor': doctor, 'form': form})


@require_http_methods(["POST"])
def rservationsCreate(request, doctor_id):  # Reservations create view
    form = NewReservation(data=request.POST)
    doctor = Doctor.objects.get(id=doctor_id)
    print(doctor.id)
    if not form.is_valid():
        print(form.errors)
        return redirect(reverse('reservation:reservation_form_view', kwargs={'doctor_id': doctor_id}))

    reservation = form.save(commit=False)
    reservation.patient_id = request.user.patient
    reservation.doctor_id = doctor

    # Check doctor available day
    day = datetime.strftime(reservation.date, "%A")
    print(day)
    doctor_shifts = get_object_or_None(Shifts, day=day, doctor_id=doctor.id)
    print(doctor_shifts)
    if doctor_shifts is None:
        print('inside day if')
        messages.error(request, 'Doctor is unavailable on this day, please choose another day')
        return redirect(reverse('reservation:reservation_form_view', kwargs={'doctor_id': doctor_id}))

    # Check doctor available time
    # 1- check if the reservation time in the doctor shift range
    free = False
    start = datetime.strptime(doctor_shifts.start_time, '%I:%M %p')
    end = datetime.strptime(doctor_shifts.end_time, '%I:%M %p')
    print(reservation.time)
    if reservation.time < start.time() or reservation.time > end.time():
        print('inside first if')
        free = False
        messages.error(request, 'Doctor is unavailable on this time, please choose another time')
        return redirect(reverse('reservation:reservation_form_view', kwargs={'doctor_id': doctor_id}))

    # 2- Check if the time of the reservations isn't conflict with other reservations
    reservations = Reservation.objects.filter(doctor_id=doctor)
    print(reservations)
    if not reservations:
        free = True
    for x in reservations:
        if not x.time == reservation.time and not x.status == 'confirm' and not x.date == reservation.date:
            free = True
        free = False
        messages.error(request, 'Doctor is unavailable on this time, please choose another hour')
        return redirect(reverse('reservation:reservation_form_view', kwargs={'doctor_id': doctor_id}))

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

    return redirect(reverse('reservation:reservation_form_view', kwargs={'doctor_id': doctor_id}),
                    {'doctor': doctor, 'form': form})


def doctors_search(request):  # Doctors search view
    query = request.GET['query']

    doctors = Doctor.objects.filter(
        Q(name__icontains=query) |
        Q(specialty_id__specialty_en__icontains=query) |
        Q(specialty_id__specialty_ar__icontains=query))

    params = {'doctors': doctors, 'query': query}
    return render(request, 'reservations/patient_search_result.html', params)