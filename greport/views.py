from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from .loader import get_data_object, dataloader
from .graph_maker import make_graph, make_trend


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


def about(request):
    return render(request, "about.html")


@login_required(login_url='/greports/login/')
def homepage(request):
    df = dataloader()
    pids = df['PatientID'].unique()
    return render(request, "greporthome.html", {'pids': pids})


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


@login_required(login_url='/greports/login/')
def gen_report(request):
    data = get_data_object(int(request.GET['pid']))
    context = {'pid': request.GET['pid'], 'data': data}
    return render(request, "generated.html", context)


@login_required(login_url='/greports/login/')
def gen_graph(request):
    make_graph(int(request.GET['pid']))
    context = {}
    return render(request, "report.html", context)


@login_required(login_url='/greports/login/')
def one_graph(request):
    pid = request.GET['pid']
    testname = request.GET['testname']
    make_trend(pid, testname)
    return render(request, "report.html", {})
