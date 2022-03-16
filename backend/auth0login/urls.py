from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('machine-learning', views.machine_learning),
    path('positions', views.positions),
    path('orders', views.orders),
    path('user-settings', views.user_settings),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
