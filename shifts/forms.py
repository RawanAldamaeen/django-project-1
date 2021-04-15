from django import forms
from .models import Shifts


class NewShifts(forms.ModelForm):
    class Meta:
        model = Shifts
        fields = ["day", "all_day", "start_time", "end_time"]