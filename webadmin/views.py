from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from accounts.models import ApartmentOwners, LawEnforcementUsers
from apartment.models import *
from enforcementcompany.models import *
from .models import *

# Create your views here.

@login_required(login_url='web_admin_login')
def web_admin_dashboard(request):
    apartment_count = ApartmentOwners.objects.all().count()
    enforcement_count = LawEnforcementUsers.objects.all().count()
    reg_vehicles_count = RegisteredVehicles.objects.all().count()
    tow_vehicles_count = TowedVehicles.objects.all().count()
    today = datetime.now()
    registered_vehicles_count_monthwise, towed_vehicles_count_monthwise = [], []
    for i in range(1,13):
        registered_vehicles_count_monthwise.append(RegisteredVehicles.objects.filter(date_registered__year=today.year, date_registered__month=i).count())
    for i in range(1,13):
        towed_vehicles_count_monthwise.append(TowedVehicles.objects.filter(towed_date__year=today.year, towed_date__month=i).count())
    context = {
        "apartment_count": apartment_count,
        "enforcement_count": enforcement_count,
        "reg_vehicles_count": reg_vehicles_count,
        "tow_vehicles_count": tow_vehicles_count,
        "towed_vehicles_count_monthwise": towed_vehicles_count_monthwise,
        "registered_vehicles_count_monthwise": registered_vehicles_count_monthwise,
    }
    return render(request, 'webadmin/dashboard.html', context=context)

@login_required(login_url='web_admin_login')
def show_all_apartment_owners(request):
    apartment_objects = ApartmentOwners.objects.all().values()
    context = {
        "apartment_objects": apartment_objects,
    }
    return render(request, 'webadmin/showAllApartments.html', context=context)

@login_required(login_url='web_admin_login')
def show_all_enforcement_company(request):
    enforcement_objects = LawEnforcementUsers.objects.all().values()
    context = {
        "enforcement_objects": enforcement_objects,
    }
    return render(request, 'webadmin/showAllEnforcements.html', context=context)

@login_required(login_url='web_admin_login')
def show_all_registered_vehicles(request):
    vehicle_objects = RegisteredVehicles.objects.all().values()
    context = {
        "vehicle_objects": vehicle_objects,
    }
    return render(request, 'webadmin/showAllRegVehicles.html', context=context)

@login_required(login_url='web_admin_login')
def show_all_towed_vehicles(request):
    vehicle_objects = TowedVehicles.objects.all().values()
    context = {
        "vehicle_objects": vehicle_objects,
    }
    return render(request, 'webadmin/showAllTowedVehicles.html', context=context)

@login_required(login_url='web_admin_login')
def delete_apartment(request, apartment_id):
    apartment = ApartmentOwners.objects.get(id=apartment_id)
    user = User.objects.get(id=apartment.user_id)
    apartment.delete()
    user.delete()
    return HttpResponse('Apartment Deleted!')

@login_required(login_url='web_admin_login')
def delete_enforcement(request, enforcement_id):
    enforcement = LawEnforcementUsers.objects.get(id=enforcement_id)
    user = User.objects.get(id=enforcement.user_id)
    enforcement.delete()
    user.delete()
    return HttpResponse('Enforcement Deleted!')

@login_required(login_url='web_admin_login')
def show_messages(request):
    messages = ReceivedMessages.objects.all()
    context = {
        "contact_messages": messages,
    }
    return render(request, 'webadmin/showAllMessages.html', context=context)
