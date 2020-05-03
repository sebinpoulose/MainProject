from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.icdmapper_login, name='icdmapperlogin'),
    path('icdmapperauth/', views.login_user, name='icdmapperauth'),
    path('home/', views.homepage, name='icdmapperhomepage'),
    path("logout/", views.logout_request, name="logout"),
    path("icdupload/", views.upload_file, name="icdupload"),
    path("loadstorage/", views.loadstorage, name="loadstorage"),
    path("about/", views.about, name="about"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
