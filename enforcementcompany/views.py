from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from .models import *
from accounts.models import ApartmentOwners, LawEnforcementUsers
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.

def get_enforcement(request):
    try:
        enforcement = LawEnforcementUsers.objects.get(user_id=request.user.id)
        return enforcement
    except Exception as e:
        return 0

@login_required(login_url='law_enforcement_users_login')
def law_enforcement_dashboard(request):
    if get_enforcement(request) == 0:
        return redirect('law_enforcement_users_logout')
    enforcement = get_enforcement(request)
    total_vehicles_count = TowedVehicles.objects.filter(enforcement_id=enforcement.id).count()
    today = datetime.now()
    vehicles_count_year = TowedVehicles.objects.filter(enforcement_id=enforcement.id, towed_date__year=today.year).count()
    vehicles_count_month = TowedVehicles.objects.filter(enforcement_id=enforcement.id, towed_date__year=today.year, towed_date__month=today.month).count()
    registered_vehicles_count_monthwise = []
    for i in range(1,13):
        registered_vehicles_count_monthwise.append(TowedVehicles.objects.filter(enforcement_id=enforcement.id, towed_date__year=today.year, towed_date__month=i).count())
    context = {
        "enforcementId": enforcement.id,
        "enforcement": enforcement,
        "total_vehicles_count": total_vehicles_count,
        "vehicles_count_year": vehicles_count_year,
        "vehicles_count_month": vehicles_count_month,
        "registered_vehicles_count_monthwise": registered_vehicles_count_monthwise,
    }
    return render(request, 'enforcementcompany/dashboard.html', context=context)

@login_required(login_url='law_enforcement_users_login')
def update_profile(request, enforcement_id):
    if get_enforcement(request) == 0:
        return redirect('law_enforcement_users_logout')
    enforcement = get_enforcement(request)
    if request.POST:
        profile_object = LawEnforcementUsers.objects.get(id=enforcement_id)
        user = User.objects.get(id=profile_object.user_id)
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.set_password(user.password)
        user.save()
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(profile_object,key,new_value)

        for key in request.FILES:
            file_instance = request.FILES[key]
            tempFileName = 'LawEnforcementUsers'+'_'+datetime.now().strftime("%m%d%y%H%M%S")+'.'+str(request.FILES[key]).split('.')[-1]
            fs = FileSystemStorage()
            filename = fs.save(tempFileName, file_instance)
            uploaded_file_url = fs.url(filename)
            setattr(profile_object,key,uploaded_file_url)

        profile_object.save()

    profile_object = LawEnforcementUsers.objects.get(id=enforcement_id)
    context = {
        "enforcementId": enforcement_id,
        "profile_object": profile_object,
        "enforcement": enforcement,
    }
    return render(request, 'enforcementcompany/updateProfile.html', context=context)

@login_required(login_url='law_enforcement_users_login')
def show_all_towed_vehicles(request, enforcement_id):
    if get_enforcement(request) == 0:
        return redirect('law_enforcement_users_logout')
    enforcement = get_enforcement(request)
    vehicle_objects = TowedVehicles.objects.filter(enforcement_id=enforcement_id).values()
    context = {
        "enforcementId": enforcement_id,
        "vehicle_objects": vehicle_objects,
        "enforcement": enforcement,
    }
    return render(request, 'enforcementcompany/showAllVehicles.html', context=context)

@login_required(login_url='law_enforcement_users_login')
def model_vehicle(request, enforcement_id):
    if get_enforcement(request) == 0:
        return redirect('law_enforcement_users_logout')
    enforcement = get_enforcement(request)
    if 'edit' in request.GET:
        vehicle_object = TowedVehicles.objects.get(id=request.GET['vehicleId'])
    else:
        vehicle_object = []
    context = {
        "enforcementId": enforcement_id,
        "vehicle_object": vehicle_object,
        "enforcement": enforcement,
    }
    return render(request, 'enforcementcompany/registerVehicle.html', context=context)

@login_required(login_url='law_enforcement_users_login')
def save_vehicle(request, enforcement_id):
    vehicle_object = TowedVehicles(enforcement_id=enforcement_id)
    if request.POST:
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(vehicle_object,key,new_value)
        vehicle_object.save()
    return redirect('show_all_towed_vehicles', enforcement_id=enforcement_id)

@login_required(login_url='law_enforcement_users_login')
def update_vehicle(request, enforcement_id, vehicle_id):
    vehicle_object = TowedVehicles.objects.get(id=vehicle_id)
    if request.POST:
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(vehicle_object,key,new_value)
        vehicle_object.save()
    return redirect('show_all_towed_vehicles', enforcement_id=enforcement_id)

@login_required(login_url='law_enforcement_users_login')
def delete_vehicle(request, enforcement_id, vehicle_id):
    vehicle_object = TowedVehicles.objects.get(id=vehicle_id)
    vehicle_object.delete()
    return HttpResponse('Towed Vehicle Deleted!')

@csrf_exempt
def change_fine_paid(request, vehicle_id, action):
    vehicle_object = TowedVehicles.objects.get(id=vehicle_id)
    vehicle_object.is_fine_paid = eval(action)
    vehicle_object.save()
    return HttpResponse('Fine Action Changed!')

@csrf_exempt
def change_vehicle_returned(request, vehicle_id, action):
    vehicle_object = TowedVehicles.objects.get(id=vehicle_id)
    vehicle_object.is_vehicle_returned = eval(action)
    vehicle_object.save()
    return HttpResponse('Vehicle Returned Action Changed!')
