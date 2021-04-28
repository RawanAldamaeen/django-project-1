from datetime import datetime
from django import forms
from .models import Shifts


class NewShifts(forms.ModelForm):
    start_time = forms.CharField(required=False)
    end_time = forms.CharField(required=False)

    class Meta:
        model = Shifts
        fields = ["day", "all_day", "start_time", "end_time"]

    def clean(self):    # Check if start time before end time
        cleaned_data = super(NewShifts, self).clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time:
            start = datetime.strptime(start_time, '%I:%M %p')
            end = datetime.strptime(end_time, '%I:%M %p')

            if start > end:
                self._errors['start_time'] = self.error_class([
                    'shift start time should be before shift end time'])

        return cleaned_data
