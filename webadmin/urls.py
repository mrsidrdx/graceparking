from django.urls import path
from webadmin.views import *

urlpatterns = [
    path('', web_admin_dashboard,name='admin_dashboard'),
    path('dashboard/', web_admin_dashboard,name='web_admin_dashboard'),
    path('view/apartments/', show_all_apartment_owners,name='web_show_all_apartment_owners'),
    path('view/enforcement-companies/', show_all_enforcement_company,name='web_show_all_enforcement_company'),
    path('view/registered-vehicles/', show_all_registered_vehicles,name='web_show_all_registered_vehicles'),
    path('view/towed-vehicles/', show_all_towed_vehicles,name='web_show_all_towed_vehicles'),
    path('delete/apartment/<int:apartment_id>/', delete_apartment,name='web_delete_apartment'),
    path('delete/enforcement-company/<int:enforcement_id>/', delete_enforcement,name='web_delete_enforcement'),
    path('view/contact-messages/', show_messages,name='show_messages'),
]
