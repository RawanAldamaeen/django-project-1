from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView
from .forms import PatientForm, LoginForm
from base.models import User
from .models import Patient
from annoying.functions import get_object_or_None
# Create your views here.
from django.urls import reverse
from .utils import account_activation_token


@login_required
def patient_logout(request):  # patient logout view
    logout(request)
    return HttpResponseRedirect(reverse('base:index'))


class RegistraionView(FormView):  # patient registration view
    template_name = 'patient/register.html'
    form_class = PatientForm


@require_http_methods(["POST"])
def register(request):  # patient registration request handler
    registered = False
    form = PatientForm(request.POST, request.FILES)
    if form.is_valid():
        user = User()
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.set_password(request.POST.get('password'))
        user.is_patient = True
        user.is_active = False
        user.save()
        patient = Patient()
        patient = form.save(commit=False)
        patient.user = user
        patient.save()
        registered = True

        # patient activation email
        # current_site = get_current_site(request)
        # subject = 'Activate Your Account'
        # message = render_to_string('patient/account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        #
        # send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    else:
        print(form.errors)

    return render(request, 'patient/register.html', {'form': form,
                                                     'registered': registered})


def activate(request, uidb64, token):  # patient activation check
    id = force_text(urlsafe_base64_decode(uidb64))

    obj = get_object_or_None(User, pk=id)
    if not obj:
        raise Http404('user not found')

    if not account_activation_token.check_token(obj, token):
        return redirect('/' + '?message=' + 'User already activated')

    if obj.is_active:
        return redirect('/')
    obj.is_active = True
    obj.save()
    messages.success(request, 'Account activated successfully')
    return redirect('/')


class LoginView(FormView):  # Patient login view
    template_name = 'patient/login.html'
    form_class = LoginForm


@require_http_methods(["POST"])
def patient_login(request):      # patient login request handler

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        print("Someone tried to login and failed.")
        print("They used username:".format(username))
        return HttpResponse("Invalid login details given")

    if not user.is_active:
        return HttpResponse("Your account still inactive,check your email for activate email")

    if not user.is_patient:
        return HttpResponse("<h3>This page for patient login<h3>")

    login(request, user)
    return HttpResponseRedirect(reverse('reservations:doctors_list'))

