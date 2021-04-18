from django.contrib import admin
from .models import User, Doctor, Patient, Specialty


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


class PatientsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(User)
admin.site.register(Doctor, DoctorsAdmin)
admin.site.register(Patient, PatientsAdmin)
admin.site.register(Specialty)
