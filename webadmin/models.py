from django.db import models

# Create your models here.

class ReceivedMessages(models.Model):
    name = models.CharField(default="", max_length=252)
    email = models.CharField(default="", max_length=252)
    subject = models.CharField(default="", max_length=400)
    message = models.TextField(default="")
