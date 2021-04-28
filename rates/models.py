from django.db import models
from reservations.models import Reservation


# Create your models here.


class Rate(models.Model):
    rate = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default=None,
                            max_length=10)
    comments = models.TextField(blank=True, null=True)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)
