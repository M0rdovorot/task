from django.contrib.auth import login

from . import models
from django.contrib import auth
from django.shortcuts import render, redirect
import os
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.urls import reverse, resolve


@login_required(login_url='login/', redirect_field_name="continue")
def logout(request):
    auth.logout(request)
    return redirect(reverse("index"))


@login_required(login_url='login/', redirect_field_name="continue")
def index(request):
    return render(request, 'index.html', context={'user': request.user})


@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                if request.GET.__contains__('continue') and request.GET.get('continue') != '':
                    return redirect(request.GET.get('continue'))
                else:
                    return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', context={'form': login_form})


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        registration_form = RegistrationForm()
    elif request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            if user:
                user.save()
                return redirect(reverse('index'))
            registration_form.add_error(None, 'User saving error')
    return render(request, 'signup.html', context={'form': registration_form})