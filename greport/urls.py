from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.greport_login, name='greportlogin'),
    path('greportauth/', views.login_user, name='greportauth'),
    path('home/', views.homepage, name='greporthomepage'),
]
