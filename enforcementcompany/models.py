from django.db import models
from accounts.models import ApartmentOwners, LawEnforcementUsers

# Create your models here.
class TowedVehicles(models.Model):
    enforcement = models.ForeignKey(LawEnforcementUsers, on_delete = models.CASCADE, related_name='towed_company')
    owner_name = models.CharField(default="", max_length=200)
    owner_email = models.CharField(default="", max_length=200)
    owner_phone_no = models.CharField(default="", max_length=200)
    vehicle_name = models.CharField(default="", max_length=200)
    vehicle_type = models.CharField(default="", max_length=200)
    vehicle_color = models.CharField(default="", max_length=200)
    towed_date = models.DateField(default="")
    fine_amount = models.PositiveIntegerField(default=0)
    is_fine_paid = models.BooleanField(default=False)
    is_vehicle_returned = models.BooleanField(default=False)
