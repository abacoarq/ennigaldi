from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Unit

class unit_list(ListView):
    model = Unit
    template_name = 'storageunit/unit_list.html' # default
    context_object_name = unit_list # default
    paginate_by = 25
    queryset = Unit.objects.all() # default

def unit_detail(request, unit_id):
    unit_data = get_object_or_404(Unit, pk=unit_id)
    return render(request, 'storageunit/detail.html', {'unit_data': unit_data})

def field_form(request):
    return HttpResponse('The unit entry form.')
