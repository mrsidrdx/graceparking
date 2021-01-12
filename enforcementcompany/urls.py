from django.urls import path
from enforcementcompany.views import *

urlpatterns = [
    path('dashboard/', law_enforcement_dashboard,name='law_enforcement_dashboard'),
    path('update_profile/<int:enforcement_id>/', update_profile,name='enf_update_profile'),
    path('view/vehicles/<int:enforcement_id>/', show_all_towed_vehicles,name='show_all_towed_vehicles'),
    path('tow/vehicle/<int:enforcement_id>/', model_vehicle,name='enf_model_vehicle'),
    path('save/vehicle/<int:enforcement_id>/', save_vehicle,name='enf_save_vehicle'),
    path('update/vehicle/<int:enforcement_id>/<int:vehicle_id>/', update_vehicle,name='enf_update_vehicle'),
    path('delete/vehicle/<int:enforcement_id>/<int:vehicle_id>/', delete_vehicle,name='enf_delete_vehicle'),
    path('change_fine_paid/<int:vehicle_id>/<str:action>/', change_fine_paid,name='change_fine_paid'),
    path('change_vehicle_returned/<int:vehicle_id>/<str:action>/', change_vehicle_returned,name='change_vehicle_returned'),
]
