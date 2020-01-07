from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.icdmapper_login, name='icdmapperlogin'),
    path('icdmapperauth/', views.login_user, name='icdmapperauth'),
    path('home/', views.homepage, name='icdmapperhomepage'),
    path("logout/", views.logout_request, name="logout"),
]
