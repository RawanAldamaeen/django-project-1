from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .forms import PatForm, PatProfileForm
from base.models import User, Patient

# Create your views here.
from django.urls import reverse
from .utils import account_activation_token


@login_required
def patient_logout(request):  # patient logout view
    logout(request)
    return HttpResponseRedirect(reverse('base:index'))


def register(request):  # patient registration view
    registered = False
    if request.method == 'POST':
        pat_form = PatForm(data=request.POST)
        pat_profile_form = PatProfileForm(data=request.POST)
        if pat_form.is_valid() and pat_profile_form.is_valid():
            user = pat_form.save()
            user.set_password(user.password)
            user.is_patient = True
            patient = Patient()
            patient.user= user
            user.patient.phone = request.POST.get('phone')
            user.patient.name = request.POST.get('name')
            user.patient.photo = request.FILES['photo']
            user.patient.gender = request.POST.get('gender')
            user.save()
            registered = True

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('patient/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            return redirect('/patient/login')
        else:
            print(pat_form.errors, pat_profile_form.errors)
    else:
        doc_form = PatForm()
        doc_profile_form = PatProfileForm()

    return render(request, 'patient/register.html',
                  {'pat_form': PatForm,
                   'pat_profile_form': PatProfileForm, 'registered': registered})


def activate(request, uidb64, token):  # patient activation check
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('/' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('/')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('/')

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return redirect('/')


def patient_login(request):     # patient login view
    if not request.method == 'POST':
        return render(request, 'patient/login.html', {})

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        print("Someone tried to login and failed.")
        print("They used username: {} and password: {}".format(username, password))
        return HttpResponse("Invalid login details given")

    if not user.is_active:
        return HttpResponse("Your account still inactive,check your email for activate email")

    if not user.is_patient:
        return HttpResponse("<h3>This page for patient login<h3>")

    login(request, user)
    return HttpResponseRedirect(reverse('reservations:doctors_list'))

