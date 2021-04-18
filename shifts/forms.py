from datetime import datetime, time

from django import forms
from django.http import Http404

from .models import Shifts


class NewShifts(forms.ModelForm):
    class Meta:
        model = Shifts
        fields = ["day", "all_day", "start_time", "end_time"]

    def clean(self):
        super(NewShifts, self).clean()

        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        if start_time and end_time:
            start = datetime.strptime(start_time, '%H:%M %p')
            end = datetime.strptime(end_time, '%H:%M %p')

            if start > end:
                self._errors['start_time'] = self.error_class([
                    'shift start time should be before shift end time'])



