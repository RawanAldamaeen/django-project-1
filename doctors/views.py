from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import DocForm, DocProfileForm
from base.models import User,Doctor, Specialty

# Create your views here.
from django.urls import reverse



@login_required
def doctors_logout(request):  # doctor logout view
    logout(request)
    return HttpResponseRedirect(reverse('base:index'))


def register(request):      # doctor registration view
    registered = False
    if request.method == 'POST':
        doc_form = DocForm(data=request.POST)
        doc_profile_form = DocProfileForm(data=request.POST)
        s = request.POST.get('specialty')
        specialty = Specialty.objects.create(specialty=s)
        if doc_form.is_valid() and doc_profile_form.is_valid():
            user = doc_form.save()
            user.set_password(user.password)
            user.is_doctor = True
            doctor = Doctor()
            doctor.user = user
            user.doctor.phone = request.POST.get('phone')
            user.doctor.name = request.POST.get('name')
            user.doctor.photo = request.FILES['photo']
            user.doctor.degree_copy = request.FILES['degree_copy']
            user.doctor.gender = request.POST.get('gender')
            user.doctor.specialty_id = Specialty.objects.get(id=specialty.id)
            user.save()
            registered = True
        else:
            print(doc_form.errors, doc_profile_form.errors)
    else:
        doc_form = DocForm()
        doc_profile_form = DocProfileForm()

    return render(request, 'doctor/register.html',
                  {'doc_form': doc_form,
                   'doc_profile_form': doc_profile_form,
                   'registered': registered})


def doctor_login(request):  # doctor login view
    if not request.method == 'POST':
        return render(request, 'doctor/login.html', {})

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        print("Someone tried to login and failed.")
        print("They used username: {} and password: {}".format(username, password))
        return HttpResponse("Invalid login details given")

    if not user.is_active:
        return HttpResponse("Your account still inactive, Admin will active it soon.")

    if not user.is_doctor:
        return HttpResponse("<h3>This page for doctor login<h3>")
    login(request, user)
    return HttpResponseRedirect(reverse('reservations:reservations_list'))

