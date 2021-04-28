from django.db import models
from doctors.models.doctor import Doctor
from patient.models import Patient


class Reservation(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rejection_reason = models.CharField(default=None, null=True, max_length=250)
    date = models.DateTimeField()
    time = models.TimeField()
    status = models.CharField(
        choices=[('new', 'New'), ('confirm', 'Confirm'), ('canceled', 'Canceled'), ('closed', 'Closed')],
        default='new', max_length=20)