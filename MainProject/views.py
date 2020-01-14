from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, "Home_page.html", {})


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def test_500(request):
    raise Exception('Make response code 500!')
