from django.urls import path

from . import views

app_name = 'rates'

urlpatterns = [
    path('<int:reservation_id>/', views.rate_create_view, name='rate-form-view'),
    path('<int:reservation_id>/request', views.rate_create, name='rate-form'),
    ]