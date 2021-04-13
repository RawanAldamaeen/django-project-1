from django.conf.urls import url
from django.contrib.auth import views as auth_views
from patient import views
from django.urls import path

app_name = 'patient'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.patient_login, name='login'),
    url(r'^logout/$', views.patient_logout, name='logout'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]