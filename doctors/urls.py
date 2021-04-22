from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .views import RegistraionView

app_name = 'doctor'

urlpatterns = [
    url(r'^register/$', RegistraionView.as_view(), name='registration_view'),
    url(r'^register/request$', views.register, name='register'),
    url(r'^logout/$', views.doctors_logout, name='logout'),
    url(r'^login/$', views.doctor_login, name='login'),
]