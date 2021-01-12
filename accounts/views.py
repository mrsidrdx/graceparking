from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from json import dumps,loads
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *

# Create your views here.

# WebAdmin LogOut
@login_required(login_url='web_admin_login')
def web_admin_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('web_admin_login'))

# WebAdmin Login
def web_admin_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('web_admin_dashboard'))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('web_admin_dashboard'))
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return render(request, 'accounts/signin.html', context = {'portal':'web_admin'})
    return render(request, 'accounts/signin.html', context = {'portal':'web_admin'})

# ApartmentOwners LogOut
@login_required(login_url='apartment_owners_login')
def apartment_owners_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('apartment_owners_login'))

# ApartmentOwners Login
def apartment_owners_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('apartment_dashboard'))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            checkUser = ApartmentOwners.objects.get(username=username, password=password)
        except Exception as e:
            messages.error(request, 'Invalid Login Credentials!')
            return render(request, 'accounts/signin.html', context = {'portal':'apartment_owners'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('apartment_dashboard'))
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return render(request, 'accounts/signin.html', context = {'portal':'apartment_owners'})
    return render(request, 'accounts/signin.html', context = {'portal':'apartment_owners'})

# ApartmentOwners Registeration
def apartment_owners_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('apartment_dashboard'))
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        username = request.POST.get("username")
        if password != cpassword:
            messages.error(request, 'Password did not match!')
            return render(request, "accounts/signup.html", context = {'portal':'apartment_owners'})
        try:
            if User.objects.get(email=email):
                messages.warning(request, 'Email Id already exists!')
                return render(request, "accounts/signup.html", context = {'portal':'apartment_owners'})
        except Exception as e:
            print("New account creation process started!")
        try:
            if User.objects.get(username=username):
                messages.warning(request, 'Username already exists!')
                return render(request, "accounts/signup.html", context = {'portal':'apartment_owners'})
        except Exception as e:
            print("New account creation process started!")
        user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
        activation_key = uuid4()
        users = ApartmentOwners(user_id=user.id, name=name, username=username, email=email, password=password, phone_no=phone_no, activation_key=activation_key)
        users.save()
        messages.success(request, 'Account Created Successfully! Check your email to activate your account.')
        return redirect('apartment_owners_login')
    return render(request, "accounts/signup.html", context = {'portal':'apartment_owners'})

# LawEnforcementUsers LogOut
@login_required(login_url='law_enforcement_users_login')
def law_enforcement_users_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('law_enforcement_users_login'))

# LawEnforcementUsers Login
def law_enforcement_users_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('law_enforcement_dashboard'))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            checkUser = LawEnforcementUsers.objects.get(username=username, password=password)
        except Exception as e:
            messages.error(request, 'Invalid Login Credentials!')
            return render(request, 'accounts/signin.html', context = {'portal':'law_enforcement_users'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('law_enforcement_dashboard'))
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return render(request, 'accounts/signin.html', context = {'portal':'law_enforcement_users'})
    return render(request, 'accounts/signin.html', context = {'portal':'law_enforcement_users'})

# LawEnforcementUsers Registeration
def law_enforcement_users_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('law_enforcement_dashboard'))
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        username = request.POST.get("username")
        if password != cpassword:
            messages.error(request, 'Password did not match!')
            return render(request, "accounts/signup.html", context = {'portal':'law_enforcement_users'})
        try:
            if User.objects.get(email=email):
                messages.warning(request, 'Email Id already exists!')
                return render(request, "accounts/signup.html", context = {'portal':'law_enforcement_users'})
        except Exception as e:
            print("New account creation process started!")
        try:
            if User.objects.get(username=username):
                messages.warning(request, 'Username already exists!')
                return render(request, "accounts/signup.html", context = {'portal':'law_enforcement_users'})
        except Exception as e:
            print("New account creation process started!")
        user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
        activation_key = uuid4()
        users = LawEnforcementUsers(user_id=user.id, name=name, username=username, email=email, password=password, phone_no=phone_no, activation_key=activation_key)
        users.save()
        messages.success(request, 'Account Created Successfully! Check your email to activate your account.')
        return redirect('law_enforcement_users_login')
    return render(request, "accounts/signup.html", context = {'portal':'law_enforcement_users'})
