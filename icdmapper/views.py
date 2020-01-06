from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def icdmapper_login(request):
    return render(request, "icdmapperlogin.html", {})


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/icdmapper/home')
    #return render_to_response('greportlogin.html', context=RequestContext(request))
    return render(request, 'icdmapperlogin.html', {'valid': False})


@login_required(login_url='/icdmapper/login/')
def homepage(request):
    return render(request, "icdhome.html", {})
