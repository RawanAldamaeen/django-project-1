from django.contrib import admin
from .models import User, Doctor

class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(Doctor, DoctorsAdmin)
