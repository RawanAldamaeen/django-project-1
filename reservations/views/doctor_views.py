from annoying.functions import get_object_or_None
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from reservations.models import Reservation

from reservation.reservation import settings


class ReservationListView(ListView):  # All reservations list view
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'reservations/reservations_list.html'


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


def rejection_form_view(request, reservation_id):  # Doctors login view
    obj = get_object_or_None(Reservation, id=reservation_id)
    if not obj:
        raise Http404('Reservation not found')

    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'reservations/reject_form.html', {'reservation': reservation})


@require_http_methods(["POST"])
def rejection_form(request, reservation_id):  # Reservation change status view
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 'canceled'
    reservation.rejection_reason = request.POST.get('rejection_reason')

    subject = f'Your Reservation Rejected'
    message = f'Hello {reservation.patient_id.name}' \
              f'Your reservation on {reservation.date}, at {reservation.time} with Doctor : {reservation.doctor_id.name}' \
              f'is Rejected for the following reason: {reservation.rejection_reason}'

    send_mail(subject, message, settings.EMAIL_HOST_USER, [reservation.patient_id.user.email])

    reservation.save()
    return redirect(reverse('reservation:rejected-form-view', kwargs={'reservation_id': reservation_id}),
                    {'reservation': reservation})


def reservations_search(request):  # Reservations search view
    query = request.GET['query']

    reservations = Reservation.objects.filter(
        Q(patient_id__name__icontains=query) |
        Q(status__icontains=query))

    params = {'reservations': reservations, 'query': query}
    return render(request, 'reservations/doc_search_result.html', params)

