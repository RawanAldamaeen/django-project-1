from datetime import datetime

from django import forms
from .models import Reservation
from django.contrib.auth.models import User
from shifts.models import Shifts


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class NewReservation(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Reservation
        fields = ['time', 'date']

    # def clean_time(self):
    #     cleaned_data = super(NewReservation, self).clean()
    #     time = cleaned_data.get('time')
    #     doctor = cleaned_data.get('doctor_id')
    #     print(doctor)
    #     time_day = datetime.strftime(time, "%A")
    #     print(type(time_day))
    #     print(time_day)

        # doc_shifts_day = Shifts.objects.get(day= time_day).filter(doctor_id=doctor)
        #
        # if time_day in doc_shifts_day:
        #     print('yes')
        # else:
        #     print('busy')

