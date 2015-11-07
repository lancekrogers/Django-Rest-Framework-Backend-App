from django.shortcuts import render

# Create your views here.


def landing(request):
    return render(request, 'preapplanding/index.html')


def test(request):
    return render(request, 'test/test.html')