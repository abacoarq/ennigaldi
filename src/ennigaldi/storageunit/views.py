from django.shortcuts import render
from django.http import HttpResponse
from .models import Unit

def unit_list(request):
    return HttpResponse('A list of storage units.')

def field_form(request):
    return HttpResponse('The unit entry form.')
