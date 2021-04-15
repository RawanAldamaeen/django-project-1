from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Shifts
from base.models import Doctor
from .forms import NewShifts


class ShiftsListView(ListView):
    model = Shifts
    context_object_name = 'shifts'
    ordering = ['-id']


class ShiftsDetailView(DetailView):
    model = Shifts
    template_name = 'shifts/shift_detail.html'


class ShiftsCreateView(LoginRequiredMixin, CreateView):
    model = Shifts
    fields = ['all_day', 'day', 'start_time', 'end_time']
    template_name = 'shifts/shifts_form.html'

    def form_valid(self, form):
        form.instance.doctor_id = self.request.user.doctor
        return super().form_valid(form)

    def get_success_url(self):
        if 'add_new' in self.request.POST:
            return self.request.path
        else:
            return reverse("shifts:shifts_list")


class ShiftsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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


class ShiftsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Shifts
    template_name = 'shifts/shift_confirm_delete.html'
    success_url = '/shifts/'

    def test_func(self):
        shift = self.get_object()
        if self.request.user.doctor == shift.doctor_id:
            return True
        return False