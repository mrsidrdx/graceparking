from django.urls import path
from accounts.views import *

urlpatterns = [
    path('webadmin/logout/', web_admin_logout,name='web_admin_logout'),
    path('webadmin/login/', web_admin_login,name='web_admin_login'),
    path('apartment/logout/', apartment_owners_logout,name='apartment_owners_logout'),
    path('apartment/login/', apartment_owners_login,name='apartment_owners_login'),
    path('apartment/register/', apartment_owners_register,name='apartment_owners_register'),
    path('law-enforcement/logout/', law_enforcement_users_logout,name='law_enforcement_users_logout'),
    path('law-enforcement/login/', law_enforcement_users_login,name='law_enforcement_users_login'),
    path('law-enforcement/register/', law_enforcement_users_register,name='law_enforcement_users_register'),
]
