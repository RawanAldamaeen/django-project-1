
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView, FormView, CreateView
)
from .models import Shifts
from doctors.models.doctor import Doctor
from .forms import NewShifts


class ShiftsListView(ListView):  # Shifts list view
    model = Shifts
    context_object_name = 'shifts'
    ordering = ['-id']


class ShiftsFormView(FormView):     # Create new shift view
    template_name = 'shifts/shifts_form.html'
    form_class = NewShifts


@require_http_methods(["POST"])
def shifts_create(request):  # Create new Shift request handler
    form = NewShifts(data=request.POST)

    if form.is_valid():
        shift = form.save(commit=False)
        shift.doctor_id = request.user.doctor
        shift.save()

        print(request.POST)
        if 'add_new' in request.POST:
            return redirect(reverse('shifts:shift_create_view'))
        else:
            return redirect(reverse('shifts:shifts_list'))

    else:
        print(form.errors)

    return render(request, 'shifts/shifts_form.html', {'form': form})


class ShiftsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # Shifts update view
    model = Shifts
    fields = ['all_day', 'day', 'start_time', 'end_time']
    success_url = '/shifts/'

    def form_valid(self, form):
        form.instance.doctor_id = self.request.user.doctor
        return super().form_valid(form)

    def test_func(self):
        shift = self.get_object()
        if self.request.user.doctor == shift.doctor_id:
            return True
        return False


class ShiftsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # Shifts delete view
    model = Shifts
    template_name = 'shifts/shift_confirm_delete.html'
    success_url = '/shifts/'

    def test_func(self):
        shift = self.get_object()
        if self.request.user.doctor == shift.doctor_id:
            return True
        return False