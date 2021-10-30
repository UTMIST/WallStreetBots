from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check_db_connection', views.get_time, name="check_db"),
]
