from django.shortcuts import render

# Create your views here.


def icdmapper_login(request):
    return render(request, "icdmapperlogin.html", {})
