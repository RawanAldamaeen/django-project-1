from django.db import models


class Specialty(models.Model):
    specialty_en = models.CharField(max_length=100)
    specialty_ar = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.specialty_en
