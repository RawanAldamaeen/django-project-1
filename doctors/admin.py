from django.contrib import admin
from .models.specialty import Specialty
from .models.doctor import Doctor

class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(Doctor, DoctorsAdmin)
admin.site.register(Specialty)
