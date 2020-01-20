import os

from django.shortcuts import render, redirect, render_to_response
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext

from MainProject import settings
from .forms import CutpasteForm


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
    return render(request, 'icdmapperlogin.html', {'valid': False})


def logout_request(request):
    logout(request)
    # return render(request, "Home_page.html", {})
    return redirect("home")


@login_required(login_url='/icdmapper/login/')
def homepage(request):
    if request.method == 'POST':
        form = CutpasteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            field = data['diagnosis']
            answer = field
            # print(field)
            return render(request, 'icdhome.html', {'form': form, 'answer': answer})
        else:
            print('error')
    else:
        form = CutpasteForm()
    return render(request, 'icdhome.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = '/icdmapper'
        url = fs.url(name)  # url to the file
        print(url)
        form = CutpasteForm()
        context = {
            'form': form,
            'url': uploaded_file.name,
            'result': "mapped value"
        }
        return render(request, 'icdhome.html', context)
    form = CutpasteForm()
    return render(request, 'icdhome.html', {'form': form})


def loadstorage(request):
    if request.method == 'POST':
        filenames = request.POST.getlist('userselect')
        print(filenames)
        result = str(filenames)
        return render(request, 'loadstore.html',
                      {'total_files': os.listdir(settings.MEDIA_ROOT), 'path': settings.MEDIA_ROOT,
                       'result': result})
    return render(request, 'loadstore.html',
                  {'total_files': os.listdir(settings.MEDIA_ROOT), 'path': settings.MEDIA_ROOT})
