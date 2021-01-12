from django.db import models
from accounts.models import ApartmentOwners

# Create your models here.
class RegisteredVehicles(models.Model):
    apartment = models.ForeignKey(ApartmentOwners, on_delete = models.CASCADE, related_name='registered_apartment')
    owner_name = models.CharField(default="", max_length=200)
    owner_email = models.CharField(default="", max_length=200)
    owner_phone_no = models.CharField(default="", max_length=200)
    vehicle_name = models.CharField(default="", max_length=200)
    vehicle_type = models.CharField(default="", max_length=200)
    vehicle_color = models.CharField(default="", max_length=200)
    make = models.CharField(default="", max_length=200)
    model = models.CharField(default="", max_length=200)
    year = models.CharField(default="", max_length=200)
    vin = models.CharField(default="", max_length=200)
    license_tag_no = models.CharField(default="", max_length=200)
    date_registered = models.DateField(auto_now_add=True)

class GenerateSticker(models.Model):
    apartment = models.ForeignKey(ApartmentOwners, on_delete = models.CASCADE, related_name='sticker_registered_apartment')
    vehicle = models.ForeignKey(RegisteredVehicles, on_delete = models.CASCADE, related_name='registered_vehicle')
    sticker_color = models.CharField(default="", max_length=200)
    expiry_date = models.DateField(default="")
    qr_code_file = models.FileField(default="")
    sticker_file = models.FileField(default="")
    date_created = models.DateField(auto_now_add=True)
