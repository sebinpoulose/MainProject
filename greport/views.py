from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd

# Create your views here.


def greport_login(request):
    return render(request, "greportlogin.html", {})


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/greports/home')
    return render(request, 'greportlogin.html', {'valid': False})


@login_required(login_url='/greports/login/')
def homepage(request):
    return render(request, "greporthome.html", {})


@login_required(login_url='/greports/login/')
def logout_request(request):
    logout(request)
    return redirect("home")


@login_required(login_url='/greports/login/')
def testset(request):
    data = pd.read_csv("./static/greportdata/TestSet.csv")
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return render(request, "greporthome.html", context)
