from django.contrib import admin
from .models import Patient

class PatientsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(Patient, PatientsAdmin)
