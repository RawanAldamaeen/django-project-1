from django.contrib import admin
from .models import User, Doctor, Specialty


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(User)
admin.site.register(Doctor, DoctorsAdmin)
admin.site.register(Specialty)