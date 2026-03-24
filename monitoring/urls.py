from django.urls import path
from .views import create_keyword, run_scan_api, list_flags, update_flag_status

urlpatterns = [
    path('keywords/', create_keyword),
    path('scan/', run_scan_api),
    path('flags/', list_flags),
    path('flags/<int:id>/', update_flag_status),
]