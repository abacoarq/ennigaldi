from django.shortcuts import render
from django.http import HttpResponse
from .models import ObjectIdentification

def index(request):
    return HttpResponse('Nothing here yet.')

def field_form(request):
    return HttpResponse('This is where the field survey form will appear.')

def next_entry(request):
    return HttpResponse('This page shows after saving an entry, offering to add another.')

def object_list(request):
    return HttpResponse('There will be a list of entered works here.')

def image_form(request):
    return HttpResponse('A form to enter images, possibly in bulk, will appear here.')

def m305(request):
    return render(request, 'objectinfo/m305.html', {})

def xml(request):
    return HttpResponse('Here there be VRA Core 4 XML.')
