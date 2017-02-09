from django.shortcuts import render
from django.http import HttpResponse
from .models import Unit

def unit_list(request):
    list_of_units = Unit.objects.all()
    return render(request, 'storageunit/list.html', {'list_of_units': list_of_units})

def unit_detail(request, unit_id):
    unit_data = get_object_or_404(Unit, pk=unit_id)
    return render(request, 'storageunit/detail.html', {'unit_data': unit_data})

def field_form(request):
    return HttpResponse('The unit entry form.')
