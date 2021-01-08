from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ApartmentOwners(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='apartment_owners')
    name = models.CharField(default="", max_length=200)
    username = models.CharField(default="", max_length=200)
    profile_pic = models.FileField(default="")
    email = models.EmailField(default="", max_length=200, unique=True)
    password = models.CharField(default="", max_length=300)
    phone_no = models.CharField(default="", max_length=200, unique=True)
    address = models.TextField(default="")
    pincode = models.CharField(default="", max_length=40)
    password_recovery_key = models.CharField(default="", max_length=200)
    activation_key = models.CharField(default="", max_length=200)

class LawEnforcementUsers(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='law_enforcement_users')
    name = models.CharField(default="", max_length=200)
    username = models.CharField(default="", max_length=200)
    profile_pic = models.FileField(default="")
    email = models.EmailField(default="", max_length=200, unique=True)
    password = models.CharField(default="", max_length=300)
    phone_no = models.CharField(default="", max_length=200, unique=True)
    address = models.TextField(default="")
    pincode = models.CharField(default="", max_length=40)
    password_recovery_key = models.CharField(default="", max_length=200)
    activation_key = models.CharField(default="", max_length=200)
