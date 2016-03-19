from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {}
    return render(request, 'pdfjs/index.html', context)

def viewer(request):
    context = {}
    return render(request, 'pdfjs/viewer.html', context)
