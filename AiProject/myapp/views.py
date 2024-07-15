
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django import forms
from .forms import StudentSignUpForm, PractitionerSignUpForm
from .decorators import student_required, practitioner_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

import random
from django.conf import settings





def practitioner_register(request):
    if request.method == 'POST':
        form = PractitionerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('practitioner_dashboard')
    else:
        form = PractitionerSignUpForm()
    return render(request, 'registration/practitioner_register.html', {'form': form})





	