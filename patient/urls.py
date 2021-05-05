from django.conf.urls import url
from django.contrib.auth import views as auth_views
from patient import views
from django.urls import path
from .views import RegistraionView, LoginView

app_name = 'patient'

urlpatterns = [
    url(r'^register/$', RegistraionView.as_view(), name='registration_view'),
    url(r'^register/request$', views.register, name='register'),
    url(r'^login/$', LoginView.as_view(), name='login_view'),
    url(r'^login/request$', views.patient_login, name='login'),
    url(r'^logout/$', views.patient_logout, name='logout'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]