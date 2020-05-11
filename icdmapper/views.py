import os
from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from MainProject import settings
from .forms import CutpasteForm
import pandas as pd
import sys
sys.path.insert(2, os.getcwd()+'\\ICD-10-Code\\')
from Mapper import Mapper
from Extractor import Extractor

obj = Mapper()

# Create your views here.
def about(request):
    return render(request, "about.html")
    

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
    return redirect("home")


@login_required(login_url='/icdmapper/login/')
def homepage(request):
    if request.method == 'POST':
        form = CutpasteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            field = data['diagnosis']
            answer = obj.map([field])
            return render(request, 'icdhome.html', {'form': form, 'answer': answer})
        else:
            print('error')
    else:
        form = CutpasteForm()
    return render(request, 'icdhome.html', {'form': form})


@login_required(login_url='/icdmapper/login/')
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = '/icdmapper'
        url = "."+fs.url(name)  # url to the file
        ext = Extractor([url])
        data = ext.getalldiagnosis()
        #answer = [data[x] for x in data]
        final_result = {}
        for key,value in data.items():
            final_result[key] = obj.map(value)
        #print(final_result)
        form = CutpasteForm()
        context = {
            'form': form,
            'url': uploaded_file.name,
            'result': final_result
        }
        return render(request, 'icdhome.html', context)
    form = CutpasteForm()
    return render(request, 'icdhome.html', {'form': form})


@login_required(login_url='/icdmapper/login/')
def loadstorage(request):
    if request.method == 'POST':
        filenames = request.POST.getlist('userselect')
        for i in range(len(filenames)):
            filenames[i]="./media/icdmapper_files/"+filenames[i]
        #print(filenames)
        ext = Extractor(filenames)
        data = ext.getalldiagnosis()
        # answer = [data[x] for x in data]
        result = {}
        for key, value in data.items():
            result[key] = obj.map(value)
        #print(final_result)
        return render(request, 'loadstore.html',
                      {'total_files': os.listdir(settings.MEDIA_ROOT+"\\icdmapper_files\\"), 'path': settings.MEDIA_ROOT,
                       'result': result})
    return render(request, 'loadstore.html',
                  {'total_files': os.listdir(settings.MEDIA_ROOT+"\\icdmapper_files\\"), 'path': settings.MEDIA_ROOT})


def icdset(request):
    data = pd.read_csv("./static/icddata/icdset.csv")
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return render(request, "icdset.html", context)
