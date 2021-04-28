from django import forms
from .models import Rate


class NewRate (forms.ModelForm):

    class Meta:
        model = Rate
        fields = ["rate", "comments"]