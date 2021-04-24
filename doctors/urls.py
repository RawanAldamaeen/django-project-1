from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .views import RegistraionView, LoginView

app_name = 'doctor'

urlpatterns = [
    url(r'^register/$', RegistraionView.as_view(), name='registration_view'),
    url(r'^register/request$', views.register, name='register'),
    url(r'^login/$', LoginView.as_view(), name='login_view'),
    url(r'^login/request$', views.doctor_login, name='login'),
    url(r'^logout/$', views.doctors_logout, name='logout'),
]