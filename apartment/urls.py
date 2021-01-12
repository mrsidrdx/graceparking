from django.urls import path
from apartment.views import *

urlpatterns = [
    path('dashboard/', apartment_dashboard,name='apartment_dashboard'),
    path('update_profile/<int:apartment_id>/', update_profile,name='update_profile'),
    path('view/vehicles/<int:apartment_id>/', show_all_registered_vehicles,name='show_all_registered_vehicles'),
    path('register/vehicle/<int:apartment_id>/', model_vehicle,name='model_vehicle'),
    path('save/vehicle/<int:apartment_id>/', save_vehicle,name='save_vehicle'),
    path('update/vehicle/<int:apartment_id>/<int:vehicle_id>/', update_vehicle,name='update_vehicle'),
    path('delete/vehicle/<int:apartment_id>/<int:vehicle_id>/', delete_vehicle,name='delete_vehicle'),
    path('view/stickers/<int:apartment_id>/', show_all_generated_stickers,name='show_all_generated_stickers'),
    path('generate/sticker/<int:apartment_id>/', model_sticker,name='model_sticker'),
    path('save/sticker/<int:apartment_id>/', save_sticker,name='save_sticker'),
    path('update/sticker/<int:apartment_id>/<int:sticker_id>/', update_sticker,name='update_sticker'),
    path('delete/sticker/<int:apartment_id>/<int:sticker_id>/', delete_sticker,name='delete_sticker'),
]
