from django import forms
from .models import Reservation
from django.contrib.auth.models import User


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class NewShifts(forms.ModelForm):
    time = forms.DateTimeField(widget=DateTimeInput)

    class Meta:
        model = Reservation
        fields = ['time']