from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login, name = 'admin_login'),
    path('home/',views.home, name = 'home'),
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('settings/',views.settings, name = 'settings'),
]
