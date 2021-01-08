from django.urls import path
from frontend.views import *

urlpatterns = [
    path('', index,name='index'),
    path('about/', about,name='about'),
    path('services/', services,name='services'),
    path('work/', work,name='work'),
    path('contact/', contact,name='contact'),
]
