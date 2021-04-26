from django.db import models
from base.models import Doctor, Patient


class Reservation(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField()
    status = models.CharField(
        choices=[('new', 'New'), ('confirm', 'Confirm'), ('canceled', 'Canceled'), ('closed', 'Closed')],
        default='new', max_length=20)
