from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.views.decorators.http import require_http_methods

from .forms import DocForm, LoginForm
from base.models import Doctor, Specialty, User

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
    if form.is_valid():
        user = User()
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.set_password(request.POST.get('password'))
        user.is_doctor = True
        user.is_active = False
        user.save()
        doctor = Doctor()
        doctor = form.save(commit=False)
        doctor.user = user
        doctor.specialty_id = Specialty.objects.get(id=s)
        doctor.save()
        registered = True
    else:
        print(form.errors)

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
        return HttpResponse("Invalid login details given")

    if not user.is_active:
        return HttpResponse("Your account still inactive, Admin will active it soon.")

    login(request, user)
    return HttpResponseRedirect(reverse('base:index'))

