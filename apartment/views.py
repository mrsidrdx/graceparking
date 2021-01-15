from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from .models import *
from accounts.models import ApartmentOwners
import qrcode
from PIL import Image
from django.conf import settings
import os
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.

def get_apartment(request):
    try:
        apartment = ApartmentOwners.objects.get(user_id=request.user.id)
        return apartment
    except Exception as e:
        return 0

@login_required(login_url='apartment_owners_login')
def apartment_dashboard(request):
    if get_apartment(request) == 0:
        return redirect('apartment_owners_logout')
    apartment = get_apartment(request)
    total_vehicles_count = RegisteredVehicles.objects.filter(apartment_id=apartment.id).count()
    total_stickers_count = GenerateSticker.objects.filter(apartment_id=apartment.id).count()
    today = datetime.now()
    vehicles_count_year = RegisteredVehicles.objects.filter(apartment_id=apartment.id, date_registered__year=today.year).count()
    vehicles_count_month = RegisteredVehicles.objects.filter(apartment_id=apartment.id, date_registered__year=today.year, date_registered__month=today.month).count()
    stickers_count_year = GenerateSticker.objects.filter(apartment_id=apartment.id, date_created__year=today.year).count()
    stickers_count_month = GenerateSticker.objects.filter(apartment_id=apartment.id, date_created__year=today.year, date_created__month=today.month).count()
    registered_vehicles_count_monthwise = []
    for i in range(1,13):
        registered_vehicles_count_monthwise.append(RegisteredVehicles.objects.filter(apartment_id=apartment.id, date_registered__year=today.year, date_registered__month=i).count())
    context = {
        "apartmentId": apartment.id,
        "apartment": apartment,
        "total_vehicles_count": total_vehicles_count,
        "total_stickers_count": total_stickers_count,
        "vehicles_count_year": vehicles_count_year,
        "vehicles_count_month": vehicles_count_month,
        "stickers_count_year": stickers_count_year,
        "stickers_count_month": stickers_count_month,
        "registered_vehicles_count_monthwise": registered_vehicles_count_monthwise,
    }
    return render(request, 'apartment/dashboard.html', context=context)

@login_required(login_url='apartment_owners_login')
def update_profile(request, apartment_id):
    if get_apartment(request) == 0:
        return redirect('apartment_owners_logout')
    apartment = get_apartment(request)
    if request.POST:
        profile_object = ApartmentOwners.objects.get(id=apartment_id)
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
            tempFileName = 'ApartmentOwners'+'_'+datetime.now().strftime("%m%d%y%H%M%S")+'.'+str(request.FILES[key]).split('.')[-1]
            fs = FileSystemStorage()
            filename = fs.save(tempFileName, file_instance)
            uploaded_file_url = fs.url(filename)
            setattr(profile_object,key,uploaded_file_url)

        profile_object.save()

    profile_object = ApartmentOwners.objects.get(id=apartment_id)
    context = {
        "apartment": apartment,
        "apartmentId": apartment_id,
        "profile_object": profile_object,
    }
    return render(request, 'apartment/updateProfile.html', context=context)

@login_required(login_url='apartment_owners_login')
def show_all_registered_vehicles(request, apartment_id):
    if get_apartment(request) == 0:
        return redirect('apartment_owners_logout')
    apartment = get_apartment(request)
    vehicle_objects = RegisteredVehicles.objects.filter(apartment_id=apartment_id).values()
    context = {
        "apartment": apartment,
        "apartmentId": apartment_id,
        "vehicle_objects": vehicle_objects,
    }
    return render(request, 'apartment/showAllVehicles.html', context=context)

@login_required(login_url='apartment_owners_login')
def model_vehicle(request, apartment_id):
    if get_apartment(request) == 0:
        return redirect('apartment_owners_logout')
    apartment = get_apartment(request)
    if 'edit' in request.GET:
        vehicle_object = RegisteredVehicles.objects.get(id=request.GET['vehicleId'])
    else:
        vehicle_object = []
    context = {
        "apartmentId": apartment_id,
        "vehicle_object": vehicle_object,
        "apartment": apartment,
    }
    return render(request, 'apartment/registerVehicle.html', context=context)

@login_required(login_url='apartment_owners_login')
def save_vehicle(request, apartment_id):
    vehicle_object = RegisteredVehicles(apartment_id=apartment_id)
    if request.POST:
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(vehicle_object,key,new_value)
        vehicle_object.save()
    return redirect('show_all_registered_vehicles', apartment_id=apartment_id)

@login_required(login_url='apartment_owners_login')
def update_vehicle(request, apartment_id, vehicle_id):
    vehicle_object = RegisteredVehicles.objects.get(id=vehicle_id)
    if request.POST:
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(vehicle_object,key,new_value)
        vehicle_object.save()
    return redirect('show_all_registered_vehicles', apartment_id=apartment_id)

@login_required(login_url='apartment_owners_login')
def delete_vehicle(request, apartment_id, vehicle_id):
    vehicle_object = RegisteredVehicles.objects.get(id=vehicle_id)
    vehicle_object.delete()
    return HttpResponse('Vehicle Deleted!')

@login_required(login_url='apartment_owners_login')
def show_all_generated_stickers(request, apartment_id):
    if get_apartment(request) == 0:
        return redirect('apartment_owners_logout')
    apartment = get_apartment(request)
    sticker_objects = GenerateSticker.objects.filter(apartment_id=apartment_id)
    context = {
        "apartmentId": apartment_id,
        "sticker_objects": sticker_objects,
        "apartment": apartment,
    }
    return render(request, 'apartment/showAllStickers.html', context=context)

@login_required(login_url='apartment_owners_login')
def model_sticker(request, apartment_id):
    if get_apartment(request) == 0:
        return redirect('apartment_owners_logout')
    apartment = get_apartment(request)
    if 'edit' in request.GET:
        sticker_object = GenerateSticker.objects.get(id=request.GET['stickerId'])
    else:
        sticker_object = []
    vehicle_objects = RegisteredVehicles.objects.filter(apartment_id=apartment_id).values()
    context = {
        "apartmentId": apartment_id,
        "sticker_object": sticker_object,
        "vehicle_objects": vehicle_objects,
        "apartment": apartment,
    }
    return render(request, 'apartment/generateSticker.html', context=context)

def generate_sticker(data_dict, color, sticker_object):
    qr = qrcode.QRCode(
            version = 1,
            box_size = 8,
            border = 1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    data = {
        'Apartment Name' : apartment.name,
        'Owner Name' : data_dict.owner_name,
        'Owner Email' : data_dict.owner_email,
        'Owner Phone' : data_dict.owner_phone_no,
        'Vehicle Name' : data_dict.vehicle_name,
        'Vehicle Type' : data_dict.vehicle_type,
        'Vehicle Color' : data_dict.vehicle_color,
        'Make' : data_dict.make,
        'Model' : data_dict.model,
        'Year' : data_dict.year,
        'VIN' : data_dict.vin,
        'License Plate No.' : data_dict.license_tag_no,
    }
    qr.add_data(data)
    qr.make(fit=True)
    if color[0:4] == 'rgba':
        rgb_color = eval(color[4:])[0:3]
        hex_color = '#' + '%02x%02x%02x' % rgb_color
    else:
        hex_color = color
    img = qr.make_image(fill_color=hex_color, back_color="white")
    tempFileName = 'qrcode'+'_'+datetime.now().strftime("%m%d%y%H%M%S")+'.png'
    uploaded_file_url = "/media/"+tempFileName
    save_qr_loc = os.path.join(settings.BASE_DIR, "media/"+tempFileName)
    img.save(save_qr_loc)
    setattr(sticker_object,'qr_code_file',uploaded_file_url)
    read_sticker_loc = os.path.join(settings.BASE_DIR, "static/webadmin/img/sample-parking-sticker.png")
    first_image = Image.open(read_sticker_loc)
    second_image = Image.open(save_qr_loc)
    first_image.paste(second_image, (600,400))
    tempFileName = 'sticker'+'_'+datetime.now().strftime("%m%d%y%H%M%S")+'.png'
    uploaded_file_url = "/media/"+tempFileName
    save_sticker_loc = os.path.join(settings.BASE_DIR, "media/"+tempFileName)
    first_image.save(save_sticker_loc)
    setattr(sticker_object,'sticker_file',uploaded_file_url)
    sticker_object.save()
    print('Sticker Generated!')

@login_required(login_url='apartment_owners_login')
def save_sticker(request, apartment_id):
    sticker_object = GenerateSticker(apartment_id=apartment_id)
    if request.POST:
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(sticker_object,key,new_value)
        sticker_object.save()
    vehicle_object = RegisteredVehicles.objects.get(id=sticker_object.vehicle_id)
    qrcode_color = sticker_object.sticker_color
    generate_sticker(vehicle_object, qrcode_color, sticker_object)
    return redirect('show_all_generated_stickers', apartment_id=apartment_id)

@login_required(login_url='apartment_owners_login')
def update_sticker(request, apartment_id, sticker_id):
    sticker_object = GenerateSticker.objects.get(id=sticker_id)
    if request.POST:
        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and len(request.POST[key]) != 0:
                new_value = request.POST[key]
                setattr(sticker_object,key,new_value)
        sticker_object.save()
    vehicle_object = RegisteredVehicles.objects.get(id=sticker_object.vehicle_id)
    qrcode_color = sticker_object.sticker_color
    generate_sticker(vehicle_object, qrcode_color, sticker_object)
    return redirect('show_all_generated_stickers', apartment_id=apartment_id)

@login_required(login_url='apartment_owners_login')
def delete_sticker(request, apartment_id, sticker_id):
    sticker_object = GenerateSticker.objects.get(id=sticker_id)
    sticker_object.delete()
    return HttpResponse('Sticker Deleted!')
