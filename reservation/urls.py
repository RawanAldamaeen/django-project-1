"""reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from base import views
from doctors import views
from shifts import views
from reservations import views
from patient import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('base.urls', 'base'), namespace="base")),
    url(r'^doctor/', include(('doctors.urls', 'doctors'), namespace="doctors")),
    url(r'^patient/', include(('patient.urls', 'patient'), namespace="patient")),
    url(r'^shifts/', include(('shifts.urls', 'shifts'), namespace="shifts")),
    url(r'^reservation/', include(('reservations.urls', 'reservations'), namespace="reservations")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
