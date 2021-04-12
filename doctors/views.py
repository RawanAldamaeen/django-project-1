from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocForm, DocProfileForm
from .models import Doctor

# Create your views here.
from django.urls import reverse


@login_required
def user_logout(request):  # User logout view
    logout(request)
    return HttpResponseRedirect(reverse('base:index'))


def register(request):
    registered = False
    if request.method == 'POST':
        doc_form = DocForm(data=request.POST)
        doc_profile_form = DocProfileForm(data=request.POST)
        if doc_form.is_valid() and doc_profile_form.is_valid():
            user = doc_form.save()
            user.set_password(user.password)
            user.doctor.phone = request.POST.get('phone')
            user.doctor.name = request.POST.get('name')
            user.doctor.photo = request.FILES['photo']
            user.doctor.degree_copy = request.FILES['degree_copy']
            user.doctor.gender = request.POST.get('gender')
            user.save()
            registered = True
        else:
            print(doc_form.errors, doc_profile_form.errors)
    else:
        doc_form = DocForm()
        doc_profile_form = DocProfileForm()

    return render(request, 'doctor/register.html',
                  {'doc_form': doc_form,
                   'doc_profile_form': doc_profile_form, 'registered': registered})

