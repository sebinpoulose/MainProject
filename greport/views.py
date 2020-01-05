from django.shortcuts import render

# Create your views here.


def greport_login(request):
    return render(request, "greportlogin.html", {})
