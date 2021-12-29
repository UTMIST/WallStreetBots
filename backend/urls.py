from django.contrib import admin
from django.urls import path, include

BASE_API_URL = "api"


urlpatterns = [
    path(f"{BASE_API_URL}/", include('backend.home.urls')),
    path(f"{BASE_API_URL}/tradingbot/", include('backend.tradingbot.urls')),
    path(f"{BASE_API_URL}/admin/", admin.site.urls),
    path('', include('backend.auth0login.urls')),
]
