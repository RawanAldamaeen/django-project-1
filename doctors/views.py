from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.decorators.http import require_http_methods
from .forms import DocForm, LoginForm
from base.models import User
from .models.doctor import Doctor
from .models.specialty import Specialty

# Create your views here.
from django.urls import reverse


@login_required
def doctors_logout(request):  # Doctors logout view
    logout(request)
    return HttpResponseRedirect(reverse('base:index'))


class RegistraionView(FormView):  # Doctors registration view
    template_name = 'doctor/register.html'
    form_class = DocForm


@require_http_methods(["POST"])
def register(request):      # Doctor registration request handler
    registered = False
    form = DocForm(request.POST, request.FILES)
    s = request.POST.get('specialty')

    if not form.is_valid():
        print(form.errors)
        redirect(request.path)

    user = User()
    user.email = request.POST.get('email')
    user.username = request.POST.get('username')
    user.set_password(request.POST.get('password'))
    user.is_doctor = True
    user.is_active= False
    user.save()
    doctor = Doctor()
    doctor = form.save(commit=False)
    doctor.user = user
    doctor.specialty_id = Specialty.objects.get(id=s)
    doctor.save()

    registered = True

    return render(request, 'doctor/register.html', {'form': form,
                                                    'registered': registered})


class LoginView(FormView):  # Doctors login view
    template_name = 'doctor/login.html'
    form_class = LoginForm


@require_http_methods(["POST"])
def doctor_login(request):      # Doctor login request handler

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        print("Someone tried to login and failed.")
        print("They used username:".format(username))
        messages.error(request, "Invalid login details given")
        return redirect(request.path)

    if not user.is_active:
        messages.error(request, "Your account still inactive, Admin will active it soon.")
        return redirect(request.path)

    login(request, user)
    return HttpResponseRedirect(reverse('base:index'))

