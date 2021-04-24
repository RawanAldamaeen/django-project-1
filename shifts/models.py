
from django.db import models
from base.models import Doctor
from django.core.validators import RegexValidator


time_regex = RegexValidator(regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s?(?:AM|PM|am|pm)')


class Shifts(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    all_day = models.BooleanField(default=False)
    start_time = models.CharField(validators=[time_regex], max_length=20, default=' ', blank=True)
    end_time = models.CharField(validators=[time_regex], max_length=20, default=' ', blank=True)
    day = models.CharField(choices=[('Sun', 'Sunday'),
                                    ('Mon', 'Monday'),
                                    ('Tue', 'Tuesday'),
                                    ('Wen', 'Wednesday'),
                                    ('Thu', 'Thursday'),
                                    ('Fri', 'Friday'),
                                    ('Sat', 'Saturday')], default=" ", max_length=10)
