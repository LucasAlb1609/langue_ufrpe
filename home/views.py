from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'index.html')


