from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from webadmin.models import ReceivedMessages

# Create your views here.

def index(request):
    return render(request,'frontend/index.html', context={})

def about(request):
    return render(request,'frontend/about.html', context={})

def services(request):
    return render(request,'frontend/services.html', context={})

def work(request):
    return render(request,'frontend/work.html', context={})

def contact(request):
    return render(request,'frontend/contact.html', context={})

def send_message(request):
    message = ReceivedMessages()
    if request.POST:
        for key in request.POST:
            setattr(message,key,request.POST[key])
        message.save()
    return redirect('contact')
