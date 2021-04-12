from django.conf.urls import url
from django.contrib.auth import views as auth_views
from doctors import views

app_name = 'doctor'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
]