from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
