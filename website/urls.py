from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.admin_login, name = 'admin_login'),
    path('home/',views.home, name = 'home'),
    path('logout_view/',views.logout_view, name = 'logout'),
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('settings/',views.settings, name = 'settings'),
]
