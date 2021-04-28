from annoying.functions import get_object_or_None
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView
from .forms import NewRate
from reservations.models import Reservation


def rate_create_view(request, reservation_id):  # Doctors login view
    obj = get_object_or_None(Reservation, id=reservation_id)
    if not obj:
        raise Http404('page not found')

    form = NewRate()
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'rates/rate_form.html', {'reservation': reservation, 'form': form})


@require_http_methods(["POST"])
def rate_create(request, reservation_id):  # Create new Shift request handler
    form = NewRate(data=request.POST)

    if not form.is_valid():
        print(form.errors)
        return redirect(reverse('rates:rate-form-view'))

    rate = form.save(commit=False)
    rate.reservation_id = Reservation.objects.get(id=reservation_id)
    rate.save()

    return redirect(reverse('rates:rate-form-view', kwargs={'reservation_id': reservation_id}), {'form': form})
