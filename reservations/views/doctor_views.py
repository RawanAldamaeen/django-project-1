from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from reservations.models import Reservation


class ReservationListView(ListView):  # All reservations list view
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'reservations/reservations_list.html'


def reservations_search(request):  # Reservations search view
    query = request.GET['query']

    reservations = Reservation.objects.filter(
        Q(patient_id__name__icontains=query) |
        Q(status__icontains=query))

    params = {'reservations': reservations, 'query': query}
    return render(request, 'reservations/doc_search_result.html', params)

