from django.contrib import admin
from .models import Patient

# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(Patient, PatientAdmin)